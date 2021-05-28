import argparse
import sys
from threading import Thread
from socket import AF_INET, SOCK_STREAM, socket

from settings.messages import action_msg
from settings.cfg_client_log import logger
from settings.utils import get_message, log, send_message
from settings.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, INDENT, RESPONSE, USER


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



def main(address):
    """Основной скрипт работы клиента"""

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
            # Соединиться с сервером
            try:
                sock.connect((address.addr, address.port))

            except:
                print(f"Unable to connect")
                sys.exit()

            else:
                alias = input("Name: ")

                listen_server = Thread(target=get_message, args=(sock, alias))
                listen_server.daemon = True
                listen_server.start()
                
                while 1:
                    msg = input("Say: ")
                    if msg == "exit":
                        sys.exit(1)

                    send_message(sock, action_msg(alias, msg))
                    logger.info("Message send")

                # while True:
                #     try:
                #         data = get_message(sock)
                #         print(f'<{data["from"] if data["from"] != alias else "You"}>: {data["message"]}')
                #         logger.info("The message is received")

                #     except (ValueError, json.JSONDecodeError):
                #         logger.error("Failed to decode server message.")


if __name__ == "__main__":
    parser = createParser()
    address = parser.parse_args()

    main(address)
