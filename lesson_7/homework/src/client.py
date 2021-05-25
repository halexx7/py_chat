import argparse
import json
import sys
from socket import AF_INET, SOCK_STREAM, socket

from settings.cfg_client_log import logger
from settings.utils import get_message, log, send_message
from settings.jim import unpack
from settings.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, RESPONSE, USER, ENCODING


@log
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
    logger.info(f"Server message: {(data)}")
    

def main(address):
    try:
        if not 1024 <= address.port <= 65535:
            raise ValueError
        logger.info(f"Connected to remote host - {address.addr}:{address.port} ")
    except ValueError:
        logger.critical("The port must be in the range 1024-6535")
        sys.exit(1)

    with socket(AF_INET, SOCK_STREAM) as sock: # Создать сокет TCP
        sock.connect((address.addr, address.port))   # Соединиться с сервером
        while True:
            msg = input('Ваше сообщение: ')
            if msg == 'exit':
                break
            sock.send(msg.encode(ENCODING)) 	# Отправить!
            data = unpack(sock.recv(1024))
            print(f'Ответ: {data}')


if __name__ == "__main__":
    parser = createParser()
    address = parser.parse_args()

    main(address)