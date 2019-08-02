from pymongo import MongoClient
import pymongo, json, xlrd, sys, pprint, datetime,os,re
from datetime import datetime
from os import listdir
from os.path import isfile, join


client = MongoClient('35.193.230.58',
    username='felix', password='12345678', 
    authSource='test',authMechanism='SCRAM-SHA-1')

db = client['test']
collection_name = 'data'
if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)
    db[collection_name].create_index("id", unique=True)
     
records = db[collection_name]
count_doc_start = records.count_documents({})

file_names = 'files'
if file_names not in db.list_collection_names():
    db.create_collection(file_names)
    db[file_names].create_index(
    [("file", pymongo.ASCENDING), ("size", pymongo.ASCENDING)],
    unique=True
)
file_names_collection = db[file_names]

#loc = ("E:\\Temp\\obd\\москворецкий_рвк.xlsx") 

#fx_rec = '''{{"f0": {0},"id": {1},"f2":"{2}","f3":"{3}","f4":"{4}","f5":"{5}","f6":"{6}","f7":"{7}","f8":"{8}","f9":"{9}","f10":"{10}","f11":"{11}"}}'''
fx_rec = '''{{"f0": {0},"id": {1},"fl":["{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}"]}}'''

# Собираем названия файлов для обработки
#mypath="E:\\Temp\\obd\\"
mypath="c:\\Temp\\obd\\"

onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath, f))]

def write_json(floc):
    global mypath
    a_rec=[]
    #Открываем ексель
    start_time = datetime.now()
    wb = xlrd.open_workbook(join(mypath,floc)) 
    if wb.nsheets> 1:
        print(floc)
        for sheet in wb.sheets():
            print('\tимя={0} строк {1}'.format(sheet.name,sheet.nrows))
            if(sheet.nrows > 4):
                for i, row in enumerate(sheet.get_rows()):
                    if(row[0].ctype==0):
                        continue
                    if(row[0].ctype==1 and str(row[0].value).lower()=='id'):
                        continue
                    if(row[0].ctype==1 and str(row[0].value).lower()!='id'):
                        try:
                            int1 = int(row[0].value)
                        except ValueError:
                            continue
                    else:
                        int1 = int(row[0].value)

                    if(int1):
                        if i % 1000 == 0:
                            print(i)
                        try:
                            ss = fx_rec.format('"обд"', int1, row[2].value.replace('\r','').replace('\n',' '), row[3].value, row[4].value, str(row[5].value).replace('"','').replace('\\','').replace('\n',''), str(row[6].value).replace('"','').replace('\\','').replace('\n',''), str(row[7].value).replace('"','').replace('\\','').replace('\n',''),str(row[8].value).replace('"','').replace('\\','').replace('\n',''), row[9].value, row[10].value,row[11].value).replace('\n',' ').replace('\t',' ')
                            a_rec.append(json.loads(ss))
                        except Exception as ex: 
                            template = "Тип ошибки {0} \nArguments:{1!r}"
                            message = template.format(type(ex).__name__, ex.args)
                            print(message)
                            print(ss)
                            sys.exit(0)  
                try:
                    records.insert_many(a_rec, ordered=False)
                except pymongo.errors.BulkWriteError as e:
                    print('writeErrors')
                # Подсчитываем затраченное время
    else:
        sheet = wb.sheet_by_index(0) 
        #obj.__next__()
        # Собираем данные из таблицы в json
        for i,row in enumerate(sheet.get_rows()):
            if(row[0].ctype==0):
                continue
            if(row[0].ctype==1 and str(row[0].value).lower()=='id'):
                continue
            if(row[0].ctype==1 and str(row[0].value).lower()!='id'):
                try:
                    int1 = int(row[0].value)
                except ValueError:
                    continue
            else:
                int1 = int(row[0].value)
            #print('type = {0} value = {1} {2}'.format(row[0].ctype,row[0].value,row[0]))
            if(int1):
                if i % 1000 == 0:
                    print(i)
                try:
                    a_rec.append(json.loads(fx_rec.format('"обд"', int1, row[1].value, row[2].value, row[3].value, row[4].value, str(row[5].value).replace('"','').replace('\\',''), str(row[6].value).replace('"','').replace('\\',''), str(row[7].value).replace('"','').replace('\\',''),row[8].value, row[9].value, row[10].value).replace('\r','').replace('\n',' ')))
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
            print('writeErrors')
        # Подсчитываем затраченное время
    count_doc_end = records.count_documents({})
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    print('count docs = {0} end docs = {1} delta = {2}'.format(count_doc_start,count_doc_end,count_doc_end-count_doc_start))

####################
for ff in onlyfiles:
    if(file_names_collection.find({"file":ff}).count()==0):
        write_json(ff)
        today = datetime.today()
        file_name = '{{"file":"{0}", "date":"{1}", "size":{2}}}'.format(ff, str(today.strftime("%d-%m-%Y %H.%M.%S")),os.path.getsize(join(mypath,ff))).encode('utf-8')
        file_names_collection.insert_one(json.loads(file_name))
    else:
        print("file {0}".format(ff))