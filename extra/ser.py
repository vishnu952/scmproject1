import socket
from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient

TOPIC = "learn"
SERVER = socket.gethostbyname(socket.gethostname())

def consume_from_kafka(topic):
    c = Consumer({
        'bootstrap.servers': SERVER,
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest'
    })
    c.subscribe([topic])

    # client = MongoClient('localhost', 27017)
    # db = client['your_db_name']
    # collection = db['your_collection_name']

    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        value = msg.value().decode('utf-8')
        
        # Insert data into MongoDB
        # collection.insert_one({'message': value})
        print(value)

    c.close()

consume_from_kafka(TOPIC)
