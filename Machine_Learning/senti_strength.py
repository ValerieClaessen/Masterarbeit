import csv
import machine_learning_processing

# function to make a list of all values from a column from a dataset
def make_list_of_column(file, column):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)  # skip header

        list = []
        for row in reader:
            list.append(row[column])

    return list

# function to write all utterances into a txt file to use with SentiStrength
def utterances_into_txt(file, filename):
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)                                  # skip header

        with open(filename, 'w') as f2:
            for row in reader:
                f2.write("%s\n" % row[5])                   # one row per utterance

#utterances_into_txt("train_set.csv", "train_set.txt")

# function to save results of SentiStrength into csv file
def sentiment_into_csv(file, filename):
    with open(file, "r") as f:
        reader = csv.reader(f, delimiter='\t')

        with open(filename, "w") as f2:
            writer = csv.writer(f2, delimiter=';')
            for row in reader:
                writer.writerow(row)

#sentiment_into_csv("train_set_sentiment.txt", "train_set_sentiment.csv")

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

# function to estimate the probability of an utterance with a specific sentiment to be in class cyberbullying / no_cyberbullying
# return a list of all probabilities (sentiment_list)
def estimate_sentiment_probabilities(sentimentfile, cbfile, cbrow):
    cb_list = make_list_of_column(cbfile, cbrow)    # list of cyberbullying values

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

#sentiment_list = estimate_sentiment_probabilities("train_set_with_sentiment.csv", "train_set.csv", 7)
#print(sentiment_list)

def make_lex_based_on_sent(sentimentfile, trainfile, lexname, sentiment):
    lex = []

    sentiment_list = make_list_of_column(sentimentfile, 1)
    print(sentiment_list)

    data_list = machine_learning_processing.process_data(trainfile)
    print(data_list)

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

    with open(lexname, 'w') as f:
        for word in lex:
            f.write("%s\n" % word)

make_lex_based_on_sent("train_list_with_sentiment.csv", "train_set.csv", "lexicon_pos.txt", 1)
#make_lex_based_on_sent("train_list_with_sentiment.csv", "train_set.csv", "lexicon_neg.txt", -1)
#make_lex_based_on_sent("train_list_with_sentiment.csv", "train_set.csv", "lexicon_neut.txt", 0)
