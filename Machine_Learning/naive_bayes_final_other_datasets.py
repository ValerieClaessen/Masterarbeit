import csv
import machine_learning_processing
import estimation
import senti_strength
import compare_labeled_data
import compare_twitter_bullying

# global variables
freq_cb = 0
freq_no_cb = 0
freq_hs = 0
freq_no_hs = 0

# function to estimate the frequencies of each cyberbullying class in the training dataset
def estimate_class_frequency_other_datasets(file, mode):
    """
    Bullying Traces:        Utterance in row[2], Cyberbullying in row[3] with 1 = Cyberbullying, 0 = no Cyberbullying; Mode: 1

    Labeled Data:           Utterance in row[6], Class in row[5] with Hate Speech = 0, Offensive Language = 1 and neither = 2.
                            Cyberbullying are all utterances with class 0 and 1. Mode: 2

    Twitter Hate Speech:    Utterance in row[1], Class in row[2] with Hate Speech = 2, Offensive Language = 1 and neither = 0.
                            Cyberbullying are all utterances with class 2 and 1. Mode: 3
    """

    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                  # skip header

        cyberbullying = 0
        no_cyberbullying = 0
        utterances = 0

        # count utterances that are labeled as cyberbuylling / no_cyberbullying
        if mode == 1:
            for row in reader:
                if row[3] == 1 or row[3] == "1":
                    cyberbullying += 1
                else:
                    no_cyberbullying += 1
                utterances += 1
        elif mode == 2:
            for row in reader:
                if row[5] == 1 or row[5] == "1":
                    cyberbullying += 1
                elif row[5] == 0 or row[5] == "0":
                    cyberbullying += 1
                else:
                    no_cyberbullying += 1
                utterances += 1
        else:
            for row in reader:
                if row[2] == 1 or row[2] == "1":
                    cyberbullying += 1
                elif row[2] == 2 or row[2] == "2":
                    cyberbullying += 1
                else:
                    no_cyberbullying += 1
                utterances += 1

        global freq_cb
        freq_cb = cyberbullying / utterances                # frequency of utterances that are labeled as cyberbullying
        global freq_no_cb
        freq_no_cb = no_cyberbullying / utterances          # frequency of utterances that are labeled as no_cyberbullying

# function to estimate the frequencies of each hate speech class in the training dataset
def estimate_hate_speech_frequency_other_datasets(file, mode):
    """
    Labeled Data:           Utterance in row[6], Class in row[5] with Hate Speech = 0, Offensive Language = 1 and neither = 2.
                            Cyberbullying are all utterances with class 0 and 1. Mode: 2

    Twitter Hate Speech:    Utterance in row[1], Class in row[2] with Hate Speech = 2, Offensive Language = 1 and neither = 0.
                            Cyberbullying are all utterances with class 2 and 1. Mode: 3
    """

    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                  # skip header

        hate_speech = 0
        no_hatespeech = 0
        utterances = 0

        # count utterances that are labeled as hate speech / no hate speech
        if mode == 2:
            for row in reader:
                if row[5] == 0 or row[5] == "0":
                    hate_speech += 1
                else:
                    no_hatespeech += 1
                utterances += 1
        else:
            for row in reader:
                if row[2] == 2 or row[2] == "2":
                    hate_speech += 1
                else:
                    no_hatespeech += 1
                utterances += 1

        global freq_hs
        freq_hs = hate_speech / utterances                # frequency of utterances that are labeled as cyberbullying
        global freq_no_hs
        freq_no_hs = no_hatespeech / utterances          # frequency of utterances that are labeled as no_cyberbullying

