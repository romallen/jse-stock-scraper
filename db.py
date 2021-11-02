from dotenv import load_dotenv
import os
import pymongo

load_dotenv()

client = pymongo.MongoClient(os.environ.get("DB_URL"))
db = client["jse"]
col = db["stocks"]
mydict = {"name": "John", "address": "Highway 37"}
x = col.insert_one(mydict)
print(x)
