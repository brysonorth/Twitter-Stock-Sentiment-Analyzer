# Twitter-Stock-Sentiment-Analyzer
The purpose of this project is to build a stock sentiment analyzer that compares tweet sentiments on a WoW or MoM basis on particular stocks. For ease of use I've chosen about 40 stocks from the NADAQ 100. The project is limited in the amount of tweets it gathers due to Twitters API restrictions. I am limiited to 180 API calls every 15 minutes and from the Twitter API docs:

"Please note that Twitter’s search service and, by extension, the Search API is not meant to be an exhaustive source of Tweets. Not all Tweets will be indexed or made available via the search interface."
This results in some stocks not being pulled from the twitter API every time the program runs. If a certain stock cannot be pulled from the API it is skipped on that particular run of the program.

The gathered tweets are run through the VADER analyzer library. VADER is a library for determining the sentiment of strings, or in this case tweeets.
The score used is the VADER compound score, which is between -1 to 1 with -1 being very negative and 1 being very positive. 

The average score of all tweets fro a given stock are then inserted into an SQLite database. The score for a given stock is then compared to the last score stored in the database from the previous run date. The current score and %change from the previous score are then printed to screen. (NOTE: if a stock was not found from the Twitter API query during the last program run, the %change will not be displayed)


twitter API access tokens need to be applied for by each user. My tokens are pulled from a  
sepereate file not in the repository. 

 In the future I intend to add visulization through a bar graph showing the current scores and percentage changes of all stocks, likely using pandas.
