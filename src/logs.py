import logging
import sys
from src import settings


class CustomFormatter(logging.Formatter):
    purple = "\x1b[35;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = ':     %(name)s - %(message)s'  # type: ignore

    FORMATS = {
        logging.DEBUG: purple + "DBUG" + reset + str(format),
        logging.INFO: green + "INFO" + reset + str(format),
        logging.WARNING: yellow + "WARN" + reset + str(format),
        logging.ERROR: red + "EROR" + str(format) + reset,
        logging.CRITICAL: bold_red + "CRIT" + str(format) + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# FORMATTER = logging.Formatter('%(levelname)s:     %(name)s - %(message)s')


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter())
    return console_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_console_handler())
    logger.propagate = False
    return logger
