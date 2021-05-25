import argparse
import sys
import select
from socket import AF_INET, SOCK_STREAM, socket

from settings.cfg_client_log import logger
from settings.utils import get_message, log, send_message
from settings.jim import pack, unpack
from settings.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, RESPONSE, USER, ENCODING


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


def read_requests(r, sock):
    """ Чтение запросов из списка клиентов
    """
    for s in sock:
        # if s == sock:
        data = unpack(s.recv(1024))
        if not data :
            print (f'\nDisconnected from chat server')
            sys.exit()
        else :
            #print data
            print(f'<{data["from"]}>: {data["message"]}')


def write_responses(alias, w, msg):
    """ Эхо-ответ сервера клиентам, от которых были запросы
    """
    for sock in w:
        try:
            msg = pack(message(alias, msg))
            sock.send(msg)
        except:  # Сокет недоступен, клиент отключился
            # print(f'Сервер {w.fileno()} {w.getpeername()} недоступен')
            sock.close()
            sys.exit()
    

def main(address):
    try:
        if not 1024 <= address.port <= 65535:
            raise ValueError
        logger.info(f"Connected to remote host - {address.addr}:{address.port} ")
    except ValueError:
        logger.critical("The port must be in the range 1024-6535")
        sys.exit(1)

    with socket(AF_INET, SOCK_STREAM) as sock:
        # Соединиться с сервером
        try :
            sock.connect((address.addr, address.port))
        except :
            print(f'Unable to connect')
            sys.exit()
           
        alias = input('Name: ')
        while True:
            sock_lst = [sock]

            # msg = input('Say: ')
            # if msg == 'exit':
            #     break

            r, w, e = select.select(sock_lst , sock_lst, [], 0)

            # write_responses(alias, w, msg)
            read_requests(r, sock_lst)



if __name__ == "__main__":
    parser = createParser()
    address = parser.parse_args()

    main(address)