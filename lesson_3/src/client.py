import argparse
import json
import sys
from socket import AF_INET, SOCK_STREAM, socket

from settings.client_log_config import logger
from settings.utils import get_message, send_message
from settings.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, RESPONSE, USER


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("addr", nargs="?", type=str, default=DEFAULT_IP_ADDRESS)
    parser.add_argument("port", nargs="?", type=int, default=DEFAULT_PORT)
    return parser


def process_ans(message):
    """Функция разбирает ответ сервера."""
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return "200 : OK"
        return f'400 : {message["error"]}'
    raise ValueError


def presets_msg():
    """Функция формирует сообщение серверу"""
    msg = {
        "action": "presence",
        "time": "<unix timestamp>",
        "user": {"account_name": USER, "password": "Secret"},
    }
    return msg


def print_msg(data):
    """Функция печатает сообщение"""
    print(f"Server message: {(data)}")
    logger.info(f"Server message: {(data)}")


def main(namespace):
    try:
        if not 1024 <= namespace.port <= 65535:
            raise ValueError
        logger.info(f"Connected to remote host - {namespace.addr}:{namespace.port} ")
    except ValueError:
        logger.critical("The port must be in the range 1024-6535")
        sys.exit(1)

    cli_sock = socket(AF_INET, SOCK_STREAM)
    cli_sock.connect((namespace.addr, namespace.port))
    msg = presets_msg()

    send_message(cli_sock, msg)
    logger.info("Message send")

    try:
        answer = process_ans(get_message(cli_sock))
    except (ValueError, json.JSONDecodeError):
        logger.error("Failed to decode server message.")

    logger.info("The message is received")
    print_msg(answer)


if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args()

    main(namespace)
