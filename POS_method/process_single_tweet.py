import nltk

from POS_method.POS_test import prepare_POS_text, POS_specials_all
from POS_method.build_single_vector import build_vector

text = "I hate Lisa!!!"


def process_single_tweet(tweet):

    # 1. clean tweet
    clean_tweet = prepare_POS_text(tweet)
    #2. pos_tag tweet

    test_postags = nltk.pos_tag(clean_tweet)
    #3. tag special words
    special_tags = ','.join((POS_specials_all(test_postags)))
    tags_split = special_tags.split(",")
    #4. build vector
    vector = build_vector(tags_split)


    # with open('POS_method/POS_Testdaten_compare.csv', 'a') as c:
    #     writer2 = csv.writer(c, delimiter=';')
    #     writer2.writerow([tweet, tags_split, vector])
    return vector

#print(process_single_tweet(text))