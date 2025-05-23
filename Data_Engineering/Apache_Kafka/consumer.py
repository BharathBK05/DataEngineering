from json import loads   
from kafka import KafkaConsumer


class consumer():
    def __init__(self) -> None:
        self.TOPIC = 'Test'

    def consume(self):
        try:
            consumer = KafkaConsumer(self.TOPIC,bootstrap_servers = ['localhost : 9092'],auto_offset_reset = 'latest',  
            enable_auto_commit = True,  
            group_id = 'my-group',
            value_deserializer = lambda x : loads(x.decode('utf-8'))  )
            for message in consumer:
                print(message.value)

        except Exception as e:
            print(str(e))    

if __name__=='__main__':
    con = consumer()
    con.consume()
            

           
