import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import machine_learning_processing

# function to write all utterances into a txt file to use with SentiStrength
def utterances_into_txt(file, filename):
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)                                  # skip header

        with open(filename, 'w') as f2:
            for row in reader:
                f2.write("%s\n" % row[5])                   # one row per utterance

#utterances_into_txt("train_set.csv", "train_set.txt")
#utterances_into_txt("test_set.csv", "test_set.txt")
#utterances_into_txt("train_cb_set.csv", "train_cb_set.txt")
#utterances_into_txt("test_cb_set.csv", "test_cb_set.txt")
#utterances_into_txt("bullying_traces_train.csv", "bullying_traces_train.txt")
#utterances_into_txt("bullying_traces_test.csv", "bullying_traces_test.txt")
#utterances_into_txt("labeled_data_train.csv", "labeled_data_train.txt")
#utterances_into_txt("labeled_data_test.csv", "labeled_data_test.txt")
#utterances_into_txt("twitter_hate_speech_train.csv", "twitter_hate_speech_train.txt")
#utterances_into_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_test.txt")

# function to save results of SentiStrength into csv file
def sentiment_into_csv(file, filename):
    with open(file, "r") as f:
        reader = csv.reader(f, delimiter='\t')

        with open(filename, "w") as f2:
            writer = csv.writer(f2, delimiter=';')
            for row in reader:
                writer.writerow(row)

#sentiment_into_csv("train_set_sentiment.txt", "train_set_sentiment.csv")
#sentiment_into_csv("test_set_sentiment.txt", "test_set_sentiment.csv")
#sentiment_into_csv("train_cb_set_sentiment.txt", "train_cb_set_sentiment.csv")
#sentiment_into_csv("test_cb_set_sentiment.txt", "test_cb_set_sentiment.csv")
#sentiment_into_csv("bullying_traces_train_sentiment.txt", "bullying_traces_train_sentiment.csv")
#sentiment_into_csv("bullying_traces_test_sentiment.txt", "bullying_traces_test_sentiment.csv")
#sentiment_into_csv("labeled_data_train_sentiment.txt", "labeled_data_train_sentiment.csv")
#sentiment_into_csv("labeled_data_test_sentiment.txt", "labeled_data_test_sentiment.csv")
#sentiment_into_csv("twitter_hate_speech_train_sentiment.txt", "twitter_hate_speech_train_sentiment.csv")
#sentiment_into_csv("twitter_hate_speech_test_sentiment.txt", "twitter_hate_speech_test_sentiment.csv")

