#Cleans tweets and finds sentiment score of tweets 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import re

def tweetSent(tweet): 
    #returns a compounded score from a tweet that runs through the Vader sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(tweet)
    vs = sentiment['compound']
    return vs


def removePattern(input_txt, pattern): #remove words using given symbol or string ex. @ 
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
        
    return input_txt  


def clean_tweets(tweets):
    #remove twitter Return handles (RT @xxx:)
    tweets = np.vectorize(removePattern)(tweets, "RT @[\w]*:") 
    
    #remove twitter handles (@xxx)
    tweets = np.vectorize(removePattern)(tweets, "@[\w]*")
    
    #remove URL links (httpxxx)
    tweets = np.vectorize(removePattern)(tweets, "https?://[A-Za-z0-9./]*")
    
    #remove special characters, numbers, punctuations (except for #)
    tweets = np.core.defchararray.replace(tweets, "[^a-zA-Z]", " ")
    
    return tweets