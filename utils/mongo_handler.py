from pymongo import MongoClient

def get_mongo_client (uri="mongodb://localhost:27017/"):
    client = MongoClient (uri)
    return client


def insert_ohlc (data, db_name="trading", collection_name="raw_ohlc"):
    client = get_mongo_client()
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_one(data)


#def insert_many_ohlc (data_list, db_name="trading", collection_name="raw_ohlc"):
 #   client = get_mongo_client()
  #  db = client[db_name]
  #  collection = db[collection_name]
   # if data_list:
    #    collection.insert_many(data_list)