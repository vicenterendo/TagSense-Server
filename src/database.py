
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import pymysql.err
import sqlalchemy.exc
from .settings import settings

Base = declarative_base()
while True:
  try:
    engine = create_engine(
      settings.database_url, 
      connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite://") else {}
    )
    break
  except sqlalchemy.exc.OperationalError or pymysql.err.OperationalError:
    print(f"ERR: Failed to connect to DB at \"{settings.database_url}\" failed, retrying...")
  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)