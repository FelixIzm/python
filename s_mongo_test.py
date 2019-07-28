from pymongo import MongoClient
import pymongo, json, xlrd, sys, pprint
from datetime import datetime
from os import listdir
from os.path import isfile, join


client = MongoClient('35.193.230.58',
    username='felix', password='12345678', 
    authSource='test',authMechanism='SCRAM-SHA-1')

db = client['test']
collection_name = 'short_field'
if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)
records = db[collection_name]
count_doc_start = records.count_documents({})

file_names = 'files'
if file_names not in db.list_collection_names():
    db.create_collection(file_names)
file_names_collection = db[file_names]

#loc = ("E:\\Temp\\obd\\москворецкий_рвк.xlsx") 

fx_rec = '''{{"f0": {0},"f1": {1},"f2":"{2}","f3":"{3}","f4":"{4}","f5":"{5}","f6":"{6}","f7":"{7}","f8":"{8}","f9":"{9}","f10":"{10}","f11":"{11}"}}'''

# Собираем названия файлов для обработки
mypath="E:\\Temp\\obd\\"
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath, f))]

def write_json(floc):
    global mypath
    #Открываем ексель
    start_time = datetime.now()
    wb = xlrd.open_workbook(join(mypath,floc)) 
    if wb.nsheets> 1:
        print(floc)
        for sheet in wb.sheets():
            print('\tимя={0} строк {1}'.format(sheet.name,sheet.nrows))

    wb.release_resources()
    del wb
    return
    sheet = wb.sheet_by_index(0) 
    obj = sheet.get_rows()
    obj.__next__()
    # Собираем данные из таблицы в json
    a_rec=[]
    for i, row in enumerate(obj):
        try:
            a_rec.append(json.loads(fx_rec.format('"обд"', int(row[0].value), row[1].value, row[2].value, row[3].value, row[4].value, str(row[5].value).replace('"','').replace('\\',''), str(row[6].value).replace('"','').replace('\\',''), str(row[7].value).replace('"','').replace('\\',''),row[8].value, row[9].value, row[10].value)))
        except Exception as ex: 
            template = "Тип ошибки {0} \nArguments:{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            print(row)
            sys.exit(0)
    # Пишем в коллекцию МонгоДБ
    try:
        records.insert_many(a_rec, ordered=False)
    except pymongo.errors.BulkWriteError as e:
        print(e.details['writeErrors'])
    # Подсчитываем затраченное время
    count_doc_end = records.count_documents({})
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    print('count docs = {0} end docs = {1} delta = {2}'.format(count_doc_start,count_doc_end,count_doc_end-count_doc_start))

####################
for ff in onlyfiles:
    write_json(ff)
    file_name = '{{"file":"{0}"}}'.format(ff).encode('utf-8')
    
    #file_names_collection.insert_one(json.loads(file_name))