#function to use the naive bayes algorithm with sentiment on an utterance of the test_set
# returns the cyberbullying class for the utterances assigned by the algorithm
def do_naive_bayes_sent_pos_ld(utterance, utterance_unprocessed, lex, sentiment, sentimentlist):
    p_utterance_class_1 = 1  # p(tweet|class)
    p_utterance_class_0 = 1

    contains_curses = False
    curses = machine_learning_processing.make_list_of_curse_words("curses.txt")

    for word in utterance:
        if word in curses:
            contains_curses = True                                      # utterances that contain curses will automatically be labeled as cyberbullying later

        for line in open(lex):
            if word in line:
                line_split = line.split()

                # multiply each word frequency in the respective class
                # with laplace smoothing
                p_utterance_class_1 *= float(line_split[1])
                p_utterance_class_0 *= float(line_split[2])

    p_pos_cb = sentimentlist[0]
    p_pos_no_cb = sentimentlist[1]
    p_neut_cb = sentimentlist[2]
    p_neut_no_cb = sentimentlist[3]
    p_neg_cb = sentimentlist[4]
    p_neg_no_cb = sentimentlist[5]

    # multiply p(tweet|class) with p(class) (freq_cb / freq_no_cb) and multiply by sentiment probability in regard to utterance's sentiment
    p_class_utterance_0 = 0
    p_class_utterance_1 = 0

    if sentiment == 1 or sentiment == "1":
        p_class_utterance_1 = p_utterance_class_1 * freq_cb * p_pos_cb
        p_class_utterance_0 = p_utterance_class_0 * freq_no_cb * p_pos_no_cb
    elif sentiment == 0 or sentiment == "0":
        p_class_utterance_1 = p_utterance_class_1 * freq_cb * p_neut_cb
        p_class_utterance_0 = p_utterance_class_0 * freq_no_cb * p_neut_no_cb
    else:
        p_class_utterance_1 = p_utterance_class_1 * freq_cb * p_neg_cb * 100000000000000        # more impact if the utterance is negative
        p_class_utterance_0 = p_utterance_class_0 * freq_no_cb * p_neg_no_cb

    # probability that utterance is in class cyberbullying / no cyberbullying based on pos-tagging
    cb_pos_prob = compare_labeled_data.compare_vec_labeled_data_cb(utterance_unprocessed, 3)
    no_cb_pos_prob = 1 - cb_pos_prob
    cb_pos_prob = 2 * cb_pos_prob

    # multiply p_class_utterance by the pos-tag-class-probability
    # if it's zero, multiply by 0.1 to avoid having 0.0 as the final value
    if cb_pos_prob != 0 and no_cb_pos_prob != 0:
        p_class_utterance_1 = p_class_utterance_1 * cb_pos_prob
        p_class_utterance_0 = p_class_utterance_0 * no_cb_pos_prob
    elif cb_pos_prob == 0:
        p_class_utterance_1 = p_class_utterance_1 * 0.1
        p_class_utterance_0 = p_class_utterance_0 * no_cb_pos_prob
    else:
        p_class_utterance_1 = p_class_utterance_1 * cb_pos_prob
        p_class_utterance_0 = p_class_utterance_0 * 0.1

    # class with the higher probability will be assigned to the utterance
    values = [p_class_utterance_1, p_class_utterance_0]
    if max(values) == values[0]:  # determine class (max p(class|tweet))
        class_cb = 1
    elif contains_curses == True:                                                               # utterances that contain curses will automatically be labeled as cyberbullying
        class_cb = 1
    else:
        class_cb = 0

    return class_cb

