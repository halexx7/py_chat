from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 8888))

while True:
    tm = s.recv(1024)
    print(f'Текущее время: {tm.decode("utf-8")}')