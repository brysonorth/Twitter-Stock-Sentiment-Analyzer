import tweepy
import hidden
import pprint
import tweetSent
import pandas as pd

secrets = hidden.oauth() #pulls accesss tokens from hidden.py

#authenticates and connects to twitter API
auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
auth.set_access_token(secrets['access_token'], secrets['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
#notifies if rate limmit is reached and waits until 15 minutes block out is up

query = 'TSLA -filter:retweets' #finds query and filter out retweets
max_tweets = 25
searched_tweets = []
last_id = -1
tweetList = []

while len(searched_tweets) < max_tweets: #max tweets to return. limited by API rate limit
    count = max_tweets - len(searched_tweets)
    try:
        #finds recent tweets containing query, and are english. 
        #max_id starts with most recent tweet and works backwards until max_tweets is reached
        new_tweets = api.search(q=query, lang='en', count=count, result_type='recent', max_id=str(last_id - 1))
        if not new_tweets:
            break

        searched_tweets = new_tweets
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        break

for tweet in searched_tweets:
    text = tweet.text
    sentiment = tweetSent.tweetSent(text)
    scoreTuple = (text, sentiment['compound'])
    tweetList.append(scoreTuple)

df = pd.DataFrame(tweetList, columns=['tweetOG', 'Score'])

#for tweet in tweetList:
#    sentiment = tweetSent.tweetSent(tweet)
#    scoreTuple = (tweet, sentiment)
#    print(tweet + ' ---->SCORE:' + str(sentiment['compound']))
#    print('\n')
    

#remaingi rate limit from twitter API
limits = api.rate_limit_status()
remain_search_limits = limits['resources']['search']['/search/tweets']['remaining']

print('--------------------------------------------------------------')
print ('Remaining Rate', remain_search_limits)

print (df)