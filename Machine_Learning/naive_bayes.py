import csv
import machine_learning_processing
import estimation
import senti_strength

# global variables
freq_cb = 0
freq_no_cb = 0
freq_hs = 0
freq_no_hs = 0
freq_s1 = 0
freq_s2 = 0
freq_s3 = 0
freq_s4 = 0
freq_s5 = 0

# function to estimate the frequencies of each cyberbullying class in the training dataset
def estimate_class_frequency(file):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                  # skip header

        cyberbullying = 0
        no_cyberbullying = 0
        utterances = 0

        # count utterances that are labeled as cyberbuylling / no_cyberbullying
        for row in reader:
            if row[7] == 1 or row[7] == "1":
                cyberbullying += 1
            else:
                no_cyberbullying += 1
            utterances += 1

        global freq_cb
        freq_cb = cyberbullying / utterances                # frequency of utterances that are labeled as cyberbullying
        global freq_no_cb
        freq_no_cb = no_cyberbullying / utterances          # frequency of utterances that are labeled as no_cyberbullying

#estimate_class_frequency("train_set.csv")

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
def estimate_hate_speech_frequency(file):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                  # skip header

        hate_speech = 0
        no_hatespeech = 0
        utterances = 0

        # count utterances that are labeled as hate speech / no hate speech
        for row in reader:
            if row[9] == 1 or row[9] == "1":
                hate_speech += 1
            else:
                no_hatespeech += 1
            utterances += 1

        global freq_hs
        freq_hs = hate_speech / utterances                # frequency of utterances that are labeled as cyberbullying
        global freq_no_hs
        freq_no_hs = no_hatespeech / utterances          # frequency of utterances that are labeled as no_cyberbullying

#estimate_hate_speech_frequency("train_set.csv")

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

# function to estimate the frequencies of each cyberbullying strength class in the training dataset
def estimate_cb_strength_frequency(file):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                  # skip header

        s1 = 0
        s2 = 0
        s3 = 0
        s4 = 0
        s5 = 0
        utterances = 0

        # count utterances that are labeled as s1 / s2 / s3 / s4 / s5
        for row in reader:
            if row[8] == 1 or row[8] == "1":
                s1 += 1
            elif row[8] == 2 or row[8] == "2":
                s2 += 1
            elif row[8] == 3 or row[8] == "3":
                s3 += 1
            elif row[8] == 4 or row[8] == "4":
                s4 += 1
            else:
                s5 += 1
            utterances += 1

        global freq_s1
        freq_s1 = s1 / utterances                   # frequency of utterances that are labeled as cyberbullying strength 1
        global freq_s2
        freq_s2 = s2 / utterances                   # frequency of utterances that are labeled as no_cyberbullying strength 2
        global freq_s3
        freq_s3 = s3 / utterances                   # frequency of utterances that are labeled as no_cyberbullying strength 3
        global freq_s4
        freq_s4 = s4 / utterances                   # frequency of utterances that are labeled as no_cyberbullying strength 4
        global freq_s5
        freq_s5 = s5 / utterances                   # frequency of utterances that are labeled as no_cyberbullying strength 5

estimate_cb_strength_frequency("train_cb_set.csv")

#function to use the naive bayes algorithm on an utterance of the test_set
# returns the cyberbullying class for the utterances assigned by the algorithm
def do_naive_bayes(utterance, lex):
    """
    We use the Naive Bayes algorithm to determine the class (cyberbullying, no cyberbullying) of each tweet.
    We work with our data_list containing all stemmed and processed tweets and our lexicon.

    For Naive Bayes we need to:
        - estimate P(class|tweet) for every class (cyberbullying, no_cyberbullying) and every tweet
        - compare the probabilites to find the greatest probability and therefore the most suitable class
        - save the tweet with the respective class in a csv-file (to later compare it with the manually assigned classes)

    P(tweet|class) = P(w1|class) * P(w2|class) * ... * P(wn|class)

    Then we have to estimate P(class|tweet) by multiplying P(tweet|class) with P(class), which is
    determined by the number of cyberbuylling-tweets and no_cyberbullying-tweets in our data.
    """

    # base value must be 1, so we won't multiply with 0
    p_utterance_class_1 = 1                                             # p(tweet|class)
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

                # without laplace smoothing --> barely a change in results
                #if line_split[1] != "0.0":
                #    p_utterance_class_1 *= float(line_split[1])
                #else:
                #    p_utterance_class_1 *= 0.025                        # multiply by a low weight to get best result with unseen word-class-occurences
                #if line_split[2] != "0.0":
                #    p_utterance_class_0 *= float(line_split[2])
                #else:
                #    p_utterance_class_0 *= 0.025

    # multiply p(tweet|class) with p(class) (freq_cb / freq_no_cb)
    p_class_utterance_1 = p_utterance_class_1 * freq_cb                 # p(class|tweet)
    p_class_utterance_0 = p_utterance_class_0 * freq_no_cb

    # class with the higher probability will be assigned to the utterance
    values = [p_class_utterance_1, p_class_utterance_0]
    if max(values) == values[0]:                                        # determine class (max p(class|tweet))
        class_cb = 1
    elif contains_curses == True:                                       # utterances that contain curses will automatically be labeled as cyberbullying
        class_cb = 1
    else:
        class_cb = 0
    #print(class_cb)

    return class_cb

