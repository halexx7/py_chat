'''
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных
из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
    a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных. 
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров 
«Изготовитель системы»,  «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить 
в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. 
В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить в него названия 
столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». 
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
    b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных 
через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
'''


import csv
import glob
import re


def get_data():
    os_prod_list, os_name_list, os_code_list, os_type_list, main_data = [], [], [], [], []
    dict_data = {
        'Изготовитель системы': os_prod_list,
        'Название ОС': os_name_list, 
        'Код продукта': os_code_list,
        'Тип системы': os_type_list
        }

    for file in glob.glob('lesson_2/data/*.txt'):
        with open(file, encoding='cp1251') as f:
            _temp_list = []
            _temp_header = []
            for line in f:
                for key, val in dict_data.items():
                    if re.search(key, line):
                        values = re.sub(r'\s+', ' ', re.split(r':', line)[1]).strip()
                        dict_data[key].append(values)
                        _temp_list.append(values)
                        _temp_header.append(key)
            if len(main_data) < 1:
                main_data.append(_temp_header)
            main_data.append(_temp_list)
    return main_data


def write_to_csv(path):
    data = get_data()
    with open(path, 'w') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

write_to_csv('lesson_2/res_data/main_data.csv')



'''
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. 
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), 
количество (quantity), цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись 
данных в виде словаря в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
'''

import json

def write_order_to_json(item, quantity, price, buyer, date):
    orders = {
        'товар': item,
        'количество': quantity,
        'цена': price,
        'покупатель': buyer,
        'дата': date
    }

    with open('lesson_2/res_data/orders.json') as f:
        data = json.load(f)

    data['orders'].append(dict(orders))

    with open('lesson_2/res_data/orders.json', 'w') as f:
        f.writelines(json.dumps(data, indent=4, ensure_ascii=False))

write_order_to_json("хлеб", 3, 50.48, "Петров Иван Иванович", "2020-04-20")
write_order_to_json("молоко", 2, 70.48, "Сидоров Алексей Петрович", "2020-04-21")
write_order_to_json("шоколад", 5, 150, "Сидоров Алексей Петрович", "2020-06-21")



'''
3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных 
в файле YAML-формата. Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, 
второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом,
отсутствующим в кодировке ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию 
файла с помощью параметра default_flow_style, а также установить возможность работы с юникодом: 
allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
'''

import yaml

data = {
    'some_list': [1, 'пятый', 'синий'],
    'some_int': 58,
    'some_dict': {'январь': '€100', 'февраль': '€150', 'март': '€200'},
}

with open('lesson_2/res_data/data.yaml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

with open('lesson_2/res_data/data.yaml') as f:
    print(f.read())
