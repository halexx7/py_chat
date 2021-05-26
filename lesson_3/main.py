import argparse

from src import client, server


def mainParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str, default="server")
    parser.add_argument("-p", "--port", type=int, default=7777)
    parser.add_argument("-a", "--addr", type=str, default="localhost")
    return parser


def start():
    parser = mainParser()
    namespace = parser.parse_args()
    return namespace


if __name__ == "__main__":
    what_run = start()
    if what_run.type == "server":
        server.main(what_run)
    elif what_run.type == "client":
        client.main(what_run)