#function to use the naive bayes algorithm with sentiment on an utterance of the test_set
# returns the cyberbullying class for the utterances assigned by the algorithm
def do_sentiment_naive_bayes(utterance, lex, sentiment, sentimentlist):
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

                # without laplace smoothing --> barely a change in results
                # if line_split[1] != "0.0":
                #    p_utterance_class_1 *= float(line_split[1])
                # else:
                #    p_utterance_class_1 *= 0.025                        # multiply by a low weight to get best result with unseen word-class-occurences
                # if line_split[2] != "0.0":
                #    p_utterance_class_0 *= float(line_split[2])
                # else:
                #    p_utterance_class_0 *= 0.025

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
    #print(p_class_utterance_0, p_class_utterance_1)

    # class with the higher probability will be assigned to the utterance
    values = [p_class_utterance_1, p_class_utterance_0]
    if max(values) == values[0]:  # determine class (max p(class|tweet))
        class_cb = 1
    elif contains_curses == True:                                                               # utterances that contain curses will automatically be labeled as cyberbullying
        class_cb = 1
    else:
        class_cb = 0
    # print(class_cb)

    return class_cb

#function to use the naive bayes algorithm on an utterance of the test_set
# returns the hate speech class for the utterances assigned by the algorithm
def do_naive_bayes_hate_speech(utterance, lex):
    """
    We use the Naive Bayes algorithm to determine the class (hate speech, no hate speech) of each tweet.
    We work with our data_list containing all stemmed and processed tweets and our lexicon.

    For Naive Bayes we need to:
        - estimate P(class|tweet) for every class (hate speech, no hate speech) and every tweet
        - compare the probabilites to find the greatest probability and therefore the most suitable class
        - save the tweet with the respective class in a csv-file (to later compare it with the manually assigned classes)

    P(tweet|class) = P(w1|class) * P(w2|class) * ... * P(wn|class)

    Then we have to estimate P(class|tweet) by multiplying P(tweet|class) with P(class), which is
    determined by the number of hate-speech-tweets and no_hate_speech-tweets in our data.
    """

    # base value must be 1, so we won't multiply with 0
    p_utterance_class_1 = 1                                             # p(tweet|class)
    p_utterance_class_0 = 1

    for word in utterance:
        for line in open(lex):
            if word in line:
                line_split = line.split()

                # multiply each word frequency in the respective class
                # with laplace smoothing
                p_utterance_class_1 *= float(line_split[1])
                p_utterance_class_0 *= float(line_split[2])

                # without laplace smoothing --> barely a change in results
                #if line_split[1] != "0.0":
                #    p_utterance_class_1 *= float(line_split[1])
                #else:
                #    p_utterance_class_1 *= 0.025                        # multiply by a low weight to get best result with unseen word-class-occurences
                #if line_split[2] != "0.0":
                #    p_utterance_class_0 *= float(line_split[2])
                #else:
                #    p_utterance_class_0 *= 0.025

    # multiply p(tweet|class) with p(class) (freq_cb / freq_no_cb)
    p_class_utterance_1 = p_utterance_class_1 * freq_hs                 # p(class|tweet)
    p_class_utterance_0 = p_utterance_class_0 * freq_no_hs

    # class with the higher probability will be assigned to the utterance
    values = [p_class_utterance_1, p_class_utterance_0]
    if max(values) == values[0]:                                        # determine class (max p(class|tweet))
        class_hs = 1
    else:
        class_hs = 0
    #print(class_cb)

    return class_hs

