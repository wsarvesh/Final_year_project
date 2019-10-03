from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import dataset
import credentials

db = dataset.connect("sqlite:///tweets.db")

class TwitterStreamer():
    
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        
        stream = Stream(auth, listener)
        
        stream.filter(track=hash_tag_list)
        
 
class StdOutListener(StreamListener):
    
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    
    def on_data(self, data):
        try:
            print(data)
            with open(self, fetched_tweets_filename, 'a') as tf:
                tf.write(data)
                
        except BaseException as e:
            print("Error on_data",str(e))
        
#         print(data)
        return True
    
    def on_error(self, status):
        print("hi",status)
      
    def on_status(self, status):
        print(status.text)
        if coords is not None:
            coords = json.dumps(coords)
        table = db["tweets"]
        table.insert(dict(
            user_description=description,
            user_location=loc,
            coordinates=coords,
            text=text,
            user_name=name,
            user_created=user_created,
            user_followers=followers,
            id_str=id_str,
            created=created,
            retweet_count=retweets,))
            #user_bg_color=bg_color,
            #polarity=sent.polarity,
            #subjectivity=sent.subjectivity,
            #subjectivity=sent.subjectivity,))
            
    
    #def on_status(self, status):
     #   if status.retweeted_status:
      #      return
    #print(status.text)
        
        
if __name__ == '__main__':
    
    hash_tag_list = ['mumbai']
    fetched_tweets_filename = "tweets.json"
    
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    
#     listener = StdOutListener()
#     auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
#     auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
    
#     stream = Stream(auth, listener)
    
#     stream.filter(track=['akshay kumar'])