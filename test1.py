#from tweepy import OAuthHandler, Stream, StreamListener
import tweepy
from tweepy.streaming import StreamListener
import authentication as auth


# Test: tweet out a message to our Twitter account

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
        print(status_code)


class TwitterStreamer():
    # Class for finding and processing live tweets
    def StreamTweets(self, track_list):
        # This handles authentication and connection to the Twitter API
        # note: might need to change this to tweepy.AppAuthHandler
        twitterAuth = tweepy.OAuthHandler(auth.consumer_key, auth.consumer_secret)
        twitterAuth.set_access_token(auth.access_token, auth.token_secret)
        api = tweepy.API(twitterAuth)

        # create stream listener and filter by the track_list
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(twitterAuth, myStreamListener)

        myStream.filter(track=track_list)

# Test if this code works so far
track_list = ['Joe Biden', 'Julian Castro', 'Bernie Sanders']
myStreamer = TwitterStreamer()
myStreamer.StreamTweets(track_list)
