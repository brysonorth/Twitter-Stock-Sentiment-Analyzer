import tweepy
import hidden
import pprint
import tweetSent

secrets = hidden.oauth() #pulls accesss tokens from hidden.py

#authenticates and connects to twitter API
auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
auth.set_access_token(secrets['access_token'], secrets['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

query = 'TSLA -filter:retweets'
max_tweets = 100
searched_tweets = []
last_id = -1


while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
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
    sentiment = tweetSent.tweetSent(tweet.text)
    print(tweet.text + ' ---->SCORE:' + str(sentiment['compound']))
    print('\n')

limits = api.rate_limit_status()
remain_search_limits = limits['resources']['search']['/search/tweets']['remaining']

print('--------------------------------------------------------------')
print ('Remaining Rate', remain_search_limits)