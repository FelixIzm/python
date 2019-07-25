from pymongo import MongoClient
import pymongo
import datetime
uri = "mongodb://felix:12345678@35.193.230.58/?authSource=test&authMechanism=SCRAM-SHA-1"
#client = MongoClient('35.193.230.58', 27017)
client = MongoClient(uri)

db = client['test']

post = {"author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()}
posts = db.posts
try:
    posts.insert_one(post)
except pymongo.errors.DuplicateKeyError:
    print("DuplicateKeyError")
    #continue
#print(post_id)
