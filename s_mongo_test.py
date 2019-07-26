import pymongo, json, xlrd, sys, pprint
from datetime import datetime

loc = ("C:\\BackUp\\Docs\\Южное Кладбище\\Выгрузки\\ниж_1.xlsx") 
#loc = ("E:\Южное Кладбище\VGD\csv\Калязинский_рн.xlsx")

fx_rec = '''{{
    "from": {0},
    "id": {1},
    "Фамилия":"{2}",
    "Имя":"{3}",
    "Отчество":"{4}",
    "Дата рождения/Возраст":"{5}",
    "Место рождения":"{6}",
    "Дата и место призыва":"{7}",
    "Последнее место службы":"{8}",
    "Воинское звание":"{9}",
    "Причина выбытия":"{10}",
    "Дата выбытия":"{11}"
}}'''


start_time = datetime.now()
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 

#sys.exit(0)

obj = sheet.get_rows()
obj.__next__()
a_rec = [json.loads(fx_rec.format('"обд"', int(row[0].value), row[1].value, row[2].value, row[3].value, row[4].value, row[5].value, row[6].value, row[7].value,row[8].value, row[9].value, row[10].value)) for i, row in enumerate(obj) ]

for i,rec in enumerate(a_rec):
    #print(type(rec))
    print(rec['Фамилия'])


end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
'''
a_rec=[]
for i, row in enumerate(obj):
    print(int(row[0].value))
    a_rec.append(json.loads(fx_rec.format('"обд"', int(row[0].value), row[1].value, row[2].value, row[3].value, row[4].value, row[5].value, row[6].value, row[7].value,row[8].value, row[9].value, row[10].value)))
'''