
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from .globals import *

Base = declarative_base()
engine = create_engine(
  DATABASE_URL, 
  connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite://") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)