#function to use the naive bayes algorithm with sentiment on an utterance of the test_set
# returns the cyberbullying class for the utterances assigned by the algorithm
def do_naive_bayes_sent_pos_ths(utterance, utterance_unprocessed, lex, sentiment, sentimentlist):
    p_utterance_class_1 = 1  # p(tweet|class)
    p_utterance_class_0 = 1

    contains_curses = False
    curses = machine_learning_processing.make_list_of_curse_words("curses.txt")

    for word in utterance:
        if word in curses:
            contains_curses = True                                      # utterances that contain curses will automatically be labeled as cyberbullying later

        for line in open(lex):
            if word in line:
                line_split = line.split()

                # multiply each word frequency in the respective class
                # with laplace smoothing
                p_utterance_class_1 *= float(line_split[1])
                p_utterance_class_0 *= float(line_split[2])

    p_pos_cb = sentimentlist[0]
    p_pos_no_cb = sentimentlist[1]
    p_neut_cb = sentimentlist[2]
    p_neut_no_cb = sentimentlist[3]
    p_neg_cb = sentimentlist[4]
    p_neg_no_cb = sentimentlist[5]

    # multiply p(tweet|class) with p(class) (freq_cb / freq_no_cb) and multiply by sentiment probability in regard to utterance's sentiment
    p_class_utterance_0 = 0
    p_class_utterance_1 = 0

    if sentiment == 1 or sentiment == "1":
        p_class_utterance_1 = p_utterance_class_1 * freq_cb * p_pos_cb
        p_class_utterance_0 = p_utterance_class_0 * freq_no_cb * p_pos_no_cb
    elif sentiment == 0 or sentiment == "0":
        p_class_utterance_1 = p_utterance_class_1 * freq_cb * p_neut_cb
        p_class_utterance_0 = p_utterance_class_0 * freq_no_cb * p_neut_no_cb
    else:
        p_class_utterance_1 = p_utterance_class_1 * freq_cb * p_neg_cb * 100000000000000        # more impact if the utterance is negative
        p_class_utterance_0 = p_utterance_class_0 * freq_no_cb * p_neg_no_cb

    # probability that utterance is in class cyberbullying / no cyberbullying based on pos-tagging
    cb_pos_prob = compare_twitter_bullying.compare_vec_twitter_bullying_cb(utterance_unprocessed, 3)
    no_cb_pos_prob = 1 - cb_pos_prob
    cb_pos_prob = 2 * cb_pos_prob

    # multiply p_class_utterance by the pos-tag-class-probability
    # if it's zero, multiply by 0.1 to avoid having 0.0 as the final value
    if cb_pos_prob != 0 and no_cb_pos_prob != 0:
        p_class_utterance_1 = p_class_utterance_1 * cb_pos_prob
        p_class_utterance_0 = p_class_utterance_0 * no_cb_pos_prob
    elif cb_pos_prob == 0:
        p_class_utterance_1 = p_class_utterance_1 * 0.1
        p_class_utterance_0 = p_class_utterance_0 * no_cb_pos_prob
    else:
        p_class_utterance_1 = p_class_utterance_1 * cb_pos_prob
        p_class_utterance_0 = p_class_utterance_0 * 0.1

    # class with the higher probability will be assigned to the utterance
    values = [p_class_utterance_1, p_class_utterance_0]
    if max(values) == values[0]:  # determine class (max p(class|tweet))
        class_cb = 1
    elif contains_curses == True:                                                               # utterances that contain curses will automatically be labeled as cyberbullying
        class_cb = 1
    else:
        class_cb = 0

    return class_cb

#function to use the naive bayes algorithm with sentiment on an utterance of the test_set
# returns the hate speech class for the utterances assigned by the algorithm
def do_naive_bayes_sent_pos_hs_ld(utterance, utterance_unprocessed, lex, sentiment, sentimentlist):
    p_utterance_class_1 = 1  # p(tweet|class)
    p_utterance_class_0 = 1

    for word in utterance:

        for line in open(lex):
            if word in line:
                line_split = line.split()

                # multiply each word frequency in the respective class
                # with laplace smoothing
                p_utterance_class_1 *= float(line_split[1])
                p_utterance_class_0 *= float(line_split[2])

    p_pos_hs = sentimentlist[0]
    p_pos_no_hs = sentimentlist[1]
    p_neut_hs = sentimentlist[2]
    p_neut_no_hs = sentimentlist[3]
    p_neg_hs = sentimentlist[4]
    p_neg_no_hs = sentimentlist[5]

    if sentiment == 1 or sentiment == "1":
        p_class_utterance_1 = p_utterance_class_1 * freq_hs * p_pos_hs
        p_class_utterance_0 = p_utterance_class_0 * freq_no_hs * p_pos_no_hs
    elif sentiment == 0 or sentiment == "0":
        p_class_utterance_1 = p_utterance_class_1 * freq_hs * p_neut_hs
        p_class_utterance_0 = p_utterance_class_0 * freq_no_hs * p_neut_no_hs
    else:
        p_class_utterance_1 = p_utterance_class_1 * freq_hs * p_neg_hs * 100000000000000        # more impact if the utterance is negative
        p_class_utterance_0 = p_utterance_class_0 * freq_no_hs * p_neg_no_hs

    # probability that utterance is in class hate speech / no hate speech based on pos-tagging
    hs_pos_prob = compare_labeled_data.compare_vec_labeled_data_hs(utterance_unprocessed, 5)
    no_hs_pos_prob = 1 - hs_pos_prob
    hs_pos_prob = 2 * hs_pos_prob

    # multiply p_class_utterance by the pos-tag-class-probability
    # if it's zero, multiply by 0.1 to avoid having 0.0 as the final value
    if hs_pos_prob != 0 and no_hs_pos_prob != 0:
        p_class_utterance_1 = p_class_utterance_1 * hs_pos_prob
        p_class_utterance_0 = p_class_utterance_0 * no_hs_pos_prob
    elif hs_pos_prob == 0:
        p_class_utterance_1 = p_class_utterance_1 * 0.1
        p_class_utterance_0 = p_class_utterance_0 * no_hs_pos_prob
    else:
        p_class_utterance_1 = p_class_utterance_1 * hs_pos_prob
        p_class_utterance_0 = p_class_utterance_0 * 0.1

    # class with the higher probability will be assigned to the utterance
    values = [p_class_utterance_1, p_class_utterance_0]
    if max(values) == values[0]:  # determine class (max p(class|tweet))
        class_hs = 1
    else:
        class_hs = 0
    # print(class_hs)

    return class_hs

