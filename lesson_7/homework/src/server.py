import argparse
import sys
import select
from socket import socket, AF_INET, SOCK_STREAM

from settings.jim import pack, unpack
from settings.cfg_server_log import logger
from settings.utils import get_message, log, my_except_hook
from settings.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_CONNECTIONS, TIMEOUT


@log
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("-a", "--addr", type=str, default=DEFAULT_IP_ADDRESS)
    return parser


@log
def read_requests(r_clients, all_clients):
    """ Чтение запросов из списка клиентов
    """
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = unpack(sock.recv(1024))
            responses[sock] = data
        except:
            print(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
            logger.info(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
            all_clients.remove(sock)

    return responses


@log
def write_responses(requests, w_clients, all_clients):
    """ Эхо-ответ сервера клиентам, от которых были запросы
    """

    for sock in w_clients:
        if sock in requests:
            try:
                resp = {'sock':sock.getpeername(), 'msg':requests[sock]}
                sock.send(pack(resp))
            except:  # Сокет недоступен, клиент отключился
                print(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
                logger.info(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
                sock.close()
                all_clients.remove(sock)


@log
def write_responses_all(requests, all_clients):
    """ Флудилка
    """
    for sock in all_clients:
        for val in requests.values():
            if val['to'] == '#room_boom':
                try:
                    sock.send(pack(message(val['from'], val['message'])))
                except:  # Сокет недоступен, клиент отключился
                    print(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
                    logger.info(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
                    sock.close()
                    all_clients.remove(sock)


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
    """ Основной скрипт работы сервера"""

    sys.excepthook = my_except_hook # Обрабатываем Ctr+C

    clients = []

    sock = socket(AF_INET, SOCK_STREAM)

    try:
        if not 1024 <= address.port <= 65535:
            raise ValueError
    except ValueError:
        logger.critical("The port must be in the range 1024-6535")
        sys.exit(1)
    else:
        sock.bind((address.addr, address.port))
        sock.listen(MAX_CONNECTIONS)
        sock.settimeout(TIMEOUT)
        logger.info(f"The server is RUNNING on the port: {address.port}")

    while True:
        try:
            conn, addr = sock.accept()  # Проверка подключений
        except OSError as e:
            pass  # timeout вышел
        else:
            print(f"Client {str(addr)} CONNECTED")
            logger.info(f"Client {str(addr)} CONNECTED")
            clients.append(conn)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 10
            r = []
            w = []
            e = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass  # Ничего не делать, если какой-то клиент отключился

            requests = read_requests(r, clients)  # Сохраним запросы клиентов
            if requests:
                write_responses_all(requests, clients)


if __name__ == "__main__":
    parser = createParser()
    address = parser.parse_args()

    main(address)