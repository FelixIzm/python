from pymongo import MongoClient
client = MongoClient('35.193.230.58',
    username='felix', password='12345678', 
    authSource='test',authMechanism='SCRAM-SHA-1')

db = client['test']
print(db.collection_names())

#print(client.database_names())  