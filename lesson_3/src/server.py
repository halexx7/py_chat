import argparse
import sys
from socket import AF_INET, SOCK_STREAM, socket

from settings.jim import pack
from settings.server_log_config import logger
from settings.utils import get_message
from settings.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_CONNECTIONS, RESPONSE


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("-a", "--addr", type=str, default=DEFAULT_IP_ADDRESS)
    return parser


def get_response(bool):
    if bool:
        return {RESPONSE: 200}
    return {RESPONSE: 400, "error": "Bad Request"}


def srv_send(response, cli):
    cli.send(pack(response))
    logger.info("Message send!")


def main(args):
    srv_sock = socket(AF_INET, SOCK_STREAM)

    try:
        if not 1024 <= args.port <= 65535:
            raise ValueError
    except ValueError:
        logger.critical("The port must be in the range 1024-6535")
        sys.exit(1)
    else:
        srv_sock.bind((args.addr, args.port))
        srv_sock.listen(MAX_CONNECTIONS)
        logger.info(f"Chat server started on port : {args.port}")

    while True:
        client, addr = srv_sock.accept()
        try:
            data = get_message(client)
            response = get_response(True)
            logger.info("ОК! The message is received.")
        except:
            response = get_response(False)
            logger.exception("This error message:")
            logger.error("NOT ОК! Something went wrong: " + str(error))
        srv_send(response, client)
        client.close()


if __name__ == "__main__":
    parser = createParser()
    args = parser.parse_args()

    main(args)
