import argparse
import sys
import select
from socket import socket, AF_INET, SOCK_STREAM

from settings.jim import pack, unpack
from settings.cfg_server_log import logger
from settings.utils import get_message, log
from settings.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_CONNECTIONS, RESPONSE, TIMEOUT, ENCODING


@log
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("-a", "--addr", type=str, default=DEFAULT_IP_ADDRESS)
    return parser


def read_requests(r_clients, all_clients):
    """ Чтение запросов из списка клиентов
    """
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = unpack(sock.recv(1024))
            responses[sock] = data
        except:
            print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
            all_clients.remove(sock)

    return responses


def write_responses(requests, w_clients, all_clients):
    """ Эхо-ответ сервера клиентам, от которых были запросы
    """

    for sock in w_clients:
        # if sock in requests:
        try:
            # Подготовить и отправить ответ сервера
            resp = {'sock':sock.getpeername(), 'msg':requests[sock]}
            # Эхо-ответ сделаем чуть непохожим на оригинал
            sock.send(pack(resp))
        except:  # Сокет недоступен, клиент отключился
            print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
            sock.close()
            all_clients.remove(sock)
    

def write_responses_all(requests, all_clients):
    """ Пересылка сообщений
    """
    for sock in all_clients:
        for val in requests.values():
            if val['to'] == '#room_boom':
                try:
                    # print(message(val['from'], val['message']))
                    sock.send(pack(message(val['from'], val['message'])))
                except:  # Сокет недоступен, клиент отключился
                    print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
                    sock.close()
                    all_clients.remove(sock)


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


@log
def main(address):
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
        logger.info(f"Сервер запущен на порту: {address.port}")

    while True:
        try:
            conn, addr = sock.accept()  # Проверка подключений
        except OSError as e:
            pass  # timeout вышел
        else:
            print(f"Клиент {str(addr)} подключился")
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
                # write_responses(requests, w, clients)  # Выполним отправку ответов клиентам
                write_responses_all(requests, clients)


if __name__ == "__main__":
    parser = createParser()
    address = parser.parse_args()

    main(address)