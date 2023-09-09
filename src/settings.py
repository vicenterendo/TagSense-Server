from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import argparse

from src.cliparser import parsed_arguments

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TAGSENSE_")

    hostname: str = "0.0.0.0"
    port: int = 80
    airport_prefix: str = ""
    database_url: str = "sqlite:///tagsense.db"
    require_squawk: bool = False
    closed: bool = False
    auto_clean: bool = False
    max_age: int = 0
    validate_store: bool = False
    db_max_attempts: int = 5
    ignore_arrived: bool = False
    cors: list[str] = []


settings: Settings = Settings()
settings.closed = False
parser = argparse.ArgumentParser(
    "TagSense Server", epilog="Environment variables are recommended. For more info consult "
                              "https://github.com/vicenterendo/TagSense-Server")

settings.airport_prefix = parsed_arguments.airport_prefix if parsed_arguments.airport_prefix is not None \
    else settings.airport_prefix
settings.hostname = parsed_arguments.hostname if parsed_arguments.hostname is not None else settings.hostname
settings.port = parsed_arguments.port if parsed_arguments.port is not None else settings.port
settings.database_url = parsed_arguments.database_url if parsed_arguments.database_url is not None\
    else settings.database_url
settings.require_squawk = parsed_arguments.require_squawk if parsed_arguments.require_squawk is not None\
    else settings.require_squawk
settings.auto_clean = parsed_arguments.auto_clean if parsed_arguments.auto_clean is not None else settings.auto_clean
settings.max_age = parsed_arguments.max_age if parsed_arguments.max_age is not None else settings.max_age  # type: ignore
settings.validate_store = parsed_arguments.validate_store if parsed_arguments.validate_store is not None\
    else settings.validate_store
settings.db_max_attempts = parsed_arguments.db_max_attempts if parsed_arguments.db_max_attempts is not None\
    else settings.db_max_attempts
settings.ignore_arrived = parsed_arguments.ignore_arrived if parsed_arguments.ignore_arrived is not None else\
    settings.ignore_arrived
settings.cors = parsed_arguments.cors if parsed_arguments.cors is not None else settings.cors
