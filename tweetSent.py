#find sentiment of tweet 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#import numpy as np
import pandas as pd
import re


def tweetSent(sentence): 
    cleanSentence = removePattern(sentence, '@')
    cleanSentence = cleanSentence.replace("[^a-zA-Z#]", " ")
    #cleanSentence= cleanSentence.apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(cleanSentence)
    return vs


def removePattern(input_txt, pattern): #remove words using given symbol or string ex. @ 
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
        
    return input_txt  


#dfTweets = pd.DataFrame(searchedTweets, columns=['rawTweets'])