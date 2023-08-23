
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import pymysql.err
import sqlalchemy.exc
from . import globals

Base = declarative_base()
while True:
  try:
    engine = create_engine(
      globals.DATABASE_URL, 
      connect_args = {"check_same_thread": False} if globals.DATABASE_URL.startswith("sqlite://") else {}
    )
    break
  except sqlalchemy.exc.OperationalError or pymysql.err.OperationalError:
    print(f"ERR: Failed to connect to DB at \"{globals.DATABASE_URL}\" failed, retrying...")
  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)