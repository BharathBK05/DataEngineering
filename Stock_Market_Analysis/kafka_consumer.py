from kafka import KafkaConsumer
from json import loads
from pymongo import MongoClient
  
# creation of MongoClient
client=MongoClient()
  
# Connect with the portnumber and host
client = MongoClient("mongodb://localhost:27017/")
  
# Access database
mydatabase = client['bharath']
  
# Access collection of the database
mycollection=mydatabase['share_Market']

consumer = KafkaConsumer(
    'share-market-analysis',
     bootstrap_servers=['localhost:9092'], 
    value_deserializer=lambda x: loads(x.decode('utf-8')))

for count, i in enumerate(consumer):
    mycollection.insert_one(i.value)