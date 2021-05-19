import logging
import os
from logging.handlers import TimedRotatingFileHandler

from py_chat.settings.variables import ENCODING, LOGGER_NAME

ROOT = os.getcwd()
DIR_LOG = "logs"

FILE_LOG_LVL = logging.INFO

LOG_DIRECTORY = os.path.join(ROOT, DIR_LOG)
LOG_FILENAME = f"app.log"

if not os.path.exists(LOG_DIRECTORY):
    os.mkdir(LOG_DIRECTORY)

BACKUP_COUNT = 5
WHEN_INTERVAL = "D"

server_formatter = logging.Formatter(
    f"%(asctime)-5s - %(levelname)-5s %(module)-5s %(message)s", datefmt="%Y-%m-%dT%H:%M:%S"
)

logHandler = TimedRotatingFileHandler(LOG_DIRECTORY, when=WHEN_INTERVAL, interval=1, encoding=ENCODING)
logHandler.setFormatter(server_formatter)

logger = logging.getLogger(LOGGER_NAME)
logger.addHandler(logHandler)
logger.setLevel(FILE_LOG_LVL)
