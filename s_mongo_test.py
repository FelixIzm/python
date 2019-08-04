from pymongo import MongoClient
import pymongo, json, xlrd, sys, pprint, datetime,os,re
from datetime import datetime
from os import listdir
from os.path import isfile, join



client = MongoClient('35.193.230.58',
    username='felix', password='12345678', 
    authSource='obd',authMechanism='SCRAM-SHA-1')

db = client['obd']
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

#    "from": {0}, "id": {1}, "Фамилия":"{2}","Имя":"{3}","Отчество":"{4}","Дата рождения/Возраст":"{5}","Место рождения":"{6}",
#   "Дата и место призыва":"{7}","Последнее место службы":"{8}","Воинское звание":"{9}","Причина выбытия":"{10}","Дата выбытия":"{11}"


fx_rec = '''{{"f0": {0},"id": {1},"f2":"{2}","f3":"{3}","f4":"{4}","f5":"{5}","f6":"{6}","f7":"{7}","f8":"{8}","f9":"{9}","f10":"{10}","f11":"{11}"}}'''
#fx_rec = '''{{"f0": {0},"id": {1},"fl":["{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}"]}}'''

# Собираем названия файлов для обработки
mypath="E:\\Temp\\obd\\"
#mypath="c:\\Temp\\obd\\"

onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath, f))]

write_data = True

def cnv_cell(cell):
    if(cell.ctype == 3):
        dt = xlrd.xldate_as_datetime(cell.value, 0)
        str_date = datetime.strftime(dt,'%m.%d.%Y')
    elif(cell.ctype==1):
        str_date = cell.value.replace('\r','').replace('\t','').replace('\n',' ').replace('"','').replace('\\','')
    else:
        str_date = cell.value
    return str_date


def write_json(floc):
    global mypath, write_data
    a_rec=[]
    #Открываем ексель
    start_time = datetime.now()
    wb = xlrd.open_workbook(join(mypath,floc)) 
    if wb.nsheets> 1:
        #print(floc)
        for sheet in wb.sheets():
            print('\tимя={0} строк {1}'.format(sheet.name,sheet.nrows))
            if(sheet.nrows > 4):
                for i, row in enumerate(sheet.get_rows()):
                    if(row[0].ctype==0):
                        continue
                    if(row[0].ctype==1 and str(row[0].value).lower()=='id'):
                        continue
                    if(row[0].ctype==1 and str(row[0].value).lower()!='id'):
                        result = re.search(r'(\d+)', row[0].value)
                        if(result):
                            try:
                                str1=int(result.group())
                            except Exception as ex: 
                                template = "Int () Тип ошибки {0} \nArguments:{1!r}"
                                message = template.format(type(ex).__name__, ex.args)
                                print(message)
                                print(row)
                                sys.exit(0)  
                        else:
                            continue
                    else:
                        str1 = int(row[0].value)
                    if(str1):
                        #if i % 1000 == 0:
                        #    print(i)

                        try:
                            cell11 = cnv_cell(row[11])
                            cell05 = cnv_cell(row[5])
                            ss = fx_rec.format('"обд"', str1, cnv_cell(row[2]), cnv_cell(row[3]), 
                                cnv_cell(row[4]), cell05, cnv_cell(row[6]), cnv_cell(row[7]),
                                cnv_cell(row[8]), cnv_cell(row[9]), cnv_cell(row[10]),cell11)
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
        # Собираем данные из таблицы в json
        for i,row in enumerate(sheet.get_rows()):
            if(row[0].ctype==0):
                continue
            if(row[0].ctype==1 and str(row[0].value).lower()=='id'):
                continue
            if(row[0].ctype==1 and str(row[0].value).lower()!='id'):
                result = re.search(r'(\d+)', row[0].value)
                if(result):
                    str1=int(result.group())
                else:
                    continue
            else:
                str1 = int(row[0].value)
            if(str1):
                try:
                    if(re.search(r'Человек', row[1].value)):
                        cell11 = cnv_cell(row[11])
                        cell05 = cnv_cell(row[5])
                        a_rec.append(json.loads(fx_rec.format('"обд"', str1, cnv_cell(row[2]), cnv_cell(row[3]), cnv_cell(row[4]), 
                        cell05, cnv_cell(row[6]), cnv_cell(row[7]),cnv_cell(row[8]), cnv_cell(row[9]), cnv_cell(row[10]),cell11)))
                    else:
                        cell10 = cnv_cell(row[10])
                        cell04 = cnv_cell(row[4])
                        a_rec.append(json.loads(fx_rec.format('"обд"', str1, cnv_cell(row[1]), cnv_cell(row[2]), cnv_cell(row[3]), cell04, cnv_cell(row[5]), cnv_cell(row[6]), 
                            cnv_cell(row[7]),cnv_cell(row[8]), cnv_cell(row[9]), cell10)))
                except Exception as ex: 
                    template = "Тип ошибки {0} \nArguments:{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print(message)
                    print(row)
                    sys.exit(0)
        # Пишем в коллекцию МонгоДБ
        if(write_data):
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
        print('{0} {1}'.format(ff,os.path.getsize(join(mypath,ff))))
        write_json(ff)
        if(write_data):
            today = datetime.today()
            file_name = '{{"file":"{0}", "date":"{1}", "size":{2}}}'.format(ff, str(today.strftime("%d-%m-%Y %H.%M.%S")),os.path.getsize(join(mypath,ff))).encode('utf-8')
            file_names_collection.insert_one(json.loads(file_name))
    else:
        print('file: {0}'.format(ff))
