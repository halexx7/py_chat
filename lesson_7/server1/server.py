import time
import select
from socket import socket, AF_INET, SOCK_STREAM

def new_listen_socket(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(5)
    sock.settimeout(0.2)
    return sock


def mainloop():
    address = ('', 8888)
    clients = []
    sock = new_listen_socket(address)

    while True:
        try:
            conn, addr = sock.accept()
        except OSError as e:
            pass
        else:
            print(f'Получен запрос на соединение с {addr}')
            clients.append(conn)
        finally:
            w = []
            try:
                r, w, e = select.select([], clients, [], 0)
            except Exception as e:
                pass

            for s_client in w:
                timestr = time.ctime(time.time()) + '\n'
                try:
                    s_client.send(timestr.encode('utf-8'))
                except:
                    print(f'Клиент отключился {s_client}')
                    clients.remove(s_client)


if __name__ =='__main__':
    print('Эхо сервер запщен!')
    mainloop()