from os import environ
import tweepy
import time
import requests
import pandas as pd
from io import BytesIO
import random

TWITTER_CONSUMER_KEY = environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = environ['TWITTER_CONSUMER_SECRET']
TWITTER_ACCESS_TOKEN = environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = environ['TWITTER_ACCESS_TOKEN_SECRET']


def autentification():
    try:
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth,wait_on_rate_limit=True)
        return api
    except:
        print('An error occur while accessing the api')
        autentification()

def read_data(url):
    try:
        df = pd.read_csv(url)
    except:
        print('an error occur while retriving the data')
        read_data(url)
    return df

def random_tweet(df, last_tweet):
    tweets_id = list(df[df['tweets'] != last_tweet].index)
    random_choice = random.choice(tweets_id)
    tweet_choosen = df['tweets'][random_choice]
    return tweet_choosen

i = 1
while True:
    api = autentification()
    sheet_url = 'https://docs.google.com/spreadsheets/d/1g1q1FgU0zUR-gtikZt7oFbyemJi31xguCxL0U1KtIqA/edit#gid=1133003764'
    csv_export_url = sheet_url.replace('/edit#', '/export?format=csv&')
    df = read_data(csv_export_url)

    try:
        time_choosen = df['time_in_hour'][0]
        interval = float(time_choosen)
    except:
        interval = None
    
    if interval:
        try:
            all_tweets = api.user_timeline()
            tweet_choosen = df['tweets'][i]
            api.update_status(tweet_choosen)
            print('The last statue updated :', tweet_choosen)
            time.sleep(60*60*interval) 
        except:
            print('an error has been occured')
        # if it's the last row return from the beggining
        if i == df.shape[0]:
            i = 1
        else:
            # change to the next row
            i+= 1
    else:
        print("There's no time set an update will be within an hour isa.")
        time.sleep(60*60)
    
