from pymongo import MongoClient
import pymongo, json, xlrd, sys, pprint

#loc = ("C:\\BackUp\\Docs\\Южное Кладбище\\Выгрузки\\ниж_1.xlsx") 
loc = ("E:\Южное Кладбище\VGD\csv\Калязинский_рн.xlsx")

client = MongoClient('35.193.230.58',
    username='felix', password='12345678', 
    authSource='test',authMechanism='SCRAM-SHA-1')

db = client['test']
collection_name = 'bulk'
print(db.list_collection_names())
if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)
#print(client.database_names())  
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


wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 

records = db.bulk
a_rec=[]
for i, row in enumerate(sheet.get_rows()):
    if(i>0):
        print(" {0} - {1}".format(i,row[1].value))
        rec = fx_rec.format('"обд"', 
        int(sheet.row(i)[0].value),
        sheet.row(i)[1].value,
        sheet.row(i)[2].value,
        sheet.row(i)[3].value,
        sheet.row(i)[4].value,
        sheet.row(i)[5].value,
        sheet.row(i)[6].value,
        sheet.row(i)[7].value,
        sheet.row(i)[8].value,
        sheet.row(i)[9].value,
        sheet.row(i)[10].value       
        )

        a_rec.append(json.loads(rec))

#pprint.pprint(a_rec)
try:
    records.insert_many(a_rec, ordered=False)
except pymongo.errors.BulkWriteError as e:
    print(e.details['writeErrors'])

sys.exit(0)

for i in range(1,sheet.nrows):
#for i in range(1,6):
    #print(sheet.row(i)[0].value)
    try:
        rec = fx_rec.format('"обд"', 
        int(sheet.row(i)[0].value),
        sheet.row(i)[1].value,
        sheet.row(i)[2].value,
        sheet.row(i)[3].value,
        sheet.row(i)[4].value,
        sheet.row(i)[5].value,
        sheet.row(i)[6].value,
        sheet.row(i)[7].value,
        sheet.row(i)[8].value,
        sheet.row(i)[9].value,
        sheet.row(i)[10].value       
        )
        #print(rec)
        #records.insert_one(json.loads(rec, strict=False))
        
    except pymongo.errors.DuplicateKeyError:
        print("DuplicateKeyError")
    except Exception as ex: 
        template = "Тип ошибки {0} \nArguments:{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
