from socket import *
from select import select
import sys
 

 
def echo_client(ADDRESS):
    # Начиная с Python 3.2 сокеты имеют протокол менеджера контекста
    # При выходе из оператора with сокет будет автоматически закрыт
    with socket(AF_INET, SOCK_STREAM) as sock: # Создать сокет TCP
        sock.connect(ADDRESS)   # Соединиться с сервером
        while True:
            msg = input('Ваше сообщение: ')
            if msg == 'exit':
                break
            sock.send(msg.encode('utf-8')) 	# Отправить!
            data = sock.recv(1024).decode('utf-8')
            print(f'Ответ: {data}')
 
if __name__ == '__main__':
    ADDRESS = ('localhost', 10000)
    echo_client(ADDRESS)