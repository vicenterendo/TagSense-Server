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
  origin_prefix: str = Field("")
  database_url: str = Field("sqlite:///tagsense.db")
  require_squawk: bool = Field(False)
  closed: bool = Field(False)
  auto_clean: int = Field(0)

settings: Settings = Settings()

settings.closed = False
parser = argparse.ArgumentParser("TagSense Server", epilog="Environment variables are recomended. For more info consult https://github.com/vicenterendo/TagSense-Server")

parser.add_argument("-a", "--addr", "--hostname", dest="hostname", metavar="ADDR")
parser.add_argument("-p", "--port", dest="port")
parser.add_argument("-db", "--database-url", dest="database_url")
parser.add_argument("-prfx", "--origin-prefix", dest="origin_prefix")
parser.add_argument("-sqwk", "--require-squawk", action='store_true', dest="require_squawk")
parser.add_argument("-c", "--auto-clean", dest="auto_clean", metavar="SECONDS")

args = parser.parse_args()

settings.origin_prefix = args.origin_prefix or settings.origin_prefix
settings.hostname = args.hostname or settings.hostname
settings.port = args.port or settings.port
settings.database_url = args.database_url or settings.database_url
settings.require_squawk = args.require_squawk or settings.require_squawk
settings.auto_clean = args.auto_clean or settings.auto_clean

missing_setting = False
for arg, value in settings.__dict__.items():
  if value is None:
    print(f"ERR: {arg} must be provided.")
    missing_setting = True

if missing_setting: exit()