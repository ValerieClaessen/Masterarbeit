# Using Twitter API to crawl data related to cyberbullying and hate speech from Twitter

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

# We will use Tweepy to crawl tweets from Twitter
api = tweepy.API(auth)

# crawl tweets by using the TwitterStreamListener (only new tweets that suit our properties will be found)
class TwitterStreamListener(tweepy.StreamListener):
    collected_tweets = 0                                                                # number of tweets with topic terms
    num_tweets = 1                                                                      # number of tweets saved to csv

    # create csv file that will contain all found tweets
    with open('twitter_bullying.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        # header
        writer.writerow(['Tweet', 'Created at', 'User', 'ID', 'Reply to', 'Retweet', 'Text', 'Hashtags'])

    def on_status(self, status):
        TwitterStreamListener.collected_tweets += 1                                     # count respective tweets

        try:
            #print(TwitterStreamListener.collected_tweets, TwitterStreamListener.num_tweets, status.text)

            # saving all data (count, date, author, id, reply_to, retweet, text, hashtags) to csv
            with open('twitter_bullying.csv', 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow([TwitterStreamListener.num_tweets, status.created_at, status.author.screen_name, status.id, status.in_reply_to_screen_name,
                                 status.retweeted, status.text, status.entities.get('hashtags')])

        except Exception as e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

        # to test the function, the stream will be stopped after a certain number of tweets was collected
        if TwitterStreamListener.num_tweets < 10001:
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

# terms = ['disney', 'pixar']        # example topics

# hashtags that are related to cyberbullying / hate speech
terms = ['bully', 'bullying', 'blacklivesmatter', 'banIslam', 'stopIslam', 'rapefugees', 'whitelivesmatter',
         'IfMySonWasGay', 'IfMyDaughterBroughtHomeABlack', 'ADeadJew', 'AGoodJew', 'IfIWereANazi', 'SignsYoSonIsGay',
         'HowToTurnDownAUglyPerson', 'HeterosexualPrideDay', 'whitenesstoldme', 'onlyintheghetto', 'ifsantawasblack', 'notracist']
# source: https://www.demos.co.uk/project/anti-islamic-content-on-twitter/, https://www.hollywoodreporter.com/news/france-twitter-hate-speech-hashtags-410664,
# https://www.glaad.org/blog/spiritday-inspires-twitter-users-reclaim-homophobic-hashtag, https://bust.com/feminism/8762-awesome-twitter-users-take-over-homophobic-hashtag.html,
# https://www.theguardian.com/world/2017/jun/30/heterosexualprideday-backfires-lgbt-users-subvert-twitter, https://www.sbs.com.au/topics/life/culture/article/2018/05/21/twitter-hashtag-calling-out-whiteness,
# https://www.lwbooks.co.uk/new-formations/78/black-twitter-racial-hashtags-networks-and-contagion, https://www.researchgate.net/publication/303868342_notracist_Exploring_Racism_Denial_Talk_on_Twitter

# only english tweets
streaming_api.filter(languages=["en"], track=terms)

# english and german tweets
#streaming_api.filter(languages=["en", "ger"], track=terms)
