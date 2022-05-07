from os import getenv
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
#load env
load_dotenv()

USER = getenv("POSTGRES_USER")
PASSWORD = getenv("POSTGRES_PASSWORD")
DB_NAME = getenv("POSTGRES_DB")
DB_PORT = getenv("DB_PORT")

db_url = f"postgresql://{USER}:{PASSWORD}@localhost:{DB_PORT}/{DB_NAME}"

engine = create_engine(db_url)
session = sessionmaker(engine) 