#function to use the naive bayes algorithm with sentiment on an utterance of the test_set
# returns the hate speech class for the utterances assigned by the algorithm
def do_naive_bayes_sent_pos_hs_ths(utterance, utterance_unprocessed, lex, sentiment, sentimentlist):
    p_utterance_class_1 = 1  # p(tweet|class)
    p_utterance_class_0 = 1

    for word in utterance:

        for line in open(lex):
            if word in line:
                line_split = line.split()

                # multiply each word frequency in the respective class
                # with laplace smoothing
                p_utterance_class_1 *= float(line_split[1])
                p_utterance_class_0 *= float(line_split[2])

    p_pos_hs = sentimentlist[0]
    p_pos_no_hs = sentimentlist[1]
    p_neut_hs = sentimentlist[2]
    p_neut_no_hs = sentimentlist[3]
    p_neg_hs = sentimentlist[4]
    p_neg_no_hs = sentimentlist[5]

    if sentiment == 1 or sentiment == "1":
        p_class_utterance_1 = p_utterance_class_1 * freq_hs * p_pos_hs
        p_class_utterance_0 = p_utterance_class_0 * freq_no_hs * p_pos_no_hs
    elif sentiment == 0 or sentiment == "0":
        p_class_utterance_1 = p_utterance_class_1 * freq_hs * p_neut_hs
        p_class_utterance_0 = p_utterance_class_0 * freq_no_hs * p_neut_no_hs
    else:
        p_class_utterance_1 = p_utterance_class_1 * freq_hs * p_neg_hs * 100000000000000        # more impact if the utterance is negative
        p_class_utterance_0 = p_utterance_class_0 * freq_no_hs * p_neg_no_hs

    # probability that utterance is in class hate speech / no hate speech based on pos-tagging
    hs_pos_prob = compare_twitter_bullying.compare_vec_twitter_bullying_hs(utterance_unprocessed, 5)
    no_hs_pos_prob = 1 - hs_pos_prob
    hs_pos_prob = 2 * hs_pos_prob

    # multiply p_class_utterance by the pos-tag-class-probability
    # if it's zero, multiply by 0.1 to avoid having 0.0 as the final value
    if hs_pos_prob != 0 and no_hs_pos_prob != 0:
        p_class_utterance_1 = p_class_utterance_1 * hs_pos_prob
        p_class_utterance_0 = p_class_utterance_0 * no_hs_pos_prob
    elif hs_pos_prob == 0:
        p_class_utterance_1 = p_class_utterance_1 * 0.1
        p_class_utterance_0 = p_class_utterance_0 * no_hs_pos_prob
    else:
        p_class_utterance_1 = p_class_utterance_1 * hs_pos_prob
        p_class_utterance_0 = p_class_utterance_0 * 0.1

    # class with the higher probability will be assigned to the utterance
    values = [p_class_utterance_1, p_class_utterance_0]
    if max(values) == values[0]:  # determine class (max p(class|tweet))
        class_hs = 1
    else:
        class_hs = 0
    # print(class_hs)

    return class_hs

