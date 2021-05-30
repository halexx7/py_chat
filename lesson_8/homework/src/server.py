import argparse
import select
from threading import Thread
import pdb
import sys
from re import match
from socket import AF_INET, SOCK_STREAM, socket

from settings.cfg_server_log import logger
from settings.response import action_msg, action_probe, get_101
from settings.utils import get_message, log, send_message
from settings.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, INDENT, MAX_CONNECTIONS, TIMEOUT, WAIT


clients = []
nicknames = []
#TODO нужна ли комната all?
rooms = [{'room_name': '#all', 'clients': clients,'nicknames': nicknames}]


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


def read_requests(r_clients, all_clients):
    """ Чтение запросов из списка клиентов
    """
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}
    for sock in r_clients:
        try:
            data = get_message(sock)
            responses[sock] = data
        except:
            print(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
            logger.info(f'Client {sock.fileno()} {sock.getpeername()} DISCONNECTED')
            all_clients.remove(sock)
    return responses


def parsing_requests(requests):
    for request in requests.values():
        if request['action'] == 'msg':
            if match(r'#', request['to']):
                broadband(request)
            else:
                private_msg(request)


def private_msg(msg):
    for nick in nicknames:
        if nick == msg['to']:
            client = clients[nicknames.index(nick)]
            send_message(client, msg)


def room_msg(msg, room):
    pass


def broadband(msg, room):
    """Флудилка"""
    for client in clients:
        try:
            send_message(client, action_msg(msg["message"], msg["from"]))
            # client.send_me(pack(action_msg(msg["from"], msg["message"])))
        except:  # Сокет недоступен, клиент отключился
            print(f"Client {client.fileno()} {client.getpeername()} DISCONNECTED")
            client.close()
            clients.remove(client)



def get_room(room_name):
    for room in rooms:
        if room['room_name'] == room_name:
            return room
        else:
            #TODO Отправить сообщение клиенту о создании комнаты!
            room_new = {'room_name': room_name, 'clients': [],'nicknames': []}
            rooms.append(room_new)


def main(address):
    """Основной скрипт работы сервера"""

    sys.excepthook = my_except_hook  # Обрабатываем Ctr+C
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
        print(f"The server is RUNNING on the port: {address.port}")
    finally:
        while True:
            try:
                conn, addr = sock.accept()
            except OSError as e:
                pass  # timeout вышел
            else:
                print(f"Connected with {str(addr)}")
                logger.info(f"Connected with {str(addr)}")
                send_message(conn, action_probe())
                cli_probe = get_message(conn)
                nickname = cli_probe['user']['account_name']
                for room in rooms:
                    #TODO проверить try-except если не будет room_name
                    if not room['room_name'] == '#all':
                        continue
                    else:
                        nicknames.append(nickname)
                        clients.append(conn)
                        print(f'{nickname} joined!')
                        #TODO разобраться почему не работает, ругается на dumps???
                        msg = get_101('Connected server!')
                        send_message(conn, msg)
                        break
            finally:
                r = []
                w = []
                
                try:
                    r, w, e = select.select(clients, clients, [], WAIT)
                except:
                    pass  # Ничего не делать, если какой-то клиент отключился

                requests = read_requests(r, clients)  # Сохраним запросы клиентов
                if requests:
                    parsing_requests(requests)


if __name__ == "__main__":
    parser = createParser()
    address = parser.parse_args()

    main(address)
