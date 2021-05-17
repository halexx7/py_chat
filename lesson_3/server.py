import argparse
import pickle
import sys
from socket import socket, AF_INET, SOCK_STREAM

from log.server_log_config import logger


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=7777)
    parser.add_argument("-a", "--addr", default="")
    return parser


def srv_recv():
    while True:
        client, addr = srv_sock.accept()
        
        try:
            data = client.recv(1024)
            response = srv_response(True)
            logger.info('ОК! The message is received.')
        except:
            response = srv_response(False)
            logger.exception('Это сообщение об ошибке:')
            logger.error('NOT ОК! Something went wrong: ' + str(error))

        srv_send(response, client)
        client.close()


def srv_response(bool):
    if bool:
        response = {"response": 200, "alert": "ОК"}
    else:
        response = {"response": 400, "alert": "Not ОК"}
    return response


def srv_send(response, cli):
    data = pickle.dumps(response)
    cli.send(data)
    logger.info('Message send')


if __name__ == "__main__":

    # socket
    srv_sock = socket(AF_INET, SOCK_STREAM)

    # bind
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    srv_sock.bind((namespace.addr, int(namespace.port)))

    # listen
    srv_sock.listen(5)
    logger.info(f'Chat server started on port : {int(namespace.port)}')

    srv_recv()


