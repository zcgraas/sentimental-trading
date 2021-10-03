from dotenv import load_dotenv
from numpy.lib.function_base import average
import pandas as pd
import requests
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

load_dotenv()
bearerToken = os.getenv('TWITTER_BEARER_TOKEN')
df = pd.DataFrame()
tweets = []
analyzer = SentimentIntensityAnalyzer()

#gets requested ticker for search
def getTicker():
    ticker = input("Enter Stock or Crypto Ticker: ")
    return ticker

#sets parameters to be passed to the api
def setParams():
    params = {'q': '$'+ getTicker(),
          'tweet_mode': 'extended',
          'lang':'en',
          'count':'100'
          }
    return params

#builds and sends the request to the api
def buildRequest():
    response = requests.get(
    'https://api.twitter.com/1.1/search/tweets.json',
    params=setParams(),
    headers={'authorization': 'Bearer '+bearerToken})
    buildSet(response)

#gets full text data of each tweet
def get_data(tweet):
    data = tweet['full_text']           
    return data

#builds list of tweets to be analyzed
def buildSet(response):
    for tweet in response.json()['statuses']:
        row = get_data(tweet)
        tweets.append(row)
    printSentiment(tweets)

#gets the sentiment of each tweet and calculates the average sentiments for the tweets
def getSentiment(tweets):
    averageTS = 0.000
    tweetCount = 0.00
    for tweet in tweets:
        vs = analyzer.polarity_scores(tweet)
        averageTS += vs['compound']
        tweetCount += 1
        print("\nTweet Body: " + "{:-<65} {}".format(tweet, str(vs)))
    return (averageTS/tweetCount)

#prints the tweet and average sentiment
def printSentiment(tweets):
    print("Overall Average: " + str(getSentiment(tweets)))
    restartProgram()

#starts the program
def startProgram():
    start = input("This is an experiemental application.\nThis is not intended to provide financial advice.\nIt returns the average compound sentiment analysis score of 100 recent tweets involving your ticker.\n A positive score means the sentiment is overall positive.\nStart: y/n\n")
    if start == "Y" or start == "y":
        buildRequest()
    else:
        print("Thanks for checking it out!")

#restarts the program
def restartProgram():
    restart = input("Would you like to search another ticker: y/n\n")
    if restart == "Y" or restart == "y":
        buildRequest()
    else:
        print("Thanks for checking it out!")
        
startProgram()





