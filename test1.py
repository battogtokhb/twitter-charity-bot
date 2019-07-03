#from tweepy import OAuthHandler, Stream, StreamListener
import tweepy
from tweepy.streaming import StreamListener
import authentication as auth
import pandas as pd
import numpy as np


# Test: tweet out a message to our Twitter account

    # myAuth = TwitterAuthenticator().authenticate()
    # api = tweepy.API(myAuth)
    # for tweet in tweepy.Cursor(api.search, q='tweepy').items(10):
    #     print(tweet.text)

    # print(api.me().name)
    # api.update_status(status='It is my birthday! Happy birthday to me!')

# Test: try to use Twitter streaming

# This creates a stream listener that prints tweets as they come in
class MyStreamListener(StreamListener):

    def __init__(self):
        self.tweets_dataframe = pd.DataFrame(data=[], columns=['Tweets'])
        self.counter = 0

    def on_data(self, data):
        try:
            #print("we have data from " + str(self.counter))
            self.tweets_dataframe[self.counter] = str(data)
            self.counter += 1
            if self.counter > 10:
                # only want to print first 10 tweets
                return False
        except BaseException as e:
            print("Data error: %s" % str(e))
        return True

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
    def StreamTweets(self, track_list):
        myAuth = self.twitter_auth
        # create stream listener and filter by the track_list

        myStream = tweepy.Stream(myAuth, self.myStreamListener)
        myStream.filter(track=track_list)


    def get_api(self):
        return self.api

    def get_tweets(self):
        return self.myStreamListener.get_data()

# Class to analyze tweets
#class TweetAnalyzer():
    #def analyze_tweets(self, tweets):



# Test if this code works so far (spoiler alert: it works (for me at least))
track_list = ['RT donate,day when']
myStreamer = TwitterStreamer()
#tweet_analyzer = TweetAnalyzer()
myStreamer.StreamTweets(track_list)
#api = myStreamer.get_api()
tweets = myStreamer.get_tweets()

for tweet in tweets:
    print(tweet)
