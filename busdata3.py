# testBusdata
from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time

input_file = open('./data/bus3.json')
json_array = json.load(input_file)

coordinates = json_array['features'][0]['geometry']['coordinates']

# CONSTRUCT MESSAGE
def gen_uuid():
    return uuid.uuid4()

def gen_checkpoint(coord):
    data = {}
    data['busline']='00003'
    data['key'] = data['busline']+'_' + str(gen_uuid())
    data['timestamp'] = str(datetime.utcnow())
    data['latitude'] = coord[1]
    data['longitude'] = coord[0]
    return data

# KAFKA PRODUCER
client = KafkaClient(hosts='localhost:9092')
topic = client.topics['geodata_final']
producer = topic.get_sync_producer()

while True:
    for coordinate in coordinates:
        data = gen_checkpoint(coordinate)
        msg = json.dumps(data)
        print(msg)
        producer.produce(msg.encode('ascii'))
        time.sleep(0.5)




'''
#KAFKA PRODUCER

client = KafkaClient(hosts='localhost:9092')

# print(client.topics)
# print(client.topics['testBusdata'])
topic = client.topics['testBusdata']

# buffer specified topic
producer = topic.get_sync_producer()

# need to encode it or else: TypeError: ("Producer.produce accepts a bytes object as message, but it got '%s'", <class 'str'>)

count =1 
for i in range(10):
    producer.produce(f'count:{i}'.encode('ascii'))

'''