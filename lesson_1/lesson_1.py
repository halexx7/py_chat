'''
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание соответствующих переменных. 
Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode и также проверить тип и содержимое переменных.
'''

def check_and_print(arr):
    for word in arr:
        word_str = str(word)
        print(f'{type(word_str)} - {word_str}')


words = ['разработка', 'сокет', 'декоратор']
check_and_print(words)

# Конвертер - https://www.branah.com/unicode-converter
words_byt = [
    '\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0',
    '\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82',
    '\xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80',
    ]
check_and_print(words_byt)

# Terminal:
# <class 'str'> - разработка
# <class 'str'> - сокет
# <class 'str'> - декоратор
# <class 'str'> - ÑÐ°Ð·ÑÐ°Ð±Ð¾ÑÐºÐ°
# <class 'str'> - ÑÐ¾ÐºÐµÑ
# <class 'str'> - Ð´ÐµÐºÐ¾ÑÐ°ÑÐ¾Ñ



'''
2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
'''

words_2 = ['class', 'function', 'method']

for word in words_2:
    word_byt = bytes(word, 'utf-8')
    print(f'{type(word_byt)} - {word_byt} (length: {len(word_byt)})')

# Terminal:
# <class 'bytes'> - b'class' (length: 5)
# <class 'bytes'> - b'function' (length: 8)
# <class 'bytes'> - b'method' (length: 6)



'''
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
'''

word_1 = b'attribute'
word_2 = b'type'
word_3 = b'класс'
word_4 = b'функция'

# Кирилицу не дает записать в байтовый тип, поднимает исключение:
#  File "c:\Users\Asus\Documents\GitHub\py_desc\lesson_1\lesson_1.py", line 47
#    word_3 = b'класс'
#                          ^
# SyntaxError: bytes can only contain ASCII literal characters.



'''
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое и выполнить 
обратное преобразование(используя методы encode и decode).
'''

words_4 = ['разработка', 'администрирование', 'protocol', 'standard']

for word in words_4:
    word_byt = word.encode('utf-8')
    word_str = word_byt.decode('utf-8')
    print(f'{word_str} - {word_byt}')


# Terminal:
# разработка - b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0'
# администрирование - b'\xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5'
# protocol - b'protocol'



'''
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип на кириллице.
'''
import subprocess

def encoder(args):
    subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)

    for line in subproc_ping.stdout:
        line = line.decode('cp866').encode('utf-8')
        print(line.decode('utf-8'))

args_1 = ['ping', 'yandex.ru']
args_2 = ['ping', 'youtube.com']

encoder(args_1)
# Terminal:

# YANDEX:
# Обмен пакетами с yandex.ru [77.88.55.60] с 32 байтами данных:
# Ответ от 77.88.55.60: число байт=32 время=690мс TTL=240
# Ответ от 77.88.55.60: число байт=32 время=715мс TTL=240
# Ответ от 77.88.55.60: число байт=32 время=306мс TTL=240
# Ответ от 77.88.55.60: число байт=32 время=618мс TTL=240

# Статистика Ping для 77.88.55.60:
#     Пакетов: отправлено = 4, получено = 4, потеряно = 0
#     (0% потерь)
# Приблизительное время приема-передачи в мс:
#     Минимальное = 306мсек, Максимальное = 715 мсек, Среднее = 582 мсек


encoder(args_2)
# Terminal:

# YOUTUBE:
# Обмен пакетами с youtube.com [216.58.209.174] с 32 байтами данных:
# Ответ от 216.58.209.174: число байт=32 время=793мс TTL=109
# Ответ от 216.58.209.174: число байт=32 время=610мс TTL=109
# Ответ от 216.58.209.174: число байт=32 время=357мс TTL=109
# Ответ от 216.58.209.174: число байт=32 время=550мс TTL=109

# Статистика Ping для 216.58.209.174:
#     Пакетов: отправлено = 4, получено = 4, потеряно = 0
#     (0% потерь)
# Приблизительное время приема-передачи в мс:
#     Минимальное = 357мсек, Максимальное = 793 мсек, Среднее = 577 мсек



'''
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
'''

lines = ['сетевое программирование\n', 'сокет\n', 'декоратор\n']

with open('test_file.txt', 'w') as w_obj:
    w_obj.writelines(lines)


with open('test_file.txt') as r_obj:
    print(r_obj)
#Terminal:
#<_io.TextIOWrapper name='test_file.txt' mode='r' encoding='cp1251'>
#Следовательно => кодировка файла - cp1251


with open('test_file.txt', encoding='utf-8') as r_obj:
    print(r_obj.readlines())
# Terminal:
# Поднимается исключение:
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xf1 in position 0: invalid continuation byte


with open('test_file.txt', encoding='cp1251') as r_obj:
    print(r_obj.readlines())
# Terminal:
# Соответственно с правильной кодировкой, все выводится
# ['сетевое программирование\n', 'сокет\n', 'декоратор\n']

