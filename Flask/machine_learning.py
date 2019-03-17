import ml_processing
import svm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# TODO: training_list should be created when the chat is being loaded to avoid creating it over and over
training_list = ml_processing.process_data("train_set.csv")

# TODO: all matrices should be created when the chat is being loaded to avoid creating them over and over
matrix_pos = svm.do_matrix(training_list, "lexicon_pos.txt")
matrix_neut = svm.do_matrix(training_list, "lexicon_neut.txt")
matrix_neg = svm.do_matrix(training_list, "lexicon_neg.txt")

# we use Vader to determine the sentiment of each chat message as SentiStrength cannot be used for the chat messages
def determine_sentiment(message):
    analyzer = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer gives a sentiment dictionary which contains pos, neg, neu, and compound scores
    score = analyzer.polarity_scores(message)

    # decide if sentiment is positive, negative or neutral
    sentiment = ""
    if score['compound'] >= 0.05:
        sentiment = "positive"

    elif score['compound'] <= - 0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return sentiment

def use_svm(message):
    file = "train_set.csv"
    cb_column = 7
    hs_column = 9
    lex_pos = "lexicon_pos.txt"
    lex_neut = "lexicon_neut.txt"
    lex_neg = "lexicon_neg.txt"

    utterance = ml_processing.process_utterance(message)

    # use lexicon with positive, neutral or negative vocabulary based on the sentiment of the utterance
    sentiment = determine_sentiment(message)
    if sentiment == "positive":
        class_cb = svm.do_svm(training_list, lex_pos, utterance, file, cb_column, matrix_pos)
        class_hs = svm.do_svm(training_list, lex_pos, utterance, file, hs_column, matrix_pos)
    elif sentiment == "negative":
        class_cb = svm.do_svm(training_list, lex_neut, utterance, file, cb_column, matrix_neut)
        class_hs = svm.do_svm(training_list, lex_neut, utterance, file, hs_column, matrix_neut)
    else:
        class_cb = svm.do_svm(training_list, lex_neg, utterance, file, cb_column, matrix_neg)
        class_hs = svm.do_svm(training_list, lex_neg, utterance, file, hs_column, matrix_neg)

    class_list = [class_cb, class_hs]
    return class_list