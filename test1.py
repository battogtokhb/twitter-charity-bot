#from tweepy import OAuthHandler, Stream, StreamListener
import tweepy
from tweepy.streaming import StreamListener
import authentication as auth
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import json

# Test: tweet out a message to our Twitter account

    # myAuth = TwitterAuthenticator().authenticate()
    # api = tweepy.API(myAuth)
    # for tweet in tweepy.Cursor(api.search, q='tweepy').items(10):
    #     print(tweet.text)

    # print(api.me().name)
    # api.update_status(status='It is my birthday! Happy birthday to me!')



# broad class to get tweets with a track_list
class GetTweets():
    def get_tweets(self, track_list):
        myStreamer = TwitterStreamer()
        myStreamer.stream_tweets(track_list)
        return myStreamer.get_tweets()

    def get_api(self):
        auth = TwitterAuthenticator().authenticate()
        return tweepy.API(auth)



# This creates a stream listener that prints tweets as they come in
class MyStreamListener(StreamListener):

    def __init__(self):
        self.tweets_dataframe = pd.DataFrame()
        self.tweets_raw_json = []
        self.counter = 0

    def on_data(self, data):
        try:
            self.tweets_raw_json.append(json.loads(data))
            self.counter += 1
            if self.counter < 10:
                # only want to print first 10 tweets
                return True
        except BaseException as e:
            print("Data error: %s" % str(e))
        # print (self.tweets_raw_json[0]) <-- exmaple raw json
        # Normalize JSON 'flattens' the JSON to detail with nested columns
        self.tweets_dataframe = pd.DataFrame(json_normalize(self.tweets_raw_json), columns=
        ['text',
        'user.screen_name',
        'created_at',
        'favorite_count',
        'retweeted_status'])
        return False

    def on_error(self, status_code):
        if status == 420:
            # Return false if we have a rate limit issue
            print(status_code)
            return False
        print(status_code)

    def get_data(self):
        return self.tweets_dataframe

# Class for authenticating
class TwitterAuthenticator():

    def authenticate(self):
        # note: might need to change this to tweepy.AppAuthHandler
        twitterAuth = tweepy.OAuthHandler(auth.consumer_key, auth.consumer_secret)
        twitterAuth.set_access_token(auth.access_token, auth.token_secret)
        return twitterAuth


class TwitterStreamer():
    def __init__(self):
        self.twitter_auth = TwitterAuthenticator().authenticate()
        self.api = tweepy.API(self.twitter_auth)
        self.myStreamListener = MyStreamListener()

    # For finding and processing live tweets
    def stream_tweets(self, track_list):
        # create stream listener and filter by the track_list
        myStream = tweepy.Stream(self.twitter_auth, self.myStreamListener)
        myStream.filter(track=track_list)


    def get_api(self):
        return self.api

    def get_tweets(self):
        return self.myStreamListener.get_data()

# Class to analyze tweets
class TweetAnalyzer():
    def print_tweets(self, tweets, headers):
        print (tweets[headers].head(n=10)) #head returns the first n rows



# Test if this code works so far

myTweeter = GetTweets()
myAnalyzer = TweetAnalyzer()

#track_list = ['RT to donate,well']
#tweets = myTweeter.get_tweets(track_list)


# This section is to test historical tweets - right now it just prints tweets

api = myTweeter.get_api()
tweet_df = pd.DataFrame()
tweet_raw = []
# Finds the most recent tweets including the search keys and adds them to a list
for tweet in tweepy.Cursor(api.search, q='today').items(10):
    tweet_raw.append(tweet._json)

tweet_df = pd.DataFrame(json_normalize(tweet_raw), columns=
    ['text',
    'user.screen_name',
    'created_at',
    'favorite_count',
    'retweeted_status'])
myAnalyzer.print_tweets(tweet_df, ['text', 'retweeted_status'])

pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', None)
test = pd.read_csv("30DaySandbox-Jul14-Q1.csv", sep='\t')
test
test2 = pd.read_csv("30DaySandbox-Jul14.csv", sep='\t')
test2





















#### GETTING OUR DATA ####





from TwitterAPI import TwitterAPI
import json
import urllib.parse
import pandas as pd
import authentication as auth
from pandas.io.json import json_normalize

# Authenticate
api = TwitterAPI(auth.consumer_key, auth.consumer_secret,  auth.access_token, auth.token_secret)

# Be careful to call this only once, at the beginning
tweet_raw = []



### REPEAT HERE ###

# Get request - 2 months at a time
params = {
          # Note: The query can be up to 256 characters for 30 day, but only 128 characters for full archive
          "query" : ( "((every OR each) (RT OR retweet) ((we will) OR we\'ll) donate)"
          " OR ((we\'ll OR (we will)) donate (every OR each) (retweet OR RT))" ),
          #            YYYYMMDDHHmm
          "fromDate": "201905020000",
          #          YYYYMMDDHHmm
          "toDate": "201907080000"
          }

print (params)

request = api.request('tweets/search/fullarchive/:Development', params)
print(request.status_code)
# wait it's 0 that's not good
# f00k
# no worries bro, ill
# damn ok I have to go help my mom make some dinner I'm curious that it didn't add anything
#(oooo im curious about the count)
print(count)
count = 0
# Add the (non-retweeted) tweets to our tweet_raw list
for item in request:
    if  'retweeted_status' not in item and item not in tweet_raw:
        count += 1
        tweet_raw.append(item)
    else:
        original = item['retweeted_status']
        if original not in tweet_raw:
            tweet_raw.append(original)

tweet_raw


# -- CALL ONCE DONE WITH ENTIRE DATA COLLECTION --

normalized_tweets = json_normalize(tweet_raw)

# Put the full text into the same column
for index, row in normalized_tweets.iterrows():
    if pd.isnull(row['extended_tweet.full_text']):
        normalized_tweets.at[index,'extended_tweet.full_text'] = row['text']

tweet_df = pd.DataFrame(normalized_tweets, columns=
    ['extended_tweet.full_text',
    'retweet_count',
    'user.screen_name',
    'user.verified',
    'user.followers_count',
    'entities.hashtags',
    'created_at',
    'favorite_count'
    ])


tweet_df.to_csv("fullArchive.csv", sep='\t')
