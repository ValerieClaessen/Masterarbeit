# Using Twitter API to crawl (cyberbullying) data from Twitter
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


# Stream & save tweets
class TwitterStreamListener(tweepy.StreamListener):
    collected_tweets = 0                                                                                    # number of tweets with topic terms
    num_tweets = 1                                                                                          # number of tweets saved to csv
    tweets = []                                                                                             # tweet-list for jsonfile

    with open('twitter_bullying.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Tweet', 'Created at', 'User', 'ID', 'Reply to', 'Retweet', 'Text', 'Hashtags'])  # header

    # Brauchen wir nicht?
    with open('twitter_bullying.json', 'w') as jsonfile:
        json.dump([], jsonfile)                                                                             # initialize file with empty list

    def on_status(self, status):
        TwitterStreamListener.collected_tweets += 1                                                         # count respective tweets

        try:
            print (TwitterStreamListener.collected_tweets, TwitterStreamListener.num_tweets, status.text)


            # saving all data to csv
            with open('twitter_bullying.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow([TwitterStreamListener.num_tweets, status.created_at, status.author.screen_name, status.id, status.in_reply_to_screen_name,
                                 status.retweeted, status.text, status.entities.get('hashtags')])

            # saving all data to json - brauchen wir nicht? - bisher nicht geordnet, nur zum Zählen
            with open('twitter_bullying.json', 'w') as tweets_jsonfile:
                entry = {'Number': TwitterStreamListener.num_tweets, 'Date': str(status.created_at),        # current tweet
                         'Text': status.text, 'Hashtags': status.entities.get('hashtags')}
                TwitterStreamListener.tweets.append(entry)                                                  # append to tweets-list
                json.dump(TwitterStreamListener.tweets,
                          tweets_jsonfile)                                                                  # write into file (to not overwrite existing entries)
                TwitterStreamListener.num_tweets += 1                                                       # count tweets that have been saved

        except Exception as e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass


        #Zum Testen: Stream stoppen nach einigen Tweets
        if TwitterStreamListener.num_tweets < 51:
            return True
        else:
            return False

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True


streaming_api = tweepy.streaming.Stream(auth, TwitterStreamListener(), timeout=60)

#TODO: Geeignete Hashtags aussuchen
terms = ['disney', 'pixar']                                                                                 # example topics

#TODO: Dritte Sprache?
streaming_api.filter(languages=["en", "ger"], track=terms)                                                  # only english and german tweets
