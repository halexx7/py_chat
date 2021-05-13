from socket import *
import pickle
import sys
import argparse

# socket
cli_sock = socket(AF_INET, SOCK_STREAM)

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('addr', nargs='+', default='')
    parser.add_argument ('port', nargs='?', default=7777)
    return parser


def presets_msg(account_name, password):
    msg = {
        "action": "authenticate",
        "time": "<unix timestamp>",
        "user": {
                "account_name": account_name,
                "password": password
        }
    }
    return msg


def send_msg(msg):
    msg_serialise = pickle.dumps(msg)
    print(msg_serialise)
    try:
        cli_sock.send(msg_serialise)
        return True
    except:
        return False

def cli_recv(bytes=1024):
    data = pickle.loads(cli_sock.recv(bytes))
    return data

def print_msg(data):
    print(f'Сообщение от сервера: {(data)}')


if __name__ == "__main__":

    # connect
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    cli_sock.connect((namespace.addr[0], namespace.port))     
    print('Connected to remote host...')

    name = "Maver1ck"
    pwd =  "Correct"

    msg = presets_msg(account_name=name, password=pwd)
    send_msg(msg)

    data = cli_recv(1024)
    print_msg(data)




