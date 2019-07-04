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


# This creates a stream listener that prints tweets as they come in
class MyStreamListener(StreamListener):

    def __init__(self):
        self.tweets_dataframe = pd.DataFrame()
        self.tweets_raw_json = []
        self.counter = 0

    def on_data(self, data):
        #print (self.counter)
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
        self.tweets_dataframe = pd.DataFrame(json_normalize(self.tweets_raw_json), columns=['created_at', 'text', 'user.screen_name', 'retweeted'])
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
track_list = ['RT to donate,day when']
tweets = GetTweets().get_tweets(track_list)
#api = myStreamer.get_api()

myAnalyzer = TweetAnalyzer()
myAnalyzer.print_tweets(tweets, ['text', 'user.screen_name'])
