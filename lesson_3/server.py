from socket import *
import pickle
import sys
import argparse


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--addr', type=str, default='')
    parser.add_argument('-p', '--port', type=int, default=7777)
    return parser


def receiver():
    while True:
        client, addr = srv_sock.accept()
        data = client.recv(1024)
        print(pickle.loads(data))
        response = {
            "response": 200,
            "alert":"ОК"
        }
        client.send(pickle.dumps(response))
        client.close()


if __name__ == "__main__":
    # socket
    srv_sock = socket(AF_INET, SOCK_STREAM)

    # bind
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    srv_sock.bind((namespace.addr, namespace.port))

    # listen    
    srv_sock.listen(5)
    print('Chat server started on port : ' + str(namespace.port))

    receiver()
