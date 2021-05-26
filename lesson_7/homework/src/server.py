import argparse
import select
import sys
from socket import AF_INET, SOCK_STREAM, socket

from settings.cfg_server_log import logger
from settings.jim import pack, unpack
from settings.utils import get_message, log
from settings.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, INDENT, MAX_CONNECTIONS, TIMEOUT, WAIT


@log
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("-a", "--addr", type=str, default=DEFAULT_IP_ADDRESS)
    return parser


def my_except_hook(exctype, value, traceback):
    """Выводим человекочитаемый 'Server STOP', при нажатии CTR + C"""

    if exctype == KeyboardInterrupt:
        print(f"{INDENT}\n\tServer STOP!\n{INDENT}")
    else:
        sys.__excepthook__(exctype, value, traceback)


@log
def read_requests(r_clients, all_clients):
    """Чтение запросов из списка клиентов"""

    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = unpack(sock.recv(1024))
            responses[sock] = data
        except:
            print(f"Client {sock.fileno()} {sock.getpeername()} DISCONNECTED")
            logger.info(f"Client {sock.fileno()} {sock.getpeername()} DISCONNECTED")
            all_clients.remove(sock)

    return responses


@log
def broadband(requests, all_clients):
    """Флудилка"""

    for sock in all_clients:
        for val in requests.values():
            if val["to"] == "#room_boom":
                try:
                    sock.send(pack(message(val["from"], val["message"])))
                except:  # Сокет недоступен, клиент отключился
                    print(f"Client {sock.fileno()} {sock.getpeername()} DISCONNECTED")
                    logger.info(f"Client {sock.fileno()} {sock.getpeername()} DISCONNECTED")
                    sock.close()
                    all_clients.remove(sock)


@log
def message(alias, message):
    """Функция формирует сообщение"""
    msg = {"action": "msg", "time": "<unix timestamp>", "to": "#room_boom", "from": alias, "message": message}
    return msg


def main(address):
    """Основной скрипт работы сервера"""

    sys.excepthook = my_except_hook  # Обрабатываем Ctr+C

    sock = socket(AF_INET, SOCK_STREAM)
    clients = []

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

    finally:
        while True:
            try:
                conn, addr = sock.accept()
            except OSError as e:
                pass  # timeout вышел

            else:
                print(f"Client {str(addr)} CONNECTED")
                logger.info(f"Client {str(addr)} CONNECTED")
                clients.append(conn)

            finally:
                r = []
                w = []
                try:
                    r, w, e = select.select(clients, clients, [], WAIT)
                except:
                    pass  # Ничего не делать, если какой-то клиент отключился

                requests = read_requests(r, clients)  # Сохраним запросы клиентов
                if requests:
                    broadband(requests, clients)  # Флудим


if __name__ == "__main__":
    parser = createParser()
    address = parser.parse_args()

    main(address)
