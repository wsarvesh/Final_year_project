from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pandas as pd
import json
# import dataset
import credentials
import sqlite3
import nltk
from nltk.tokenize import RegexpTokenizer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import pickle
from Naive_bayes_model import *
import xgboost as xgb


f = open('models/nb2.pickle', 'rb')
NBayesClassifier = pickle.load(f)
f.close()

f1 = open('models/xgb.pickle', 'rb')
XGBClassifier = pickle.load(f1)
f1.close()

conn = sqlite3.connect('tweets.db')
c = conn.cursor()

def pred(data):

    tweetProcessor = PreProcessTweets()
    preprocessedTrainingSet = tweetProcessor.processTweets(data)

    word_features = buildVocabulary(preprocessedTrainingSet)
#     print("\n",word_features,"\n")
#     buildVocabulary(preprocessedTrainingSet)
    trainingFeatures = nltk.classify.apply_features(extract_features, preprocessedTrainingSet)

    print(preprocessedTrainingSet[0][0])

    NB = NBayesClassifier.classify(extract_features(preprocessedTrainingSet[0][0],word_features))

    return NB



def attributeselection(tweet,query_word):
    attr= []

    #text = "Alleged East Bay serial arsonist arrested #SanFrancisco - http://t.co/ojuHfkHVb2"
    tweet = tweet.lower() # convert text to lower-case
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet) # remove URLs
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet) # remove username
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet) # remove the # in #hashtag
    tweet = re.sub(r'\\s+',r' ', tweet, flags=re.I)
    tweet = re.sub("([^\x00-\x7F])+"," ",tweet) #remove all non-english characters
    tweet = re.sub(r"\s+"," ", tweet, flags = re.I) #remove multiple spaces
    text = tweet
    text = nltk.word_tokenize(text)
    poslist = nltk.pos_tag(text)
#     print(poslist)

    verblist = []
    for i in range(len(poslist)):
        if poslist[i][1].startswith('V'):
            verblist.append(poslist[i])

    word_count = len(poslist)
#     print(word_count)

    if len(verblist) == 0:
        l = (query_word,'VB')
        verblist.append(l)

#     print(verblist,"\n")
    verb_count = len(verblist)
#     print(verb_count)

   # query_word = 'arson'

    words_before = words_after = 0
    for i in range(len(poslist)):
        if poslist[i][0].startswith(query_word):
            words_before = i

    words_after = word_count - words_before - 1

#     print(words_before)
#     print(words_after)
    verbs = []
    attr.append(word_count)
#     for i in verblist:
#         print(i[0])
#         verbs.append(i[0])
#     attr.append(verbs)
    attr.append(verb_count)
    attr.append(words_before + 1)
#     attr_query_word.append(query_word)
    attr.append(words_before)
    attr.append(words_after)



    column_names = ['no_of_words', 'no_of_verbs', 'pos_query_word', 'word_before', 'word_after']
    print(attr,column_names)
    df = pd.DataFrame([attr], columns=column_names)
    arr_x=df.to_numpy(dtype=object)
    print(arr_x,arr_x.shape)
    y_pred = XGBClassifier.predict(arr_x)
    print("PRIORITY: ",y_pred)



class TwitterStreamer():

    def stream_tweets(self, fetched_tweets_filename, hashtag):
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

        stream = Stream(auth, listener,tweet_mode='extended')

        stream.filter(languages=["en"],track=[hashtag])


class StdOutListener(StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_error(self, status):
        print(status)

    def on_data(self, data):
        if hashtag == '-1':
            return False
        all_data             = json.loads(data)
        created_at           = all_data['created_at']
        favorite_count       = all_data['favorite_count']
        favorited            = all_data['favorited']
        filter_level         = all_data['filter_level']
        lang                 = all_data['lang']
        retweet_count        = all_data['retweet_count']
        retweeted            = all_data['retweeted']
        source               = all_data['source']
        text                 = all_data['text']
        truncated            = all_data['truncated']
        user_created_at      = all_data['user']['created_at']
        user_followers_count = all_data['user']['followers_count']
        user_location        = all_data['user']['location']
        user_lang            = all_data['user']['lang']
        user_name            = all_data['user']['name']
        user_screen_name     = all_data['user']['screen_name']
        user_time_zone       = all_data['user']['time_zone']
        user_utc_offset      = all_data['user']['utc_offset']
        user_friends_count   = all_data['user']['friends_count']
        geo_enabled          = all_data['user']['geo_enabled']
        coordinates          = all_data['coordinates']
        geo                  = all_data['geo']
        place                = all_data['place']
        if place is not None:
            place_name       = all_data['place']['name']
        else:
            place_name       = all_data['place']

        print("hashtag: ",hashtag)
        print("Tweet: "+text+"\n")

        data = [{'text': text,'Classfication': ''}]

        info = pred(data)

        if info == 'Relevant' or info == 1 or info == '1':
            attributeselection(text,'coronavirus')

        print("\n Class: "+info+"\n")

        conn = sqlite3.connect('tweets.db')
        c = conn.cursor()

        c.execute('''INSERT INTO all_tweet
        (hashtag,created_at, favorite_count, favorited, filter_level, lang,
                         retweet_count, retweeted, source, text, truncated, user_created_at,
                         user_followers_count, user_location, user_lang, user_name,
                         user_screen_name, user_time_zone, user_friends_count,geo_enabled,coordinates,geo,place_name )
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (hashtag,created_at, favorite_count, favorited, filter_level, lang, retweet_count,
                         retweeted, source, text, truncated, user_created_at,
                         user_followers_count, user_location, user_lang, user_name,
                         user_screen_name, user_time_zone, user_friends_count,geo_enabled,coordinates,geo,place_name ))

        c.execute('''INSERT INTO tweet_class
        (text, class)
            VALUES (?,?)''',
            (text, info))

        conn.commit()


def stream(h):
    print("              hfdshjdskfjdsklfjsdlkfjdslkfjflksdjfklsfjslk               ",h)

    global hashtag
    hashtag = h
    # if __name__ == '__main__':
    print("hashtag: ",hashtag)

    fetched_tweets_filename = "tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hashtag)
