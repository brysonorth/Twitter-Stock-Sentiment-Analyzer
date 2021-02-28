import tweepy
import hidden
import pprint
import tweetSent
import html
import pandas as pd

secrets = hidden.oauth() #pulls accesss tokens from hidden.py

#authenticates and connects to twitter API
auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
auth.set_access_token(secrets['access_token'], secrets['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
#notifies if rate limit is reached and waits until 15 minute wait time is up


max_tweets = 3
searched_tweets = []
last_id = -1
stocksList = ['$NVDA', '$NFLX', '$PYPL']
scores = []
scoreList = []
tickList = []

for stock in stocksList:
    # query to search. filters out retweets
    query = stock + ' -filter:retweets'
    while len(searched_tweets) < max_tweets: #max tweets to return. limited by API rate limit
         #filters retweets for query 
        count = max_tweets - len(searched_tweets)
        try:
            #finds recent tweets containing query, and are english. 
            #max_id starts with most recent tweet and works backwards until max_tweets is reached
            new_tweets = api.search(q=query, lang='en', count=count, result_type='mixed', max_id=str(last_id - 1))
            if not new_tweets:
                break
            
            #excludes tweet beginning with '@' to avoid replies
            for tweet in new_tweets:
                currenttweet = html.unescape(tweet.text)
                if not currenttweet[:1].startswith('@'):
                    searched_tweets.append(tweet)
                    last_id = new_tweets[-1].id
        
        except tweepy.TweepError as e:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            break
    
    for tweet in searched_tweets:
        text = tweet.text
        #list dictionaries of tickers and tweets including given ticker
        tickList.append({'stock': stock, 'text':text}) 

    #converts tickList into dataframe
    df = pd.DataFrame.from_dict(tickList)
    df['text'] =  tweetSent.clean_tweets(df['text'])

    #calls sentiment analyzer funcction and returns a compounded score
    for i in range (df['text'].shape[0]):
        compound = tweetSent.tweetSent(df['text'][i])
        scores.append({'compound':compound})

    #joining the tweets df with the scores df    
    sentScore = pd.DataFrame.from_dict(scores)
    df = df.join(sentScore)

    #find average of sentiment scores for a given stock
    scoreAvg = df['compound'].mean()
    scoreAvg = round(scoreAvg, 5)
    scoreList.append({'stock':stock, 'score': scoreAvg})
    print(df)
    
    #clear lists
    tickList.clear()
    scores.clear()
    searched_tweets.clear()
    new_tweets.clear()


#remaingi rate limit from twitter API
limits = api.rate_limit_status()
remain_search_limits = limits['resources']['search']['/search/tweets']['remaining']


print('-----------------------------------------------------------------')
print ('Remaining Rate', remain_search_limits)
print(scoreList)
