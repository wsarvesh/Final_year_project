from nltk.corpus import stopwords
from string import punctuation
import re
import nltk
# word_features = {}

class PreProcessTweets:
    def __init__(self):
#         from nltk.corpus import stopwords
#         from string import punctuation
        self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER','URL'])
        
    def processTweets(self, list_of_tweets):
        processedTweets=[]
            
        for tweet in list_of_tweets:
            processedTweets.append((self._processTweet(tweet["text"]),tweet["Classfication"]))
        return processedTweets
    
    def _processTweet(self, tweet):
#         import re
        from nltk.tokenize import word_tokenize
        tweet = tweet.lower() # convert text to lower-case
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet) # remove URLs
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet) # remove usernames
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet) # remove the # in #hashtag
        tweet = word_tokenize(tweet) # remove repeated characters (helloooooooo into hello)
        return [word for word in tweet if word not in self._stopwords]
    
    


def buildVocabulary(preprocessedTrainingData):
#     import nltk 
#     global word_features
    all_words = []
    
    for (words, sentiment) in preprocessedTrainingData:
        all_words.extend(words)

    wordlist = nltk.FreqDist(all_words)
    word_features = wordlist.keys()
    
    return word_features

def extract_features(tweet,word_features):
#     global word_features
    tweet_words = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in tweet_words)
    return features