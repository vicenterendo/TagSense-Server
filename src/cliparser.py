import argparse
from typing import Optional

from pydantic import BaseModel, IPvAnyAddress, Field, UrlConstraints

parser = argparse.ArgumentParser("TagSense Server",
                                 epilog="Environment variables are recommended. For more info consult "
                                        "https://github.com/vicenterendo/TagSense-Server")


class CLIParser(BaseModel):
    hostname: Optional[str] = None
    port: Optional[int] = Field(gt=0, lt=65536)
    database_url: Optional[str] = UrlConstraints(allowed_schemes=[  # type: ignore
        "mysql",
        "mysql+mysqlconnector",
        "mysql+aiomysql",
        "mysql+asyncmy",
        "mysql+mysqldb",
        "mysql+pymysql",
        "mysql+cymysql",
        "mysql+pyodbc",
        "sqlite"
    ],
        default_port=3306)
    airport_prefix: Optional[str] = Field(max_length=4)
    require_squawk: Optional[bool] = None
    auto_clean: Optional[bool] = None
    max_age: Optional[str] = Field(gt=-1)
    validate_store: Optional[bool] = None
    db_max_attempts: Optional[int] = None
    ignore_arrived: Optional[bool] = None
    cors: Optional[list[str]] = None
    hide_attributes: Optional[list[str]] = None


parser.add_argument("-a", "--addr", "--hostname",
                    dest="hostname", metavar="ADDR")
parser.add_argument("-p", "--port", dest="port", type=int)
parser.add_argument("-db", "--database-url", dest="database_url")
parser.add_argument("-prfx", "--airport-prefix", dest="airport_prefix")
parser.add_argument("-sqwk", "--require-squawk",
                    action='store_true', dest="require_squawk")
parser.add_argument("-c", "--auto-clean",
                    dest="auto_clean", action='store_true')
parser.add_argument("-ma", "--max-age", dest="max_age",
                    metavar="SECONDS", type=int)
parser.add_argument("--validate-store",
                    dest="validate_store", action="store_true")
parser.add_argument("--db-max-attempts",
                    dest="db_max_attempts", metavar="ATTEMPTS", type=int)
parser.add_argument("--ignore-arrived",
                    dest="ignore_arrived", action="store_true")
parser.add_argument('-crs', "--cors", nargs='+', dest="cors")
parser.add_argument('--hide-attributes', nargs='+', dest="hide_attributes")

args = parser.parse_args()

parsed_arguments = CLIParser(**vars(parser.parse_args()))