# function to label a test set using the Naive Bayes algorithm and Sentiment and Pos-Tagging and to save results in a new file for the other datasets
def do_test_set_naive_bayes_sent_pos_ld(utterances, utterances_unprocessed, filename, lex, file, column, sentimentfile_train, sentimentfile_test, mode):
    # annotation using naive_bayes will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying"]) # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities_other_datasets(sentimentfile_train, file, column, mode)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            class_cb = do_naive_bayes_sent_pos_ld(utterance, utterance_unprocessed, lex, list_of_sentiments[utterance_id], sentimentlist)  # determine class of the utterance using do_naive_bayes()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_cb])

            if utterance_id == 100:
                print(100)
            elif utterance_id == 200:
                print(200)
            elif utterance_id == 300:
                print(300)
            elif utterance_id == 400:
                print(400)
            elif utterance_id == 500:
                print(500)
            elif utterance_id == 600:
                print(600)
            elif utterance_id == 700:
                print(700)
            elif utterance_id == 800:
                print(800)
            elif utterance_id == 900:
                print(900)
            elif utterance_id == 1000:
                print(1000)
            elif utterance_id == 1100:
                print(1100)
            elif utterance_id == 1200:
                print(1200)
            elif utterance_id == 1300:
                print(1300)
            elif utterance_id == 1400:
                print(1400)
            elif utterance_id == 1500:
                print(1500)
            elif utterance_id == 1600:
                print(1600)
            elif utterance_id == 1700:
                print(1700)
            elif utterance_id == 1800:
                print(1800)
            elif utterance_id == 1900:
                print(1900)
            elif utterance_id == 2000:
                print(2000)
            elif utterance_id == 2100:
                print(2100)
            elif utterance_id == 2200:
                print(2200)

            utterance_id += 1

# function to label a test set using the Naive Bayes algorithm and Sentiment and Pos-Tagging and to save results in a new file for the other datasets
def do_test_set_naive_bayes_sent_pos_ths(utterances, utterances_unprocessed, filename, lex, file, column, sentimentfile_train, sentimentfile_test, mode):
    # annotation using naive_bayes will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying"]) # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities_other_datasets(sentimentfile_train, file, column, mode)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            class_cb = do_naive_bayes_sent_pos_ths(utterance, utterance_unprocessed, lex, list_of_sentiments[utterance_id], sentimentlist)  # determine class of the utterance using do_naive_bayes()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_cb])

            if utterance_id == 100:
                print(100)
            elif utterance_id == 200:
                print(200)
            elif utterance_id == 300:
                print(300)
            elif utterance_id == 400:
                print(400)
            elif utterance_id == 500:
                print(500)
            elif utterance_id == 600:
                print(600)
            elif utterance_id == 700:
                print(700)
            elif utterance_id == 800:
                print(800)
            elif utterance_id == 900:
                print(900)
            utterance_id += 1

# function to label a test set using the Naive Bayes algorithm and Sentiment and to save results in a new file for the other datesets
def do_test_set_naive_bayes_sent_pos_hs_ld(utterances, utterances_unprocessed, filename, lex, file, column, sentimentfile_train, sentimentfile_test, mode):
    # annotation using naive_bayes will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Hate Speech"]) # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities_other_datasets(sentimentfile_train, file, column, mode)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            class_hs = do_naive_bayes_sent_pos_hs_ld(utterance, utterance_unprocessed, lex, list_of_sentiments[utterance_id], sentimentlist)  # determine class of the utterance using do_sentiment_naive_bayes_hs()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_hs])

            if utterance_id == 100:
                print(100)
            elif utterance_id == 200:
                print(200)
            elif utterance_id == 300:
                print(300)
            elif utterance_id == 400:
                print(400)
            elif utterance_id == 500:
                print(500)
            elif utterance_id == 600:
                print(600)
            elif utterance_id == 700:
                print(700)
            elif utterance_id == 800:
                print(800)
            elif utterance_id == 900:
                print(900)
            elif utterance_id == 1000:
                print(1000)
            elif utterance_id == 1100:
                print(1100)
            elif utterance_id == 1200:
                print(1200)
            elif utterance_id == 1300:
                print(1300)
            elif utterance_id == 1400:
                print(1400)
            elif utterance_id == 1500:
                print(1500)
            elif utterance_id == 1600:
                print(1600)
            elif utterance_id == 1700:
                print(1700)
            elif utterance_id == 1800:
                print(1800)
            elif utterance_id == 1900:
                print(1900)
            elif utterance_id == 2000:
                print(2000)
            elif utterance_id == 2100:
                print(2100)
            elif utterance_id == 2200:
                print(2200)

            utterance_id += 1

