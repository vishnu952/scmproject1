import socket
import subprocess
import sys
import errno
import json
import time
import random
import os
from dotenv import load_dotenv
 
load_dotenv()
 
PORT = int(os.getenv("PORT"))
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = ("", PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
 
command_executed = False
if not command_executed:
    kafka_path = r'C:\kafka'
    # Start Zookeeper
    zookeeper_command = rf'{kafka_path}\bin\windows\zookeeper-server-start.bat {kafka_path}\config\zookeeper.properties'
    subprocess.Popen(['start', 'cmd', '/k', zookeeper_command], cwd=kafka_path, shell=True)
    
    # Start Kafka Broker
    kafka_command = rf'{kafka_path}\bin\windows\kafka-server-start.bat {kafka_path}\config\server.properties'
    subprocess.Popen(['start', 'cmd', '/k', kafka_command], cwd=kafka_path, shell=True)
    
    topic_command = rf'{kafka_path}bin\windows\kafka-topics.bat --create --topic learn --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1'
    subprocess.Popen(['start', 'cmd', '/k', topic_command], cwd=kafka_path, shell=True)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket created")
 
server.bind(ADDR)    # bind this socket to the address we configured earlier
server.listen(2)
print(f"[LISTENING] Server is listening on {SERVER}")

conn, addr = server.accept()
print(f'CONNECTION FROM {addr} HAS BEEN ESTABLISHED')
connected = True
while connected:
        try:
            for i in range(0,5):
                route = ['Newyork,USA','Chennai, India','Bengaluru, India','London,UK']
                routefrom = random.choice(route)
                routeto = random.choice(route)
                if (routefrom!=routeto):
                    data = {
                        "Battery_Level":round(random.uniform(2.00,5.00),2),
                        "Device_ID": random.randint(1150,1158),
                        "First_Sensor_temperature":round(random.uniform(10,40.0),1),
                        "Route_From":routefrom,
                        "Route_To":routeto
                        }
                    userdata = (json.dumps(data, indent=1)).encode(FORMAT)
                    conn.send(userdata)
                    print(userdata)
                    time.sleep(10)
                else:
                    continue
 
            # clientdata = conn.recv(1024).decode(FORMAT)
            # print("ACKNOWLEDGEMENT RECEIVED FROM CLIENT : " +clientdata)

 
        except IOError as e:
            if e.errno == errno.EPIPE:
                pass
     #close the connection

    # client = f'python C:\\Users\\vijayaram\\Desktop\\exafluence\\project\\python\\client.py'
    # subprocess.Popen(['start', 'cmd', '/k', client], cwd=kafka_path, shell=True)

    # consumer_command = f'python C:\\Users\\vijayaram\\Desktop\\exafluence\\project\\python\\consumer.py'
    # subprocess.Popen(['start', 'cmd', '/k', consumer_command], cwd=kafka_path, shell=True)

    # command_executed = True
# execute_command_once()
conn.close()