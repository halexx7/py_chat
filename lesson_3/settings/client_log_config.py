import logging

from settings.variables import ENCODING, LOG_FILENAME, LOGGER_NAME

FILE_LOG_LVL = logging.INFO

client_formatter = logging.Formatter(
    f"%(asctime)-5s - %(levelname)-5s | %(module)-5s | %(message)s", datefmt="%Y-%m-%dT%H:%M:%S"
)

logHandler = logging.FileHandler(LOG_FILENAME, encoding=ENCODING)
logHandler.setFormatter(client_formatter)

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(FILE_LOG_LVL)
