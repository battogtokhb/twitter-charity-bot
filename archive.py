from TwitterAPI import TwitterAPI
import json
import urllib.parse
import pandas as pd
import authentication as auth
from pandas.io.json import json_normalize



api = TwitterAPI(auth.consumer_key, auth.consumer_secret,  auth.access_token, auth.token_secret)

# With sandbox, our query can be 256 characters long -- noting if we ever encounter weird error

params = {
          "query" : "((we\'ll OR (we will)) donate for (every OR each) (retweet OR RT)) OR (for (every OR each) (RT OR retweet) this tweet gets ((we will) OR we\'ll) donate) OR (for (every OR each) (RT OR retweet) ((we will) OR we\'ll) donate)"
          }
          # do the parentheses check out? #yeah i tink so yeah looks good
          # YES for now HYPEEE
          # should we try this? I'm sure there are others but let's see if it works for now
          # RT / retweet; we'll / we will; every / each
          # is there a clean way to say "for each RT/retweet"?
          # yeah lets do that thats sMORT
          # maybe "for each (RT OR retweet) (we\'ll OR (we will)) donate"



#print ((params["query"]))

#print (len(params["query"]))

request = api.request('tweets/search/30day/:Development', params)

# Status code will tell us if it worked - 200 means its gucci
# I GOT A 422
# did you run the right section of code? lol
#print (request.status_code)

tweet_raw = []



for item in request:
    if  'retweeted_status' not in item and item not in tweet_raw:
        print ("appending original tweet")
        tweet_raw.append(item)
    else:
        original = item['retweeted_status']
        if original not in tweet_raw:
            tweet_raw.append(original)


normalized_tweets = json_normalize(tweet_raw)

#normalized_tweets["extended_tweet.full_text"]

#print (len(normalized_tweets))

#print (type(normalized_tweets))


#print (normalized_tweets['text'])

tweet_df = pd.DataFrame(json_normalize(tweet_raw), columns=
    ['extended_tweet.full_text',
    'user.screen_name',
    'user.verified',
    'user.followers_count',
    'entities.hashtags',
    'created_at',
    'favorite_count',
    'retweet_count'])

tweet_df

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(tweet_df)


tweet_df.to_csv("30DaySandbox-Jul13.csv", sep='\t')

test = pd.read_csv("30DaySandbox-Jul13.csv", sep='\t')

test





# fields we might want to use:
# retweeted_status ("This attribute contains a representation of the original Tweet that was retweeted")

# from this: https://developer.twitter.com/en/docs/tweets/search/api-reference/premium-search
# cuz im thinking we can use the fields in the tags to refine the search