#function to use the naive bayes algorithm on an utterance of the test_set
# returns the strength class for the utterances assigned by the algorithm
def do_naive_bayes_strength(utterance, lex):
    """
    We use the Naive Bayes algorithm to determine the cyberbullying strength of each tweet.
    We work with our data_list containing all stemmed and processed tweets and our lexicon.

    For Naive Bayes we need to:
        - estimate P(class|tweet) for every class (s1-s5) and every tweet
        - compare the probabilites to find the greatest probability and therefore the most suitable class
        - save the tweet with the respective class in a csv-file (to later compare it with the manually assigned classes)

    P(tweet|class) = P(w1|class) * P(w2|class) * ... * P(wn|class)

    Then we have to estimate P(class|tweet) by multiplying P(tweet|class) with P(class), which is
    determined by the number of s1- to s5-tweets in our data.
    """

    # base value must be 1, so we won't multiply with 0
    p_utterance_class_1 = 1                                             # p(tweet|class)
    p_utterance_class_2 = 1
    p_utterance_class_3 = 1
    p_utterance_class_4 = 1
    p_utterance_class_5 = 1

    for word in utterance:
        for line in open(lex):
            if word in line:
                line_split = line.split()

                # multiply each word frequency in the respective class
                # with laplace smoothing
                p_utterance_class_1 *= float(line_split[1])
                p_utterance_class_2 *= float(line_split[2])
                p_utterance_class_3 *= float(line_split[3])
                p_utterance_class_4 *= float(line_split[4])
                p_utterance_class_5 *= float(line_split[5])

    # multiply p(tweet|class) with p(class) (freq_cb / freq_no_cb)
    p_class_utterance_1 = p_utterance_class_1 * freq_s1                 # p(class|tweet)
    p_class_utterance_2 = p_utterance_class_2 * freq_s2
    p_class_utterance_3 = p_utterance_class_3 * freq_s3
    p_class_utterance_4 = p_utterance_class_4 * freq_s4
    p_class_utterance_5 = p_utterance_class_5 * freq_s5

    # class with the higher probability will be assigned to the utterance
    values = [p_class_utterance_1, p_class_utterance_2, p_class_utterance_3, p_class_utterance_4, p_class_utterance_5]
    if max(values) == values[0]:                                        # determine class (max p(class|tweet))
        class_strength = 1
    elif max(values) == values[1]:
        class_strength = 2
    elif max(values) == values[2]:
        class_strength = 3
    elif max(values) == values[3]:
        class_strength = 4
    else:
        class_strength = 5

    return class_strength

