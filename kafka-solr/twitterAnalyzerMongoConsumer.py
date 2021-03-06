from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from kafka import KafkaConsumer
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/',
                     username='seech', password='sechien')
db = client.twitter
collection = db.tweets

if __name__ == '__main__':
    print('Mongo consumer listening for messages...')
    topic_name = 'tweets-kafka'

    consumer = KafkaConsumer(topic_name,
                             auto_offset_reset='latest',
                             bootstrap_servers=['localhost:9092'],
                             api_version=(0, 10),
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))  # , consumer_timeout_ms=1000)

    for msg in consumer:
        result = collection.insert_one(msg.value)
        print(collection.find_one({'_id': result.inserted_id}))
