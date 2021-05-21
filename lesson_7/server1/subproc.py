from subprocess import Popen
import os

p_list = []

while True:
    user = input('Запустить 10 клиентов (s) / Закрыть клиентов (x) / Выйти (q)')

    if user == 'q':
        break
    elif user == 's':
        for _ in range(10):
            p_list.append(Popen('python3 client.py', shell=True))

        print('Запущено 10 клиентов')
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()