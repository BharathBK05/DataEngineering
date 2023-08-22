from kafka import KafkaProducer
from time import sleep
from datetime import datetime
from json import dumps

class producer():
    def __init__(self) -> None:
        self.TOPIC = 'Test'
    
    def produce(self):
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                value_serializer=lambda x: 
                                dumps(x).encode('utf-8'))


        self.producer.flush()

        id = 1
        while True:
            dic = {}
            dic['Id'] = id
            dic['Time'] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

            self.producer.send(self.TOPIC, value=dic)

            sleep(1)
            id += 1

if __name__=='__main__':
    prd = producer()
    prd.produce()