from pymongo import MongoClient
import pymongo, json
import datetime
import traceback

uri = "mongodb://felix:12345678@35.193.230.58/?authSource=test&authMechanism=SCRAM-SHA-1"
#client = MongoClient('35.193.230.58', 27017)
client = MongoClient(uri)

db = client['test']
'''
post = {"author": "Mike","text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()}
    '''


rec = '''{{
    "from": {0},
    "id": {1},
    "Фамилия":{2},
    "Имя":{3},
    "Отчество":{4},
    "Дата рождения/Возраст":{5},
    "Место рождения":{6},
    "Дата и место призыва":{7},
    "Последнее место службы":{8},
    "Воинское звание":{9},
    "Причина выбытия":{10},
    "Дата выбытия":{11}
}}'''

post = '''{{"автор": {0},"text": "text","tags": ["mongodb", "python", "pymongo"],"date": "date"}}'''
posts = db.posts
try:
    #print(post.format('Felix',"My next post",str(datetime.datetime.utcnow())))
    #post = post.format("Felix","My next post",str(datetime.datetime.utcnow())).encode('utf-8')
    post = post.format('"Robert"').encode('utf-8')
    print(post)
    posts.insert_one(json.loads(post))
except pymongo.errors.DuplicateKeyError:
    print("DuplicateKeyError")
except Exception as ex: 
    template = "Тип ошибки {0} \nArguments:{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)
    #continue
#print(post_id)
