from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import time
import threading
from .settings import settings

Base = declarative_base()
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith(
        "sqlite://") else {}
)


def auto_cleaner():
    from . import crud, utils
    skipped_iterations = 0
    while True:
        time.sleep(1)

        if settings.closed:
            break
        skipped_iterations += 1

        if skipped_iterations != 10:
            continue
        skipped_iterations = 0

        session = SessionLocal()
        flights = crud.get_flights(session)

        for flight in flights:
            if not utils.validate_flight(flight):
                session.delete(flight)

        session.commit()
        session.close()


if settings.auto_clean:
    threading.Thread(target=auto_cleaner).start()

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
