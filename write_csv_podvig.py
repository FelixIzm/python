#!/usr/bin/python3
import csv,json
import sqlite3
#conn = sqlite3.connect("./db/all_fields.db") # или :memory: чтобы сохранить в RAM
conn = sqlite3.connect("e:/temp/db/all_fields.db") # или :memory: чтобы сохранить в RAM

#csvfile = open('./csv/data.csv', 'w', newline='')
csvfile = open('e:/temp/db/data.csv', 'w', newline='')

csv_columns = ['id','Фамилия']
csv_columns.append('Имя')
csv_columns.append('Отчество')
csv_columns.append('Год рождения')
csv_columns.append('Звание')
csv_columns.append('В РККА с')
csv_columns.append('Место призыва')
csv_columns.append('Место рождения')
csv_columns.append('Ссылка на запись')

writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()

cursor = conn.cursor()
count=1
cursor.execute("SELECT count(1) FROM search_ids where flag=1")
count_row = cursor.fetchone()[0]
cursor.execute("SELECT * FROM search_ids WHERE flag=1")
for i in cursor.fetchall():
    try:
        obj_json = json.loads(i[2].replace("'",'"'))
        obj_json['Ссылка на запись'] = 'http://podvignaroda.ru/?#id={}&tab=navDetailManCard'.format(obj_json['id'])
        writer.writerow(obj_json)
    except:
        print(i[2])
        raise ValueError('Ошибка записи строки')

    print ('{} из {}'.format(count,count_row))
    count+=1



