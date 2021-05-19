import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger("app." + __name__)

logFormatter = logging.Formatter(
    "%(asctime)-5s - %(levelname)-5s %(module)-5s %(message)s", 
    datefmt="%Y-%m-%dT%H:%M:%S")

# Time rotation
logHandler = TimedRotatingFileHandler("log/app.log", when="d", interval=1, encoding="utf-8")
logHandler.setFormatter(logFormatter)
logger.addHandler(logHandler)

logger.setLevel(logging.INFO)
