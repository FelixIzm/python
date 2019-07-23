from pymongo import MongoClient
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

posts.insert_one(post)
#print(post_id)
