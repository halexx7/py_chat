import argparse
import sys
from threading import Thread
from socket import AF_INET, SOCK_STREAM, socket

from settings.messages import action_msg, action_presence, action_auth, action_msg, action_join, action_leave, action_quit
from settings.cfg_client_log import logger
from settings.utils import get_message, log, send_message
from settings.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, INDENT, RESPONSE


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("addr", nargs="?", type=str, default=DEFAULT_IP_ADDRESS)
    parser.add_argument("port", nargs="?", type=int, default=DEFAULT_PORT)
    return parser


def my_except_hook(exctype, value, traceback):
    """Выводим человекочитаемый 'Disconnect from the server!', при нажатии CTR + C"""

    if exctype == KeyboardInterrupt:
        print(f"{INDENT}\n  Disconnect from the server  \n{INDENT}")
    else:
        sys.__excepthook__(exctype, value, traceback)


def process_ans(message):
    """Функция разбирает ответ сервера."""
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return "200 : OK"
        return f'400 : {message["error"]}'
    raise ValueError


def receive(client, nickname):
    while True:   
        # try:
        message = get_message(client)
        print(message)
        if message['action'] == 'probe':
            send_message(client, action_presence(nickname))
        else:
            print(message['message'])
        # except:                                                 #case on wrong ip/port details
        #     print("An error occured!")
        #     client.close()
        #     break


def write(client, nickname):
    while True:                                                 #message layout
        message = f"{nickname}: {input('')}"
        send_message(client, message)


def main(address):
    """Основной скрипт работы клиента"""

    nickname = input("Choose your nickname: ")

    sys.excepthook = my_except_hook  # Обрабатываем Ctr+C
    try:
        if not 1024 <= address.port <= 65535:
            raise ValueError
        logger.info(f"Connected to remote host - {address.addr}:{address.port} ")
    except ValueError:
        logger.critical("The port must be in the range 1024-6535")
        sys.exit(1)
    else:
        with socket(AF_INET, SOCK_STREAM) as sock:
            try:
                sock.connect((address.addr, address.port))
            except:
                print(f"Unable to connect")
                sys.exit()
            else:
                receive_thread = Thread(target=receive, args=(sock, nickname))               #receiving multiple messages
                receive_thread.start()
                write_thread = Thread(target=write, args=(sock, nickname))                   #sending messages 
                write_thread.start()
                

if __name__ == "__main__":
    parser = createParser()
    address = parser.parse_args()
    
    main(address)
