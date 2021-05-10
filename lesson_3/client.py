from socket import *
import pickle
import sys
import argparse

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', nargs='+', type=str, default='')
    parser.add_argument('port', nargs='?', type=int, default=7777)
    return parser


def presets_msg():
    msg = {
        "action": "authenticate",
        "time": "<unix timestamp>",
        "user": {
                "account_name": "Maver1ck",
                "password":     "CorrectHorseBatterStaple"
        }
    }
    cli_sock.send(pickle.dumps(msg))
    data = cli_sock.recv(1024)
    print(f'Сообщение от сервера: {pickle.loads(data)}')


if __name__ == "__main__":
    # socket
    cli_sock = socket(AF_INET, SOCK_STREAM)


    # connect
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    cli_sock.connect((namespace.addr[0], namespace.port))     
    print('Connected to remote host...')

    presets_msg()