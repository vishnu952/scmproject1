from confluent_kafka import Consumer
import pymongo
from dotenv import load_dotenv
import os
import json
import ast
load_dotenv()
CONNECTION_STRING=os.getenv("connectdb")
print(CONNECTION_STRING)
c = pymongo.MongoClient(CONNECTION_STRING)

# --------------------
dblist=c.list_database_names()
if "logdata" in dblist:
    db=c["logdata"]
    collist=db.list_collection_names()
    if "devicedata" in collist:
        col_dev=db["devicedata"]
    else:
        db.create_collection("devicedata")
        col_dev=db["devicedata"] 
# ----------------------

consumer_config = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'learner',
    'auto.offset.reset': 'earliest',
}
kafka_consumer = Consumer(consumer_config)
topic = 'learn'
kafka_consumer.subscribe([topic])
def upload_to_database(data):
    json_objects = data.split('}')
    for json_object in json_objects:
        if json_object.strip():
            json_object += '}'
            try:
                document = json.loads(json_object)
                col_dev.insert_one(document)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
count=1
try:
    while count<=5:
        msg = kafka_consumer.poll(1.0)
        if msg is not None:
            count+=1
            data = msg.value().decode('utf-8')
            print(data)
            upload_to_database(data)
        else:
            continue
       
except KeyboardInterrupt:
    pass
finally:
    kafka_consumer.close()