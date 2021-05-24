import argparse
import pickle
import sys
from socket import AF_INET, SOCK_STREAM, socket

from log.log_utilities import log
from log.server_log_config import logger


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=7777)
    parser.add_argument("-a", "--addr", type=str, default="localhost")
    return parser


@log
def srv_recv():
    while True:
        client, addr = srv_sock.accept()

        try:
            data = client.recv(1024)
            response = srv_response(True)
            logger.info("ОК! The message is received.")
        except:
            response = srv_response(False)
            logger.exception("This error message:")
            logger.error("NOT ОК! Something went wrong: " + str(error))

        srv_send(response, client)
        client.close()


@log
def srv_response(bool):
    if bool:
        response = {"response": 200, "alert": "OK"}
    else:
        response = {"response": 400, "alert": "Not OK"}
    return response


@log
def srv_send(response, cli):
    data = pickle.dumps(response)
    cli.send(data)
    logger.info("Message send")


if __name__ == "__main__":

    # socket
    srv_sock = socket(AF_INET, SOCK_STREAM)

    # bind
    parser = createParser()
    namespace = parser.parse_args()

    try:
        if not 1024 <= namespace.port <= 65535:
            raise ValueError
        srv_sock.bind((namespace.addr, int(namespace.port)))
        # listen
        srv_sock.listen(5)
        logger.info(f"Chat server started on port : {int(namespace.port)}")
    except ValueError:
        logger.critical("The port must be in the range 1024-6535")
        sys.exit(1)

    srv_recv()
