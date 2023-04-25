from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from uuid import UUID, uuid4
from pydantic import BaseModel

from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters

router = APIRouter(prefix="/user")


class SessionData(BaseModel):
    username: str
    count: int


cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)
backend = InMemoryBackend[UUID, SessionData]()


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
            self,
            *,
            identifier: str,
            auto_error: bool,
            backend: InMemoryBackend[UUID, SessionData],
            auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)


@router.post("/create_session")
async def create_session(name: str, response: Response):
    session = uuid4()
    initial_count = 0
    data = SessionData(username=session, count=initial_count)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    response.set_cookie(key="count", value=initial_count)
    response.set_cookie(key="name", value=name)

    return f"created session name for {name} with count {data.count}"


@router.get("/whoami", dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data


@router.get("/increase_count")
async def increase_count(response: Response, count: str | None = Cookie(default=None),
                         name: str | None = Cookie(default=None)):
    new_count = int(count) + 1
    response.set_cookie(key="count", value=new_count)

    return {"count": new_count, "name": name}


@router.post("/delete_session")
async def del_session(response: Response):
    response.delete_cookie(key="count")
    return "deleted session"
