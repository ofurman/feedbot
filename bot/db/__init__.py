from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import POSTGRESQL_DATABASE_URI
from contextlib import asynccontextmanager

engine = create_engine(POSTGRESQL_DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)

from db import models

#Load database
Base.metadata.create_all(engine)

@asynccontextmanager
async def open_session():
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise
    else:
        session.commit()