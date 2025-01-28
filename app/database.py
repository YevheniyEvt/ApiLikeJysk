from sqlmodel import create_engine, Session
from fastapi import Depends
from typing import Annotated
from sqlalchemy.engine import URL
from .config import settings

url =URL.create(
    'postgresql',
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=settings.database_port,
    database=settings.database_name
)

engine = create_engine(url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

