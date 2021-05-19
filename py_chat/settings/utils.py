import inspect
import json
import sys

from py_chat.settings.jim import pack, unpack
from py_chat.settings.server_log_config import logger as cli_logger
from py_chat.settings.server_log_config import logger as srv_logger
from py_chat.settings.variables import ENCODING, MAX_PACKAGE_LENGTH

if sys.argv[0].find("client") == -1:
    logger = srv_logger
else:
    logger = cli_logger


def get_message(client):
    """
    Утилита приема и декодирования сообщения.
    Принимает байты и выдает словарь, если принято что - то другое отдает ошибку значения
    """
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        response = unpack(encoded_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(sock, message):
    """
    Утилита кодирования и отправки сообщения.
    Принимает словарь и отправляет его.
    """
    encoded_message = pack(message)
    sock.send(encoded_message)


def log(func):
    def wrapper(*args, **kwargs):
        logger.info(f'function name: "{func.__name__}", arguments: {args}, {kwargs}')
        r = func(*args, **kwargs)
        logger.info(f'Function "{func.__name__}" called from a function "{inspect.stack()[1][3]}"')
        return r

    return wrapper
