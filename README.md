### Тестовый проект с курса Егора

uvicorn main:app

pip install -r requirements.txt

alembic init migration (Требует установить пакет глобально в linux)

alembic revision --autogenerate -m 'initial'(Перед этим настроить alembic.ini)

