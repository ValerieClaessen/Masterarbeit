# Using Twitter API to look up status.text from tweets from file NAACL_SRW_2016.csv

import csv

import tweepy
from tweepy import OAuthHandler

from twython import Twython

consumer_key = 'obZZa92lwvVyzgWmP2yLIyLNh'
consumer_secret = 'sZMjbyDsEVjVyQyGfWOK7O0YX5wtn6eeb5AiTPAdTm1YIxaAhb'
access_token = '2182630772-Hg4Y4zSoJb5S79W9SvJvA1202OMZS7m4RdS5bnT'
access_secret = 'H36PBHlXEwJib0FNrVgAhU45fRZEvf3opvqR3Jq52WSJr'

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

with open('bullying_traces_cleaned.csv', 'a') as csvfile_clean:

    writer = csv.writer(csvfile_clean, delimiter=';')
    writer.writerow(['ID', 'Tweet'])                 # header

    with open('data.csv') as csvfile:
        csv_reader: object = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            print(row)
            try:
                id_of_tweet = (row[0])
                tweet = get_tweet_text(id_of_tweet)
                print(tweet)

                writer = csv.writer(csvfile_clean, delimiter=';')
                writer.writerow([id_of_tweet, tweet])
            except tweepy.TweepError as e:
                print(e)