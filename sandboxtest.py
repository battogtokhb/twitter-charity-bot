from TwitterAPI import TwitterAPI
import json
import pandas as pd
from pandas.io.json import json_normalize
import authentication as auth

api = TwitterAPI(auth.consumer_key, auth.consumer_secret, auth.access_token, auth.token_secret)

request = api.request('tweets/search/30day/:Development', {'query': 'we\'ll donate for every retweet to help'})

tweet_raw = []

for item in request:
    tweet_raw.append(json.dumps(item))

tweet_df = pd.DataFrame(json_normalize(tweet_raw), columns=
    ['text',
    'user.screen_name',
    'created_at',
    'favorite_count',
    'in_reply_to_status_id',
    'retweeted_status',
    'matching_rules'])

tweet_df.to_csv("30DaySandbox.csv", sep='\t')