# function to label a test set using the Naive Bayes algorithm and Sentiment and to save results in a new file for the other datesets
def do_test_set_naive_bayes_sent_pos_hs_ths(utterances, utterances_unprocessed, filename, lex, file, column, sentimentfile_train, sentimentfile_test, mode):
    # annotation using naive_bayes will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Hate Speech"]) # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities_other_datasets(sentimentfile_train, file, column, mode)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            class_hs = do_naive_bayes_sent_pos_hs_ths(utterance, utterance_unprocessed, lex, list_of_sentiments[utterance_id], sentimentlist)  # determine class of the utterance using do_sentiment_naive_bayes_hs()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_hs])

            if utterance_id == 100:
                print(100)
            elif utterance_id == 200:
                print(200)
            elif utterance_id == 300:
                print(300)
            elif utterance_id == 400:
                print(400)
            elif utterance_id == 500:
                print(500)
            elif utterance_id == 600:
                print(600)
            elif utterance_id == 700:
                print(700)
            elif utterance_id == 800:
                print(800)
            elif utterance_id == 900:
                print(900)

            utterance_id += 1

# labeled data
estimate_class_frequency_other_datasets("labeled_data_train.csv", 2)
estimate_hate_speech_frequency_other_datasets("labeled_data_train.csv", 2)
test_list_ld = machine_learning_processing.process_data("labeled_data_test.csv", 6)
test_list_ld_unprocessed = machine_learning_processing.process_data("labeled_data_test.csv", 6)
do_test_set_naive_bayes_sent_pos_ld(test_list_ld, test_list_ld_unprocessed, "labeled_data_naive_bayes_final.csv", "lexicon_with_occurences_ld.txt", "labeled_data_train.csv", 5, "labeled_data_train_with_sentiment.csv", "labeled_data_test_with_sentiment.csv", 2)
do_test_set_naive_bayes_sent_pos_hs_ld(test_list_ld, test_list_ld_unprocessed, "labeled_data_naive_bayes_final_hs.csv", "lexicon_with_occurences_hs_ld.txt", "labeled_data_train.csv", 5, "labeled_data_train_with_sentiment.csv", "labeled_data_test_with_sentiment.csv", 2)
estimation.test_results("labeled_data_test.csv", 5, "labeled_data_naive_bayes_final.csv", 1)
estimation.test_results("labeled_data_test.csv", 5, "labeled_data_naive_bayes.csv", 1)

estimation.test_results("labeled_data_test.csv", 5, "labeled_data_naive_bayes_final_hs.csv", 1)
estimation.test_results("labeled_data_test.csv", 5, "labeled_data_naive_bayes_hs.csv", 1)

# twitter hate speech
estimate_class_frequency_other_datasets("twitter_hate_speech_train.csv", 3)
estimate_hate_speech_frequency_other_datasets("twitter_hate_speech_train.csv", 3)
test_list_ths = machine_learning_processing.process_data("twitter_hate_speech_test.csv", 1)
test_list_ths_unprocessed = machine_learning_processing.process_data("twitter_hate_speech_test.csv", 1)
do_test_set_naive_bayes_sent_pos_ths(test_list_ths, test_list_ths_unprocessed, "twitter_hate_speech_naive_bayes_final.csv", "lexicon_with_occurences_ths.txt", "twitter_hate_speech_train.csv", 2, "twitter_hate_speech_train_with_sentiment.csv", "twitter_hate_speech_test_with_sentiment.csv", 3)
do_test_set_naive_bayes_sent_pos_hs_ths(test_list_ths, test_list_ths_unprocessed, "twitter_hate_speech_naive_bayes_final_hs.csv", "lexicon_with_occurences_hs_ths.txt", "twitter_hate_speech_train.csv", 2, "twitter_hate_speech_train_with_sentiment.csv", "twitter_hate_speech_test_with_sentiment.csv", 3)
estimation.test_results("twitter_hate_speech_test.csv", 2, "twitter_hate_speech_naive_bayes_final.csv", 1)
estimation.test_results("twitter_hate_speech_test.csv", 2, "twitter_hate_speech_naive_bayes_final_hs.csv", 1)

estimation.test_results("twitter_hate_speech_test.csv", 2, "twitter_hate_speech_naive_bayes.csv", 1)
estimation.test_results("twitter_hate_speech_test.csv", 2, "twitter_hate_speech_naive_bayes_hs.csv", 1)