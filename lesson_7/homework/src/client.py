import argparse
import sys
import select
import json
from socket import AF_INET, SOCK_STREAM, socket

from settings.cfg_client_log import logger
from settings.utils import get_message, log, send_message
from settings.jim import pack, unpack
from settings.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, RESPONSE, USER, BUFFER_SIZE


@log
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("addr", nargs="?", type=str, default=DEFAULT_IP_ADDRESS)
    parser.add_argument("port", nargs="?", type=int, default=DEFAULT_PORT)
    return parser


@log
def process_ans(message):
    """Функция разбирает ответ сервера."""
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return "200 : OK"
        return f'400 : {message["error"]}'
    raise ValueError


@log
def presets_msg():
    """Функция формирует сообщение серверу"""
    msg = {
        "action": "presence",
        "time": "<unix timestamp>",
        "user": {"account_name": USER, "password": "Secret"},
    }
    return msg


@log
def message(alias, message):
    """Функция формирует сообщение"""
    msg = {
        "action": "msg",
        "time": "<unix timestamp>",
        "to": "#room_boom",
        "from": alias,
        "message": message
    }
    return msg


def main(address):
    try:
        if not 1024 <= address.port <= 65535:
            raise ValueError
        logger.info(f"Connected to remote host - {address.addr}:{address.port} ")
    except ValueError:
        logger.critical("The port must be in the range 1024-6535")
        sys.exit(1)
    else:
        with socket(AF_INET, SOCK_STREAM) as sock:
            # Соединиться с сервером
            try :
                sock.connect((address.addr, address.port))
            except :
                print(f'Unable to connect')
                sys.exit()
            else:
                alias = input('Name: ')
                msg = input('Say: ')
                if msg == 'exit':
                    sys.exit(1)
                send_message(sock, message(alias, msg))
                logger.info("Message send")

                while True:
                    try:
                        data = get_message(sock)
                        print(f'<{data["from"] if data["from"] != alias else "You"}>: {data["message"]}')
                        logger.info("The message is received")
                    except (ValueError, json.JSONDecodeError):
                        logger.error("Failed to decode server message.")

          
if __name__ == "__main__":
    parser = createParser()
    address = parser.parse_args()

    main(address)