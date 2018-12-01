# Cleaning and looking up Tweets from IDs of Bullying Traces (data.csv)

import csv
import sys

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

with open('data.csv', encoding="utf-8", errors='ignore') as f:    #save with ; as delimiter
    reader = csv.reader(f, delimiter = ',')

    with open('bullying_traces_cleaned.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        for row in reader:
            try:
                writer.writerow(row)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % ("twitter-hate-speech-classifier_cleaned.csv", reader.line_num, e))

with open('bullying_traces_cleaned.csv', 'r') as f2:
    reader2 = csv.reader(f2, delimiter = ";")

    with open('bullying_traces_cleaned2.csv', 'w') as csvfile2:
        writer2 = csv.writer(csvfile2, delimiter=';')
        writer2.writerow(["User ID", "Tweet ID", "Text", "Cyberbullying", "Type", "Form", "Teasing"])

        for row in reader2:
            print(row)
            try:
                if row[2] == "y":
                    row[2] = 1
                else:
                    row[2] = 0

                if row[5] == "y":
                    row[5] = 2
                elif row[5] == "n":
                    row[5] = 1
                else:
                    row[5] = 0
                id_of_tweet = (row[0])
                tweet = get_tweet_text(id_of_tweet)

                print([row[1], id_of_tweet, tweet, row[2], row[3], row[4], row[5]])
                writer2.writerow([row[1], id_of_tweet, tweet, row[2], row[3], row[4], row[5]])
            except tweepy.TweepError as e:
                print(e)