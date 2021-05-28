import argparse
import select
from threading import Thread
import sys
from socket import AF_INET, SOCK_STREAM, socket

from settings.cfg_server_log import logger
from settings.response import action_msg, action_probe
from settings.jim import pack, unpack
from settings.utils import get_message, log, send_messages
from settings.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, INDENT, MAX_CONNECTIONS, TIMEOUT, WAIT


rooms = [{'room_name': '#all', 'clients': [],'nicknames': []}]


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


def handle(rooms):
    """Чтение запросов из списка клиентов"""
    while True:
        try:                                                            #recieving valid messages from client
            message = client.recv(1024)
            broadcast(message)
        except:                                                         #removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

    return responses


def broadband(msg, clients):
    """Флудилка"""
    for client in clients:
        for val in msg.values():
            if val["to"] == "#all":
                try:
                    client.send(pack(action_msg(val["from"], val["message"])))
                except:  # Сокет недоступен, клиент отключился
                    print(f"Client {client.fileno()} {client.getpeername()} DISCONNECTED")
                    client.close()
                    clients.remove(client)



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
    finally:
        while True:
            try:
                conn, addr = sock.accept()
            except OSError as e:
                pass  # timeout вышел
            else:
                print(f"Connected with {str(addr)}")
                logger.info(f"Connected with {str(addr)}")
                send_messages(conn, action_probe())
                cli_probe = get_message(conn)
                nickname = cli_probe['user']['account_name']
                for room in rooms:
                    #TODO проверить try-except если не будет room_name
                    if not room['room_name'] == '#all':
                        continue
                    else:
                        room['nicknames'].append(nickname)
                        room['clients'].append(conn)
                        print(f"Nickname is {nickname}")
                        broadband(action_msg(f'{nickname} joined!', room['clients']))
                        send_messages(action_msg(f'Connected to server!'))
                        thread = Thread(target=handle, args=(rooms,))
                        thread.start()
                        break



            # finally:
            #     r = []
            #     w = []
            #     try:
            #         r, w, e = select.select(clients, clients, [], WAIT)
            #     except:
            #         pass  # Ничего не делать, если какой-то клиент отключился

            #     requests = read_requests(r, clients)  # Сохраним запросы клиентов
            #     if requests:
            #         broadband(requests, clients)  # Флудим


if __name__ == "__main__":
    parser = createParser()
    address = parser.parse_args()

    main(address)
