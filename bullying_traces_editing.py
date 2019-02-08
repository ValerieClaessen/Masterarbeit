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

# start tweepy with a wait_on_rate_limit, so it won't stop after the limit of looked up tweets is reached
api = tweepy.API(auth, wait_on_rate_limit=True)

twitter = Twython(
    consumer_key, consumer_secret, access_token, access_secret)

# function to get the text of a tweet based on the id using tweepy
def get_tweet_text(tweet_id):
    tweet = api.get_status(tweet_id)
    return tweet.text

# function to get the text of a tweet based on the id using Twython
def get_tweet_text_twython(tweet_id):
    tweet = twitter.show_status(id=tweet_id)
    return (tweet['text'])

# save file as a new file with ; as delimiter
with open('data.csv', encoding="utf-8", errors='ignore') as f:
    reader = csv.reader(f, delimiter = ',')

    with open('bullying_traces_cleaned.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        for row in reader:
            try:
                writer.writerow(row)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % ("twitter-hate-speech-classifier_cleaned.csv", reader.line_num, e))

# find the text of tweets and save it as a new column
with open('bullying_traces_cleaned.csv', 'r') as f2:
    reader2 = csv.reader(f2, delimiter = ";")

    with open('bullying_traces_cleaned2.csv', 'w') as csvfile2:
        writer2 = csv.writer(csvfile2, delimiter=';')

        # new header containg the column for the text of the tweet
        writer2.writerow(["User ID", "Tweet ID", "Text", "Cyberbullying", "Type", "Form", "Teasing"])

        for row in reader2:
            #print(row)
            try:
                # if the tweet is labeled as cyberbullying ("y") change the annotation to "1", otherwise change it to "0"
                if row[2] == "y":
                    row[2] = 1
                else:
                    row[2] = 0

                # if the tweet is labeled as teasing ("y") change the annotation to "1", otherwise change it to "0"
                if row[5] == "y":
                    row[5] = 2
                elif row[5] == "n":
                    row[5] = 1
                else:
                    row[5] = 0
                id_of_tweet = (row[0])
                tweet = get_tweet_text(id_of_tweet)         # look up the text of the tweet based on the id

                #print([row[1], id_of_tweet, tweet, row[2], row[3], row[4], row[5]])

                # save the data in a new file that contains the column with the text of the tweet
                writer2.writerow([row[1], id_of_tweet, tweet, row[2], row[3], row[4], row[5]])
            except tweepy.TweepError as e:
                print(e)