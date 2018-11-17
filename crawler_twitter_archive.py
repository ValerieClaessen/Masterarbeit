import csv
import json
import sys

import tweepy
from tweepy import OAuthHandler

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

with open('twitter_bullying_archive.csv', 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(['Tweet', 'Created at', 'User', 'ID', 'Reply to', 'Retweet', 'Text', 'Hashtags'])  # header

num_tweets = 1

hashtags = "#bully OR #bullying OR #blacklivesmatter OR #banIslam OR #stopIslam OR #rapefugees OR #whitelivesmatter OR #IfMySonWasGay OR #IfMyDaughterBroughtHomeABlack OR #ADeadJew OR #AGoodJew OR #IfIWereANazi OR #SignsYoSonIsGay OR #HowToTurnDownAUglyPerson OR #HeterosexualPrideDay OR #whitenesstoldme OR #onlyintheghetto OR #ifsantawasblack OR #notracist"

for tweet in tweepy.Cursor(api.search,q=hashtags,
                           lang="en",
                           since="2018-10-01").items(10000):
    print (num_tweets, tweet.text)

    with open('twitter_bullying_archive.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([num_tweets, tweet.created_at, tweet.author.screen_name, tweet.id,
                         tweet.in_reply_to_screen_name,
                         tweet.retweeted, tweet.text, tweet.entities.get('hashtags')])
        num_tweets += 1