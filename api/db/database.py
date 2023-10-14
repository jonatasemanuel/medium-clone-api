from sqlmodel import SQLModel, create_engine, Session

from decouple import config


DB_URL = config('DB_URL')
engine = create_engine(DB_URL)
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
