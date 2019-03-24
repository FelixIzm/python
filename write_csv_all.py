import csv,json
import sqlite3
conn = sqlite3.connect("../doc/all_fields.db") # или :memory: чтобы сохранить в RAM

########################################################
fio = 'литвинов'
########################################################
csvfile = open(fio+'.csv', 'w', newline='')
csv_columns = ['ID','Фамилия']
csv_columns.append('Имя')
csv_columns.append('Отчество')
csv_columns.append('Дата рождения/Возраст')
csv_columns.append('Место рождения')
csv_columns.append('Дата и место призыва')
csv_columns.append('Последнее место службы')
csv_columns.append('Воинское звание')
csv_columns.append('Причина выбытия')
csv_columns.append('Дата выбытия')
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()


cursor = conn.cursor()
count=1
cursor.execute("SELECT count(1) FROM search_ids where flag=1")
count_row = cursor.fetchone()[0]
cursor.execute("SELECT * FROM search_ids WHERE flag=1")
for i in cursor.fetchall():
    try:
        writer.writerow(json.loads(i[2].replace("'",'"')))
    except:
        print(i[2])
        raise ValueError('Не определилось число страниц')

    print ('{} из {}'.format(count,count_row))
    count+=1
