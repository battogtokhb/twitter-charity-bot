#from tweepy import OAuthHandler, Stream, StreamListener
import tweepy
from tweepy.streaming import StreamListener
import authentication as auth


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
    def on_data(self, data):
        try:
            print(data)
        except BaseException as e:
            print("Data error: %s" % str(e))
        return True

    def on_error(self, status_code):
        if status == 420:
            # Return false if we have a rate limit issue
            return False
        print(status_code)

# Class for authenticating
class TwitterAuthenticator():

    def authenticate(self):
        # note: might need to change this to tweepy.AppAuthHandler
        twitterAuth = tweepy.OAuthHandler(auth.consumer_key, auth.consumer_secret)
        twitterAuth.set_access_token(auth.access_token, auth.token_secret)
        return twitterAuth


class TwitterStreamer():
    def __init__(self):
        self.twitter_auth = TwitterAuthenticator()

    # For finding and processing live tweets
    def StreamTweets(self, track_list):
        myAuth = self.twitter_auth.authenticate()
        # create stream listener and filter by the track_list
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(myAuth, myStreamListener)
        myStream.filter(track=track_list)

# Test if this code works so far (spoiler alert: it works (for me at least))
track_list = ['RT,donate']
myStreamer = TwitterStreamer()
myStreamer.StreamTweets(track_list)