#function to use the naive bayes algorithm with sentiment on an utterance of the test_set
# returns the hate speech class for the utterances assigned by the algorithm
def do_sentiment_naive_bayes_hs(utterance, lex, sentiment, sentimentlist):
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
    #print(p_class_utterance_0, p_class_utterance_1)

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
def do_sentiment_naive_bayes_strength(utterance, lex, sentiment, sentimentlist):
    p_utterance_class_1 = 1  # p(tweet|class)
    p_utterance_class_2 = 1
    p_utterance_class_3 = 1
    p_utterance_class_4 = 1
    p_utterance_class_5 = 1

    for word in utterance:
        for line in open(lex):
            if word in line:
                line_split = line.split()

                # multiply each word frequency in the respective class
                # with laplace smoothing
                p_utterance_class_1 *= float(line_split[1])
                p_utterance_class_2 *= float(line_split[2])
                p_utterance_class_3 *= float(line_split[3])
                p_utterance_class_4 *= float(line_split[4])
                p_utterance_class_5 *= float(line_split[5])

    p_pos_s1 = sentimentlist[0]
    p_pos_s2 = sentimentlist[1]
    p_pos_s3 = sentimentlist[2]
    p_pos_s4 = sentimentlist[3]
    p_pos_s5 = sentimentlist[4]
    p_neut_s1 = sentimentlist[5]
    p_neut_s2 = sentimentlist[6]
    p_neut_s3 = sentimentlist[7]
    p_neut_s4 = sentimentlist[8]
    p_neut_s5 = sentimentlist[9]
    p_neg_s1 = sentimentlist[10]
    p_neg_s2 = sentimentlist[11]
    p_neg_s3 = sentimentlist[12]
    p_neg_s4 = sentimentlist[13]
    p_neg_s5 = sentimentlist[14]

    if sentiment == 1 or sentiment == "1":
        p_class_utterance_1 = p_utterance_class_1 * freq_s1 * p_pos_s1
        p_class_utterance_2 = p_utterance_class_2 * freq_s2 * p_pos_s2
        p_class_utterance_3 = p_utterance_class_3 * freq_s3 * p_pos_s3
        p_class_utterance_4 = p_utterance_class_4 * freq_s4 * p_pos_s4
        p_class_utterance_5 = p_utterance_class_5 * freq_s5 * p_pos_s5
    elif sentiment == 0 or sentiment == "0":
        p_class_utterance_1 = p_utterance_class_1 * freq_s1 * p_neut_s1
        p_class_utterance_2 = p_utterance_class_2 * freq_s2 * p_neut_s2
        p_class_utterance_3 = p_utterance_class_3 * freq_s3 * p_neut_s3
        p_class_utterance_4 = p_utterance_class_4 * freq_s4 * p_neut_s4
        p_class_utterance_5 = p_utterance_class_5 * freq_s5 * p_neut_s5
    else:
        p_class_utterance_1 = p_utterance_class_1 * freq_s1 * p_neg_s1
        p_class_utterance_2 = p_utterance_class_2 * freq_s2 * p_neg_s2
        p_class_utterance_3 = p_utterance_class_3 * freq_s3 * p_neg_s3
        p_class_utterance_4 = p_utterance_class_4 * freq_s4 * p_neg_s4
        p_class_utterance_5 = p_utterance_class_5 * freq_s5 * p_neg_s5

    # class with the higher probability will be assigned to the utterance
    values = [p_class_utterance_1, p_class_utterance_2, p_class_utterance_3, p_class_utterance_4, p_class_utterance_5]
    if max(values) == values[0]:  # determine class (max p(class|tweet))
        class_strength = 1
    elif max(values) == values[1]:
        class_strength = 2
    elif max(values) == values[2]:
        class_strength = 3
    elif max(values) == values[3]:
        class_strength = 4
    else:
        class_strength = 5
    # print(class_strength)

    return class_strength

# function to label a test set using the Naive Bayes algorithm and to save results in a new file
def do_test_set_naive_bayes(utterances, filename, lex):
    # annotation using naive_bayes will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying"]) # header

        for utterance in utterances:
            class_cb = do_naive_bayes(utterance, lex)               # determine class of the utterance using do_naive_bayes()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_cb])

# function to label a test set using the Naive Bayes algorithm and Sentiment and to save results in a new file
def do_test_set_naive_bayes_sent(utterances, filename, lex, file, column, sentimentfile_train, sentimentfile_test):
    # annotation using naive_bayes will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying"]) # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities(sentimentfile_train, file, column)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances:
            class_cb = do_sentiment_naive_bayes(utterance, lex, list_of_sentiments[utterance_id], sentimentlist)  # determine class of the utterance using do_naive_bayes()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_cb])
            utterance_id += 1

# function to label a test set using the Naive Bayes algorithm and to save results in a new file
def do_test_set_naive_bayes_hate_speech(utterances, filename, lex):
    # annotation using naive_bayes will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Hate Speech"]) # header

        for utterance in utterances:
            class_hs = do_naive_bayes_hate_speech(utterance, lex)               # determine class of the utterance using do_naive_bayes()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_hs])

# function to label a test set using the Naive Bayes algorithm and to save results in a new file
def do_test_set_naive_bayes_strength(utterances, filename, lex):
    # annotation using naive_bayes will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying Strength"]) # header

        for utterance in utterances:
            class_strength = do_naive_bayes_strength(utterance, lex)            # determine class of the utterance using do_naive_bayes()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_strength])

# function to label a test set using the Naive Bayes algorithm and Sentiment and to save results in a new file
def do_test_set_naive_bayes_sent_hs(utterances, filename, lex, file, column, sentimentfile_train, sentimentfile_test):
    # annotation using naive_bayes will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Hate Speech"]) # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities(sentimentfile_train, file, column)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances:
            class_hs = do_sentiment_naive_bayes_hs(utterance, lex, list_of_sentiments[utterance_id], sentimentlist)  # determine class of the utterance using do_sentiment_naive_bayes_hs()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_hs])
            utterance_id += 1

