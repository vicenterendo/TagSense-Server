from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv
from pydantic_core._pydantic_core import ValidationError
from sys import exit
import argparse
load_dotenv()

class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_prefix="TAGSENSE_")
  
  hostname: str = Field("0.0.0.0")
  port: int = Field(80)
  airport_prefix: str = Field("")
  database_url: str = Field("sqlite:///tagsense.db")
  require_squawk: bool = Field(False)
  closed: bool = Field(False)
  auto_clean: bool = Field(False)
  max_age: int = Field(0)
  validate_store: bool = Field(False)
  db_max_attempts: int = Field(5)
  ignore_arrived: bool = Field(False)

settings: Settings = Settings() # type: ignore
 
settings.closed = False
parser = argparse.ArgumentParser("TagSense Server", epilog="Environment variables are recommended. For more info consult https://github.com/vicenterendo/TagSense-Server")

parser.add_argument("-a", "--addr", "--hostname", dest="hostname", metavar="ADDR")
parser.add_argument("-p", "--port", dest="port", type=int)
parser.add_argument("-db", "--database-url", dest="database_url")
parser.add_argument("-prfx", "--airport-prefix", dest="airport_prefix")
parser.add_argument("-sqwk", "--require-squawk", action='store_true', dest="require_squawk")
parser.add_argument("-c", "--auto-clean", dest="auto_clean", action='store_true')
parser.add_argument("-ma", "--max-age", dest="max_age", metavar="SECONDS", type=int)
parser.add_argument("--validate-store", dest="validate_store", action="store_true")
parser.add_argument("--db-max-attempts", dest="db_max_attempts", metavar="ATTEMPTS", type=int)
parser.add_argument("--ignore-arrived", dest="ignore_arrived", action="store_true")

args = parser.parse_args()

settings.airport_prefix = args.airport_prefix or settings.airport_prefix
settings.hostname = args.hostname or settings.hostname
settings.port = args.port or settings.port
settings.database_url = args.database_url or settings.database_url
settings.require_squawk = args.require_squawk or settings.require_squawk
settings.auto_clean = args.auto_clean or settings.auto_clean
settings.max_age = args.max_age or settings.max_age
settings.validate_store = args.validate_store or settings.validate_store
settings.db_max_attempts = args.db_max_attempts or settings.db_max_attempts
settings.ignore_arrived = args.ignore_arrived or settings.ignore_arrived

missing_setting = False
for arg, value in settings.__dict__.items():
  if value is None:
    print(f"ERR: {arg} must be provided.")
    missing_setting = True

if missing_setting: exit()