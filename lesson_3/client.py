import argparse
import pickle
import sys
from socket import *

# socket
cli_sock = socket(AF_INET, SOCK_STREAM)


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("addr", nargs="?", type=str, default="localhost")
    parser.add_argument("port", nargs="?", type=int, default=7777)
    return parser


def presets_msg():
    msg = {
        "action": "authenticate",
        "time": "<unix timestamp>",
        "user": {"account_name": "Dave", "password": "Secret"},
    }
    msg_serialise = pickle.dumps(msg)
    return msg_serialise


def send_msg(msg):
    cli_sock.send(msg)


def cli_recv():
    data = cli_sock.recv(1024)
    return data


def loads_srv_msg(data):
    msg = pickle.loads(data)
    return msg


def print_msg(data):
    print(f"Server message: {(data)}")


# connect
parser = createParser()
namespace = parser.parse_args()
cli_sock.connect((namespace.addr, namespace.port))
print("Connected to remote host...")

msg = presets_msg()
send_msg(msg)

data = cli_recv()
print_msg(loads_srv_msg(data))

