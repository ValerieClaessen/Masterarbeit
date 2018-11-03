# Using Twitter API to look up status.text from tweets from file NAACL_SRW_2016.csv

import csv

import tweepy
from tweepy import OAuthHandler

from twython import Twython

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

twitter = Twython(
    consumer_key, consumer_secret, access_token, access_secret)

# id to text using tweepy
def get_tweet_text(tweet_id):
    tweet = api.get_status(tweet_id)
    return tweet.text

# id to text using Twython
def get_tweet_text_twython(tweet_id):
    tweet = twitter.show_status(id=tweet_id)
    return (tweet['text'])

with open('NAACL_SRW_2016_cleaned.csv', 'a') as csvfile_clean:

    writer = csv.writer(csvfile_clean, delimiter=';')
    writer.writerow(['ID', 'Form of Hate Speech', 'Tweet'])                 # header

    with open('NAACL_SRW_2016.csv') as csvfile:
        csv_reader: object = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            id_of_tweet = (row[0])
            hate = (row[1])
            tweet = get_tweet_text(id_of_tweet)
            print(tweet)

            writer = csv.writer(csvfile_clean, delimiter=';')
            writer.writerow([id_of_tweet, hate, tweet])