# function to estimate the sentiment based on SentiStrength assigned positive and negative values
def estimate_sentiment(file, filename):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                                              # skip header

        with open(filename, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(["Utterance", "Sentiment", "Positive", "Negative", "Emotion Rationale"])    # header

            sentiment = 0
            for row in reader:
                result = int(row[1]) + int(row[2])          # sum of the positive value (e.g. 2) and negative value (e.g. -3)
                if result > 0:                              # the sentiment is positive (1) if the result is a positive value
                    sentiment = 1
                elif result < 0:                            # the sentiment is negative (-1) if the result is a negative value
                    sentiment = -1
                else:                                       # the sentiment is neutral (0) if the result is 0
                    sentiment = 0

                writer.writerow([row[0], sentiment, row[1], row[2], row[3]])

#estimate_sentiment("train_set_sentiment.csv", "train_set_with_sentiment.csv")
#estimate_sentiment("test_set_sentiment.csv", "test_set_with_sentiment.csv")
#estimate_sentiment("train_cb_set_sentiment.csv", "train_cb_set_with_sentiment.csv")
#estimate_sentiment("test_cb_set_sentiment.csv", "test_cb_set_with_sentiment.csv")
#estimate_sentiment("bullying_traces_train_sentiment.csv", "bullying_traces_train_with_sentiment.csv")
#estimate_sentiment("bullying_traces_test_sentiment.csv", "bullying_traces_test_with_sentiment.csv")
#estimate_sentiment("labeled_data_train_sentiment.csv", "labeled_data_train_with_sentiment.csv")
#estimate_sentiment("labeled_data_test_sentiment.csv", "labeled_data_test_with_sentiment.csv")
#estimate_sentiment("twitter_hate_speech_train_sentiment.csv", "twitter_hate_speech_train_with_sentiment.csv")
#estimate_sentiment("twitter_hate_speech_test_sentiment.csv", "twitter_hate_speech_test_with_sentiment.csv")

# function to estimate the probability of an utterance with a specific sentiment to be in class cyberbullying / no_cyberbullying
# return a list of all probabilities (sentiment_list)
def estimate_sentiment_probabilities(sentimentfile, cbfile, cbrow):
    cb_list = machine_learning_processing.make_list_of_column(cbfile, cbrow)    # list of cyberbullying values

    count_pos = 0                                           # number of positive utterances
    count_neut = 0                                          # number of neutral utterances
    count_neg = 0                                           # number of negative utterances

    pos_cb = 0                                              # number of positive utterances in class cyberbullying
    pos_no_cb = 0                                           # number of positive utterances in class no_cyberbullying
    neut_cb = 0                                             # number of neutral utterances in class cyberbullying
    neut_no_cb = 0                                          # number of neutral utterances in class no_cyberbullying
    neg_cb = 0                                              # number of negative utterances in class cyberbullying
    neg_no_cb = 0                                           # number of negative utterances in class no_cyberbullying

    with open(sentimentfile, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader, None)                                  # skip header

        utterance_id = 0
        for row in reader:
            if row[1] == 1 or row[1] == "1":
                count_pos += 1

                if cb_list[utterance_id] == 1 or cb_list[utterance_id] == "1":
                    pos_cb += 1
                else:
                    pos_no_cb += 1
            elif row[1] == -1 or row[1] == "-1":
                count_neg += 1

                if cb_list[utterance_id] == 1 or cb_list[utterance_id] == "1":
                    neg_cb += 1
                else:
                    neg_no_cb += 1
            else:
                count_neut += 1

                if cb_list[utterance_id] == 1 or cb_list[utterance_id] == "1":
                    neut_cb += 1
                else:
                    neut_no_cb += 1

            utterance_id += 1

    #print(count_pos, count_neut, count_neg)
    #print(pos_cb, pos_no_cb, neut_cb, neut_no_cb, neg_cb, neut_no_cb)

    p_pos_cb = pos_cb / count_pos                           # probability of a positive utterance being in class cyberbullying
    p_pos_no_cb = pos_no_cb / count_pos                     # probability of a positive utterance being in class no_cyberbullying
    p_neut_cb = neut_cb / count_neut                        # probability of a neutral utterance being in class cyberbullying
    p_neut_no_cb = neut_no_cb / count_neut                  # probability of a neutral utterance being in class no_cyberbullying
    p_neg_cb = neg_cb / count_neg                           # probability of a negative utterance being in class cyberbullying
    p_neg_no_cb = neg_no_cb / count_neg                     # probability of a negative utterance being in class no_cyberbullying

    p_pos_cb = round(p_pos_cb, 3)                           # round probabilities to values with 3 positions behind decimal point
    p_pos_no_cb = round(p_pos_no_cb, 3)
    p_neut_cb = round(p_neut_cb, 3)
    p_neut_no_cb = round(p_neut_no_cb, 3)
    p_neg_cb = round(p_neg_cb, 3)
    p_neg_no_cb = round(p_neg_no_cb, 3)

    sentiment_list = [p_pos_cb, p_pos_no_cb, p_neut_cb, p_neut_no_cb, p_neg_cb, p_neg_no_cb]
    return sentiment_list

# function to estimate the probability of an utterance with a specific sentiment to be in class s1-s5
# return a list of all probabilities (sentiment_list)
def estimate_sentiment_probabilities_strengths(sentimentfile, cbfile, cbrow):
    strength_list = machine_learning_processing.make_list_of_column(cbfile, cbrow)    # list of cyberbullying values

    count_pos = 0                                           # number of positive utterances
    count_neut = 0                                          # number of neutral utterances
    count_neg = 0                                           # number of negative utterances

    pos_s1 = 0                                              # number of positive utterances in class s1
    pos_s2 = 0
    pos_s3 = 0
    pos_s4 = 0
    pos_s5 = 0

    neut_s1 = 0                                             # number of neutral utterances in class s1
    neut_s2 = 0
    neut_s3 = 0
    neut_s4 = 0
    neut_s5 = 0

    neg_s1 = 0                                              # number of negative utterances in class s1
    neg_s2 = 0
    neg_s3 = 0
    neg_s4 = 0
    neg_s5 = 0

    with open(sentimentfile, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                  # skip header

        utterance_id = 0
        for row in reader:
            if row[1] == 1 or row[1] == "1":
                count_pos += 1

                if strength_list[utterance_id] == 1 or strength_list[utterance_id] == "1":
                    pos_s1 += 1
                elif strength_list[utterance_id] == 2 or strength_list[utterance_id] == "2":
                    pos_s2 += 1
                elif strength_list[utterance_id] == 3 or strength_list[utterance_id] == "3":
                    pos_s3 += 1
                elif strength_list[utterance_id] == 4 or strength_list[utterance_id] == "4":
                    pos_s4 += 1
                else:
                    pos_s5 += 1
            elif row[1] == -1 or row[1] == "-1":
                count_neg += 1

                if strength_list[utterance_id] == 1 or strength_list[utterance_id] == "1":
                    neg_s1 += 1
                elif strength_list[utterance_id] == 2 or strength_list[utterance_id] == "2":
                    neg_s2 += 1
                elif strength_list[utterance_id] == 3 or strength_list[utterance_id] == "3":
                    neg_s3 += 1
                elif strength_list[utterance_id] == 4 or strength_list[utterance_id] == "4":
                    neg_s4 += 1
                else:
                    neg_s5 += 1
            else:
                count_neut += 1

                if strength_list[utterance_id] == 1 or strength_list[utterance_id] == "1":
                    neut_s1 += 1
                elif strength_list[utterance_id] == 2 or strength_list[utterance_id] == "2":
                    neut_s2 += 1
                elif strength_list[utterance_id] == 3 or strength_list[utterance_id] == "3":
                    neut_s3 += 1
                elif strength_list[utterance_id] == 4 or strength_list[utterance_id] == "4":
                    neut_s4 += 1
                else:
                    neut_s5 += 1

            utterance_id += 1

    #print(count_pos, count_neut, count_neg)
    #print(pos_s1, pos_s2, pos_s3, pos_s4, pos_s5)
    #print(neut_s1,neut_s2,neut_s3,neut_s4,neut_s5)
    #print(neg_s1, neg_s2, neg_s3, neg_s4, neg_s5)

    p_pos_s1 = pos_s1 / count_pos                           # probability of a positive utterance being in class s1
    p_pos_s2 = pos_s2 / count_pos
    p_pos_s3 = pos_s3 / count_pos
    p_pos_s4 = pos_s4 / count_pos
    p_pos_s5 = pos_s5 / count_pos
    p_neut_s1 = neut_s1 / count_neut                        # probability of a neutral utterance being in class s1
    p_neut_s2 = neut_s2 / count_neut
    p_neut_s3 = neut_s3 / count_neut
    p_neut_s4 = neut_s4 / count_neut
    p_neut_s5 = neut_s5 / count_neut
    p_neg_s1 = neg_s1 / count_neg                           # probability of a negative utterance being in class s1
    p_neg_s2 = neg_s2 / count_neg
    p_neg_s3 = neg_s3 / count_neg
    p_neg_s4 = neg_s4 / count_neg
    p_neg_s5 = neg_s5 / count_neg

    p_pos_s1 = round(p_pos_s1, 3)                           # round probabilities to values with 3 positions behind decimal point
    p_pos_s2 = round(p_pos_s2, 3)
    p_pos_s3 = round(p_pos_s3, 3)
    p_pos_s4 = round(p_pos_s4, 3)
    p_pos_s5 = round(p_pos_s5, 3)
    p_neut_s1 = round(p_neut_s1, 3)
    p_neut_s2 = round(p_neut_s2, 3)
    p_neut_s3 = round(p_neut_s3, 3)
    p_neut_s4 = round(p_neut_s4, 3)
    p_neut_s5 = round(p_neut_s5, 3)
    p_neg_s1 = round(p_neg_s1, 3)
    p_neg_s2 = round(p_neg_s2, 3)
    p_neg_s3 = round(p_neg_s3, 3)
    p_neg_s4 = round(p_neg_s4, 3)
    p_neg_s5 = round(p_neg_s5, 3)

    sentiment_list = [p_pos_s1, p_pos_s2, p_pos_s3, p_pos_s4, p_pos_s5, p_neut_s1, p_neut_s2, p_neut_s3, p_neut_s4, p_neut_s5, p_neg_s1, p_neg_s2, p_neg_s3, p_neg_s4, p_neg_s5]
    return sentiment_list

# function to estimate the probability of an utterance with a specific sentiment to be in class cyberbullying / no_cyberbullying
# return a list of all probabilities (sentiment_list)
def estimate_sentiment_probabilities_other_datasets(sentimentfile, cbfile, cbrow, mode):
    cb_list = machine_learning_processing.make_list_of_column(cbfile, cbrow)    # list of cyberbullying values

    count_pos = 0                                           # number of positive utterances
    count_neut = 0                                          # number of neutral utterances
    count_neg = 0                                           # number of negative utterances

    pos_cb = 0                                              # number of positive utterances in class cyberbullying
    pos_no_cb = 0                                           # number of positive utterances in class no_cyberbullying
    neut_cb = 0                                             # number of neutral utterances in class cyberbullying
    neut_no_cb = 0                                          # number of neutral utterances in class no_cyberbullying
    neg_cb = 0                                              # number of negative utterances in class cyberbullying
    neg_no_cb = 0                                           # number of negative utterances in class no_cyberbullying

    with open(sentimentfile, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                  # skip header

        utterance_id = 0
        for row in reader:
            if row[1] == 1 or row[1] == "1":
                count_pos += 1

                if mode == 2:
                    if cb_list[utterance_id] == 1 or cb_list[utterance_id] == "1":
                        pos_cb += 1
                    elif cb_list[utterance_id] == 0 or cb_list[utterance_id] == "0":
                        pos_cb += 1
                    else:
                        pos_no_cb += 1
                else:
                    if cb_list[utterance_id] == 1 or cb_list[utterance_id] == "1":
                        pos_cb += 1
                    elif cb_list[utterance_id] == 2 or cb_list[utterance_id] == "2":
                        pos_cb += 1
                    else:
                        pos_no_cb += 1
            elif row[1] == -1 or row[1] == "-1":
                count_neg += 1

                if mode == 2:
                    if cb_list[utterance_id] == 1 or cb_list[utterance_id] == "1":
                        neg_cb += 1
                    elif cb_list[utterance_id] == 0 or cb_list[utterance_id] == "0":
                        neg_cb += 1
                    else:
                        neg_no_cb += 1
                else:
                    if cb_list[utterance_id] == 1 or cb_list[utterance_id] == "1":
                        neg_cb += 1
                    elif cb_list[utterance_id] == 2 or cb_list[utterance_id] == "2":
                        neg_cb += 1
                    else:
                        neg_no_cb += 1
            else:
                count_neut += 1

                if mode == 2:
                    if cb_list[utterance_id] == 1 or cb_list[utterance_id] == "1":
                        neut_cb += 1
                    elif cb_list[utterance_id] == 0 or cb_list[utterance_id] == "0":
                        neut_cb += 1
                    else:
                        neut_no_cb += 1
                else:
                    if cb_list[utterance_id] == 1 or cb_list[utterance_id] == "1":
                        neut_cb += 1
                    elif cb_list[utterance_id] == 2 or cb_list[utterance_id] == "2":
                        neut_cb += 1
                    else:
                        neut_no_cb += 1

            utterance_id += 1

    #print(count_pos, count_neut, count_neg)
    #print(pos_cb, pos_no_cb, neut_cb, neut_no_cb, neg_cb, neut_no_cb)

    p_pos_cb = pos_cb / count_pos                           # probability of a positive utterance being in class cyberbullying
    p_pos_no_cb = pos_no_cb / count_pos                     # probability of a positive utterance being in class no_cyberbullying
    p_neut_cb = neut_cb / count_neut                        # probability of a neutral utterance being in class cyberbullying
    p_neut_no_cb = neut_no_cb / count_neut                  # probability of a neutral utterance being in class no_cyberbullying
    p_neg_cb = neg_cb / count_neg                           # probability of a negative utterance being in class cyberbullying
    p_neg_no_cb = neg_no_cb / count_neg                     # probability of a negative utterance being in class no_cyberbullying

    p_pos_cb = round(p_pos_cb, 3)                           # round probabilities to values with 3 positions behind decimal point
    p_pos_no_cb = round(p_pos_no_cb, 3)
    p_neut_cb = round(p_neut_cb, 3)
    p_neut_no_cb = round(p_neut_no_cb, 3)
    p_neg_cb = round(p_neg_cb, 3)
    p_neg_no_cb = round(p_neg_no_cb, 3)

    sentiment_list = [p_pos_cb, p_pos_no_cb, p_neut_cb, p_neut_no_cb, p_neg_cb, p_neg_no_cb]
    return sentiment_list

#sentiment_list = estimate_sentiment_probabilities("train_set_with_sentiment.csv", "train_set.csv", 7)
#print(sentiment_list)

# hate speech
#sentiment_list = estimate_sentiment_probabilities("train_set_with_sentiment.csv", "train_set.csv", 9)
#print(sentiment_list)

# strength
#sentiment_list = estimate_sentiment_probabilities_strengths("train_cb_set_with_sentiment.csv", "train_cb_set.csv", 8)
#print(sentiment_list)

def make_lex_based_on_sent(sentimentfile, trainfile, lexname, sentiment, mode, class_column):
    lex = []

    sentiment_list = machine_learning_processing.make_list_of_column(sentimentfile, 1)

    data_list = machine_learning_processing.process_data(trainfile, class_column)

    utterance_id = 0
    for list in data_list:
        if sentiment_list[utterance_id] == sentiment or sentiment_list[utterance_id] == str(sentiment):
            for word in list:
                if word not in lex:
                    lex.append(word)
                #else:
                    #print("already in lexicon")
        utterance_id += 1

    lex = sorted(lex)                                                       # sort list alphabetically

    # only words that occur at least twice in the dataset will be part of the lexicon
    lex2 = []
    for word in lex:
        count = sum(x.count(word) for x in data_list)
        if count > 1:
            lex2.append(word)

    with open(lexname, 'w') as f:
        if mode == 1:
            for word in lex:
                f.write("%s\n" % word)
        else:
            for word in lex2:
                f.write("%s\n" % word)

#make_lex_based_on_sent("train_set_with_sentiment.csv", "train_set.csv", "lexicon_pos.txt", 1, 1)
#make_lex_based_on_sent("train_set_with_sentiment.csv", "train_set.csv", "lexicon_neg.txt", -1, 1)
#make_lex_based_on_sent("train_set_with_sentiment.csv", "train_set.csv", "lexicon_neut.txt", 0, 1)

#make_lex_based_on_sent("train_set_with_sentiment.csv", "train_set.csv", "lexicon_pos2.txt", 1, 0)
#make_lex_based_on_sent("train_set_with_sentiment.csv", "train_set.csv", "lexicon_neg2.txt", -1, 0)
#make_lex_based_on_sent("train_set_with_sentiment.csv", "train_set.csv", "lexicon_neut2.txt", 0, 0)

# strength
#make_lex_based_on_sent("train_cb_set_with_sentiment.csv", "train_cb_set.csv", "lexicon_pos_cb.txt", 1, 1, 5)
#make_lex_based_on_sent("train_cb_set_with_sentiment.csv", "train_cb_set.csv", "lexicon_neg_cb.txt", -1, 1, 5)
#make_lex_based_on_sent("train_cb_set_with_sentiment.csv", "train_cb_set.csv", "lexicon_neut_cb.txt", 0, 1, 5)

#make_lex_based_on_sent("bullying_traces_train_with_sentiment.csv", "bullying_traces_train.csv", "lexicon_pos_bt.txt", 1, 1, 2)
#make_lex_based_on_sent("bullying_traces_train_with_sentiment.csv", "bullying_traces_train.csv", "lexicon_neg_bt.txt", -1, 1, 2)
#make_lex_based_on_sent("bullying_traces_train_with_sentiment.csv", "bullying_traces_train.csv", "lexicon_neut_bt.txt", 0, 1, 2)

#make_lex_based_on_sent("labeled_data_train_with_sentiment.csv", "labeled_data_train.csv", "lexicon_pos_ld.txt", 1, 1, 6)
#make_lex_based_on_sent("labeled_data_train_with_sentiment.csv", "labeled_data_train.csv", "lexicon_neg_ld.txt", -1, 1, 6)
#make_lex_based_on_sent("labeled_data_train_with_sentiment.csv", "labeled_data_train.csv", "lexicon_neut_ld.txt", 0, 1, 6)

#make_lex_based_on_sent("twitter_hate_speech_train_with_sentiment.csv", "twitter_hate_speech_train.csv", "lexicon_pos_ths.txt", 1, 1, 1)
#make_lex_based_on_sent("twitter_hate_speech_train_with_sentiment.csv", "twitter_hate_speech_train.csv", "lexicon_neg_ths.txt", -1, 1, 1)
#make_lex_based_on_sent("twitter_hate_speech_train_with_sentiment.csv", "twitter_hate_speech_train.csv", "lexicon_neut_ths.txt", 0, 1, 1)
