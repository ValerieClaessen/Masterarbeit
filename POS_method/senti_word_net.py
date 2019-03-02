import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
text = "Donald Trump is an Ass and a coward, I HATE him, ban Islam"
split_text = text.split()
print("Vollständiger Satz: 3", text)
#test_subset=[split_text]

sid = SentimentIntensityAnalyzer()
pos_word_list=[]
neu_word_list=[]
neg_word_list=[]

# for word in split_text:
#     if (sid.polarity_scores(word)['compound']) >= 0.5:
#         pos_word_list.append(word)
#     elif (sid.polarity_scores(word)['compound']) <= -0.5:
#         neg_word_list.append(word)
#     else:
#         neu_word_list.append(word)
#
# print('Positive :',pos_word_list)
# print('Neutral :',neu_word_list)
# print('Negative :',neg_word_list)


def analyze_sentiment(token):

    neg_sentiment = False
    if (sid.polarity_scores(token)['compound']) <= -0.5:
        neg_sentiment = True
    #print(sid.polarity_scores(token)['compound'])
    return neg_sentiment

print(analyze_sentiment("hate"))
