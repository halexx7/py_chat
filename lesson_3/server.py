from socket import *
import pickle
import sys
import argparse


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=7777)
    parser.add_argument('-a', '--addr', default='')
    return parser


def srv_recv():
    while True:
        client, addr = srv_sock.accept()
        try:
            data = client.recv(1024)
            print(pickle.loads(data))
            response = srv_response(True)
        except:
            response = srv_response(False)
        
        srv_send(response, client)
        client.close()


def srv_response(bool):
    if bool:
        response = {
            "response": 200,
            "alert":"ОК"
        }
    else:
        response = {
            "response": 400,
            "alert":"Not ОК"
        }
    return response


def srv_send(response, cli):
    data = pickle.dumps(response)
    try:
        cli.send(data)
        return True
    except:
        return False


if __name__ == "__main__":
    # socket
    srv_sock = socket(AF_INET, SOCK_STREAM)

    # bind
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    srv_sock.bind((namespace.addr, int(namespace.port)))

    # listen    
    srv_sock.listen(5)
    print('Chat server started on port : ' + str(namespace.port))

    srv_recv()