# function to label a test set using the Naive Bayes algorithm and Sentiment and to save results in a new file
def do_test_set_naive_bayes_sent_strength(utterances, filename, lex, file, column, sentimentfile_train, sentimentfile_test):
    # annotation using naive_bayes will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying Strength"]) # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities_strengths(sentimentfile_train, file, column)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances:
            class_strength = do_sentiment_naive_bayes_strength(utterance, lex, list_of_sentiments[utterance_id], sentimentlist)  # determine class of the utterance using do_naive_bayes()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_strength])
            utterance_id += 1

# function to label a test set using the Naive Bayes algorithm and Sentiment and to save results in a new file for the other datasets
def do_test_set_naive_bayes_sent_other(utterances, filename, lex, file, column, sentimentfile_train, sentimentfile_test, mode):
    # annotation using naive_bayes will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying"]) # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities_other_datasets(sentimentfile_train, file, column, mode)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances:
            class_cb = do_sentiment_naive_bayes(utterance, lex, list_of_sentiments[utterance_id], sentimentlist)  # determine class of the utterance using do_naive_bayes()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_cb])
            utterance_id += 1

# function to label a test set using the Naive Bayes algorithm and Sentiment and to save results in a new file for the other datesets
def do_test_set_naive_bayes_sent_hs_other(utterances, filename, lex, file, column, sentimentfile_train, sentimentfile_test, mode):
    # annotation using naive_bayes will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Hate Speech"]) # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities_other_datasets(sentimentfile_train, file, column, mode)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances:
            class_hs = do_sentiment_naive_bayes_hs(utterance, lex, list_of_sentiments[utterance_id], sentimentlist)  # determine class of the utterance using do_sentiment_naive_bayes_hs()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_hs])
            utterance_id += 1

utterance = machine_learning_processing.process_utterance("Yup. I can't stand this shit. The left screams and yells Black Lives Matter and the minute a black man or woman disappear")
utterance2 = machine_learning_processing.process_utterance("ban islam")
utterance3 = machine_learning_processing.process_utterance("This is our president. WHO talks like that?!? Our leader does. I cant. How embarrassing. A disgrace to the office.")

test_list = machine_learning_processing.process_data("test_set.csv", 5)

#do_naive_bayes(utterance, "lexicon_with_occurences.txt")
#do_naive_bayes(utterance2, "lexicon_with_occurences.txt")
#do_naive_bayes(utterance3, "lexicon_with_occurences.txt")

#do_test_set_naive_bayes(test_list, "twitter_bullying_naive_bayes.csv", "lexicon_with_occurences.txt")
#do_test_set_naive_bayes(training_list, "twitter_bullying_naive_bayes_test_no_laplace.csv", "lexicon_with_occurences_without_laplace.txt")

#do_test_set_naive_bayes_sent(test_list, "twitter_bullying_naive_bayes_sent.csv", "lexicon_with_occurences.txt", "train_set.csv", 7, "train_set_with_sentiment.csv", "test_set_with_sentiment.csv")

#do_test_set_naive_bayes(test_list, "twitter_bullying_naive_bayes2.csv", "lexicon_with_occurences2.txt")

#do_test_set_naive_bayes(test_list, "twitter_bullying_naive_bayes_c.csv", "lexicon_with_occurences.txt")

#do_test_set_naive_bayes_sent(test_list, "twitter_bullying_naive_bayes_sent_c.csv", "lexicon_with_occurences.txt", "train_set.csv", 7, "train_set_with_sentiment.csv", "test_set_with_sentiment.csv")

#estimation.test_results("test_set.csv", 7, "twitter_bullying_naive_bayes.csv", 1)
#estimation.test_results("test_set.csv", 7, "twitter_bullying_naive_bayes_sent.csv", 1)
#estimation.test_results("test_set.csv", 7, "twitter_bullying_naive_bayes2.csv", 1)
#estimation.test_results("test_set.csv", 7, "twitter_bullying_naive_bayes_c.csv", 1)
#estimation.test_results("test_set.csv", 7, "twitter_bullying_naive_bayes_sent_c.csv", 1)

