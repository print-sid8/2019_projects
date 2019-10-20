from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import credentials
from pykafka import KafkaClient
import json

# function with localhost number and kafka client running port
def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')

# defined a std class, it takes StreamListener and
# whenever there is any data in it, it will print it.

class StdOutListener(StreamListener):
    def on_data(self, data):
        #print(data)

# using imported json, to only produce data that has 'place' in it
# so twitter data is written as json, then looks for place then sends it
# to producer via topic with the help of kafka client.
#hence we indent the lines between if and return
        message = json.loads(data)
        if message['place'] is not None:
#calls the function of kafka client, gets kafka broker and stores it in
# client variable
            client = get_kafka_client()
# goes to prevoiusly created topic in kafka
            topic = client.topics['twittermap']
# producer produces data from the kafka topic.
# 'message' variable is not used at producer bcoz we dont want json to go into producer,
# its only to pull tweets with place in them.
            producer = topic.get_sync_producer()
            producer.produce(data.encode('ascii'))
        return True

# here we define on_error, and it prints any error we get.
def on_error(self, status):
    print(status)

if __name__ == "__main__":

# setup auth
    auth = OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

# new variables for tweet listener and streaming by calling StdOutListener and
# stream takes our auth and listener
    listener = StdOutListener()
    stream = Stream(auth, listener)

# streams tweets by tracking keyword
# only one filter at a time

    stream.filter(track=['climate'])

#filters stream by locations only
    #stream.filter(locations=[-180,-90,180,90])
