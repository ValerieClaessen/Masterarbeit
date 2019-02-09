import csv

import tweepy
from tweepy import OAuthHandler

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# We will use Tweepy to crawl tweets from Twitter
# start tweepy with a wait_on_rate_limit, so it won't stop after the limit of looked up tweets is reached
api = tweepy.API(auth, wait_on_rate_limit=True)

# create csv file that will contain all found tweets
with open('twitter_bullying_archive7.csv', 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')

    # header
    writer.writerow(['Tweet', 'Created at', 'User', 'ID', 'Reply to', 'Retweet', 'Text', 'Hashtags'])

num_tweets = 1

# hashtags related to cyberbullying / hate speech
# source: https://www.demos.co.uk/project/anti-islamic-content-on-twitter/, https://www.hollywoodreporter.com/news/france-twitter-hate-speech-hashtags-410664,
# https://www.glaad.org/blog/spiritday-inspires-twitter-users-reclaim-homophobic-hashtag, https://bust.com/feminism/8762-awesome-twitter-users-take-over-homophobic-hashtag.html,
# https://www.theguardian.com/world/2017/jun/30/heterosexualprideday-backfires-lgbt-users-subvert-twitter, https://www.sbs.com.au/topics/life/culture/article/2018/05/21/twitter-hashtag-calling-out-whiteness,
# https://www.lwbooks.co.uk/new-formations/78/black-twitter-racial-hashtags-networks-and-contagion, https://www.researchgate.net/publication/303868342_notracist_Exploring_Racism_Denial_Talk_on_Twitter
hashtags = "#bully OR #bullying OR #blacklivesmatter OR #banIslam OR #stopIslam OR #rapefugees OR #whitelivesmatter OR #IfMySonWasGay OR #IfMyDaughterBroughtHomeABlack OR #ADeadJew OR #AGoodJew OR #IfIWereANazi OR #SignsYoSonIsGay OR #HowToTurnDownAUglyPerson OR #HeterosexualPrideDay OR #whitenesstoldme OR #onlyintheghetto OR #ifsantawasblack OR #notracist"

# search twitter archive from a certain date up to a more recent date
for tweet in tweepy.Cursor(api.search,q=hashtags,
                           lang="en",
                           since="2018-11-28",
                           until="2018-11-30").items(40000):        # set a limit of tweets that should be collected
    #print (num_tweets, tweet.text)

    # saving all data (count, date, author, id, reply_to, retweet, text, hashtags) to csv
    with open('twitter_bullying_archive7.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([num_tweets, tweet.created_at, tweet.author.screen_name, tweet.id,
                         tweet.in_reply_to_screen_name,
                         tweet.retweeted, tweet.text, tweet.entities.get('hashtags')])
        num_tweets += 1
