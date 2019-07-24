from pymongo import MongoClient
client = MongoClient('35.193.230.58',
    username='felix', password='12345678', 
    authSource='test',authMechanism='SCRAM-SHA-1')

db = client['test']
print(db.collection_names())
if 'my_collection' not in db.collection_names():
    db.create_collection('my_collection')
#print(client.database_names())  