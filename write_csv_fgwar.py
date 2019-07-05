#!/usr/bin/python3
import csv,json
import sqlite3
conn = sqlite3.connect("./db/data.db") # или :memory: чтобы сохранить в RAM
#conn = sqlite3.connect("e:/temp/vpp/db/gwar.db") # или :memory: чтобы сохранить в RAM

csvfile = open('./csv/data.csv', 'w', newline='')
#csvfile = open('e:/temp/vpp/csv/data.csv', 'w', newline='')

csv_columns = ['Фамилия']
csv_columns.append('Имя')
csv_columns.append('Отчество')
csv_columns.append('Дата рождения')
csv_columns.append('Должность/Звание')
csv_columns.append('Воинская часть')
csv_columns.append('Губерния')
csv_columns.append('Уезд')
csv_columns.append('Волость')
csv_columns.append('Причина выбытия')
csv_columns.append('Дата события')
csv_columns.append('Место события')
csv_columns.append('Тип документа')
csv_columns.append('Архив')
csv_columns.append('Дело')
csv_columns.append('Ссылка на запись')

writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()
cursor = conn.cursor()
count=1
cursor.execute("SELECT count(1) FROM data")
count_row = cursor.fetchone()[0]
cursor.execute("SELECT * FROM data")
for i in cursor.fetchall():
    json.loads(i[1].replace("'",'"'))
    csv_str=''
    for y,element in enumerate(eval(i[1])):
        csv_str+='"'+csv_columns[y]+'":"'+element+'",'
    csv_str="{"+csv_str[:-1]+"}"
    print(csv_str)

    try:
        writer.writerow(json.loads(csv_str))
    except:
        print(csv_str)
        raise ValueError('Ошибка записи строки')

    print ('{} из {}'.format(count,count_row))
    count+=1

