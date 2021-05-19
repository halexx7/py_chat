import logging

logger = logging.getLogger("app." + __name__)

logFormatter = logging.Formatter(
    "%(asctime)-5s - %(levelname)-5s %(module)-5s %(message)s", datefmt="%Y-%m-%dT%H:%M:%S"
)

logHandler = logging.FileHandler("log/app.log", encoding="utf-8")
logHandler.setFormatter(logFormatter)
logger.addHandler(logHandler)

logger.setLevel(logging.INFO)