# hate speech
#do_test_set_naive_bayes_hate_speech(test_list, "twitter_bullying_naive_bayes_hs.csv", "lexicon_with_occurences_hs.txt")
#estimation.test_results("test_set.csv", 9, "twitter_bullying_naive_bayes_hs.csv", 1)

# hate speech with sentiment
#do_test_set_naive_bayes_sent_hs(test_list, "twitter_bullying_naive_bayes_sent_hs.csv", "lexicon_with_occurences_hs.txt", "train_set.csv", 9, "train_set_with_sentiment.csv", "test_set_with_sentiment.csv")
#estimation.test_results("test_set.csv", 9, "twitter_bullying_naive_bayes_sent_hs.csv", 1)

# strength
test_s_list = machine_learning_processing.process_data("test_cb_set.csv", 5)
#do_test_set_naive_bayes_strength(test_s_list, "twitter_bullying_naive_bayes_strength.csv", "lexicon_with_occurences_cb.txt")
#estimation.test_results_strengths("test_cb_set.csv", 8, "twitter_bullying_naive_bayes_strength.csv", 1)

# strength with sentiment
#do_test_set_naive_bayes_sent_strength(test_s_list, "twitter_bullying_naive_bayes_sent_strength.csv", "lexicon_with_occurences_cb.txt", "train_cb_set.csv", 8, "train_cb_set_with_sentiment.csv", "test_cb_set_with_sentiment.csv")
#estimation.test_results_strengths("test_cb_set.csv", 8, "twitter_bullying_naive_bayes_sent_strength.csv", 1)

# bullying traces
estimate_class_frequency_other_datasets("bullying_traces_train.csv", 1)
test_list_bt = machine_learning_processing.process_data("bullying_traces_test.csv", 2)
do_test_set_naive_bayes_sent(test_list_bt, "bullying_traces_naive_bayes.csv", "lexicon_with_occurences_bt.txt", "bullying_traces_train.csv", 3, "train_set_bt_with_sentiment.csv", "test_set_bt_with_sentiment.csv")
estimation.test_results("test_set.csv", 7, "bullying_traces_naive_bayes.csv", 1)

# labeled data
estimate_class_frequency_other_datasets("labeled_data_train.csv", 2)
estimate_hate_speech_frequency_other_datasets("labeled_data_train.csv", 2)
test_list_ld = machine_learning_processing.process_data("labeled_data_test.csv", 6)
do_test_set_naive_bayes_sent_other(test_list_ld, "labeled_data_naive_bayes.csv", "lexicon_with_occurences_ld.txt", "labeled_data_train.csv", 5, "train_set_ld_with_sentiment.csv", "test_set_ld_with_sentiment.csv", 2)
do_test_set_naive_bayes_sent_hs_other(test_list_ld, "labeled_data_naive_bayes_hs.csv", "lexicon_with_occurences_hs_ld.txt", "labeled_data_train.csv", 5, "train_set_ld_with_sentiment.csv", "test_set_ld_with_sentiment.csv", 2)
estimation.test_results("test_set.csv", 7, "labeled_data_naive_bayes.csv", 1)
estimation.test_results("test_set.csv", 9, "labeled_data_naive_bayes_hs.csv", 1)

# twitter hate speech
estimate_class_frequency_other_datasets("twitter_hate_speech_train.csv", 3)
estimate_hate_speech_frequency_other_datasets("twitter_hate_speech_train.csv", 3)
test_list_ths = machine_learning_processing.process_data("twitter_hater_speech_test.csv", 1)
do_test_set_naive_bayes_sent_other(test_list_ths, "twitter_hate_speech_naive_bayes.csv", "lexicon_with_occurences_ths.txt", "twitter_hate_speech_train.csv", 2, "train_set_ths_with_sentiment.csv", "test_set_ths_with_sentiment.csv", 3)
do_test_set_naive_bayes_sent_hs_other(test_list_ths, "twitter_hate_speech_naive_bayes_hs.csv", "lexicon_with_occurences_hs_ths.txt", "twitter_hate_speech_train.csv", 2, "train_set_ths_with_sentiment.csv", "test_set_ths_with_sentiment.csv", 3)
estimation.test_results("test_set.csv", 7, "twitter_hate_speech_naive_bayes.csv", 1)
estimation.test_results("test_set.csv", 9, "twitter_hate_speech_naive_bayes_hs.csv", 1)


