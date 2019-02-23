import csv
import machine_learning_processing
import estimation
import senti_strength
import math

# function to use the Maximum Entropy Model algorithm on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_mem(utterance, lex):
    """
    We use the Maximum Entropy Model algorithm to determine the class of each utterance.
    We work with our data_list containing all stemmed and processed utterances and our lexicon with occurence probabilities.

    For MEM we need to estimate the weighted feature sum for each class (cyberbullying, no_cyberbullying) and every tweet.
    For this we need to add up the probabilities from our lexicon.

    The weighted feature sums will be used in the MEM-algorithms. For example, for the cyberbullying class it's estimated like this:
        P(class|tweet) = e(cyberbullying_feature_sum) divided by (e(cyberbullying_feature_sum) + e(no_cyberbullying_feature_sum)
    """

    cyberbullying_feature_sum = 0                                   # weighted feature sums
    no_cyberbullying_feature_sum = 0
    cb_class = ""

    contains_curses = False
    curses = machine_learning_processing.make_list_of_curse_words("curses.txt")

    for word in utterance:
        if word in curses:
            contains_curses = True                                          # utterances that contain curses will automatically be labeled as cyberbullying later

        for line in open(lex):
            if word in line:
                line_split = line.split()
                cyberbullying_feature_sum += float(line_split[1])
                no_cyberbullying_feature_sum += float(line_split[2])

    cyberbullying_feature_sum = cyberbullying_feature_sum / 10              # values are too big, divide by 10 to make it practical
    no_cyberbullying_feature_sum = no_cyberbullying_feature_sum / 10

    # estimating P(class|tweet)
    e = math.e
    e_cyberbullying_feature_sum = e ** cyberbullying_feature_sum
    e_no_cyberbullying_feature_sum = e ** no_cyberbullying_feature_sum

    p_cyberbullying_utterance = e_cyberbullying_feature_sum * 1.2 / (e_cyberbullying_feature_sum + e_no_cyberbullying_feature_sum)
    p_no_cyberbullying_utterance = e_no_cyberbullying_feature_sum / (e_no_cyberbullying_feature_sum + e_no_cyberbullying_feature_sum)
    values = [p_cyberbullying_utterance, p_no_cyberbullying_utterance]

    if max(values) == values[0]:                                    # determine class (max P(class|tweet))
        cb_class = 1
    elif contains_curses == True:                                                               # utterances that contain curses will automatically be labeled as cyberbullying
        cb_class = 1
    else:
        cb_class = 0
    #print(cb_class)

    return cb_class

# function to use the Maximum Entropy Model algorithm and Sentiment on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_sentiment_mem(utterance, lex, sentiment, sentimentlist):
    cyberbullying_feature_sum = 0                                   # weighted feature sums
    no_cyberbullying_feature_sum = 0
    cb_class = ""

    contains_curses = False
    curses = machine_learning_processing.make_list_of_curse_words("curses.txt")

    for word in utterance:
        if word in curses:
            contains_curses = True                                          # utterances that contain curses will automatically be labeled as cyberbullying later

        for line in open(lex):
            if word in line:
                line_split = line.split()
                cyberbullying_feature_sum += float(line_split[1])
                no_cyberbullying_feature_sum += float(line_split[2])

    cyberbullying_feature_sum = cyberbullying_feature_sum / 10              # values are too big, divide by 10 to make it practical
    no_cyberbullying_feature_sum = no_cyberbullying_feature_sum / 10

    # estimating P(class|tweet)
    e = math.e
    e_cyberbullying_feature_sum = e ** cyberbullying_feature_sum
    e_no_cyberbullying_feature_sum = e ** no_cyberbullying_feature_sum

    p_cyberbullying_utterance = e_cyberbullying_feature_sum * 1.2 / (e_cyberbullying_feature_sum + e_no_cyberbullying_feature_sum)
    p_no_cyberbullying_utterance = e_no_cyberbullying_feature_sum / (e_no_cyberbullying_feature_sum + e_no_cyberbullying_feature_sum)

    p_pos_cb = sentimentlist[0]
    p_pos_no_cb = sentimentlist[1]
    p_neut_cb = sentimentlist[2]
    p_neut_no_cb = sentimentlist[3]
    p_neg_cb = sentimentlist[4]
    p_neg_no_cb = sentimentlist[5]

    # multiply by sentiment probability in regard to utterance's sentiment
    if sentiment == 1 or sentiment == "1":
        p_cyberbullying_utterance = p_cyberbullying_utterance * p_pos_cb
        p_no_cyberbullying_utterance = p_no_cyberbullying_utterance * p_pos_no_cb
    elif sentiment == 0 or sentiment == "0":
        p_cyberbullying_utterance = p_cyberbullying_utterance * p_neut_cb
        p_no_cyberbullying_utterance = p_no_cyberbullying_utterance * p_neut_no_cb
    else:
        p_cyberbullying_utterance = p_cyberbullying_utterance * p_neg_cb * 500
        p_no_cyberbullying_utterance = p_no_cyberbullying_utterance * p_neg_no_cb

    values = [p_cyberbullying_utterance, p_no_cyberbullying_utterance]
    #print(values)

    if max(values) == values[0]:                                    # determine class (max P(class|tweet))
        cb_class = 1
    elif contains_curses == True:                                                               # utterances that contain curses will automatically be labeled as cyberbullying
        cb_class = 1
    else:
        cb_class = 0
    #print(cb_class)

    return cb_class

# function to use the Maximum Entropy Model algorithm on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_mem_hs(utterance, lex):
    """
    We use the Maximum Entropy Model algorithm to determine the class of each utterance.
    We work with our data_list containing all stemmed and processed utterances and our lexicon with occurence probabilities.

    For MEM we need to estimate the weighted feature sum for each class (hate speech, no_hate_speech) and every tweet.
    For this we need to add up the probabilities from our lexicon.

    The weighted feature sums will be used in the MEM-algorithms. For example, for the cyberbullying class it's estimated like this:
        P(class|tweet) = e(hate_speech_feature_sum) divided by (e(hate_speech_feature_sum) + e(no_hate_speech_feature_sum)
    """

    hs_feature_sum = 0                                   # weighted feature sums
    no_hs_feature_sum = 0
    hs_class = ""

    for word in utterance:
        for line in open(lex):
            if word in line:
                line_split = line.split()
                hs_feature_sum += float(line_split[1])
                no_hs_feature_sum += float(line_split[2])

    hs_feature_sum = hs_feature_sum / 10              # values are too big, divide by 10 to make it practical
    no_hs_feature_sum = no_hs_feature_sum / 10

    # estimating P(class|tweet)
    e = math.e
    e_hs_feature_sum = e ** hs_feature_sum
    e_no_hs_feature_sum = e ** no_hs_feature_sum

    p_hs_utterance = e_hs_feature_sum * 1.2 / (e_hs_feature_sum + e_no_hs_feature_sum)
    p_no_hs_utterance = e_no_hs_feature_sum / (e_no_hs_feature_sum + e_no_hs_feature_sum)
    values = [p_hs_utterance, p_no_hs_utterance]

    if max(values) == values[0]:                                    # determine class (max P(class|tweet))
        hs_class = 1
    else:
        hs_class = 0
    #print(hs_class)

    return hs_class

# function to use the Maximum Entropy Model algorithm on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_mem_strength(utterance, lex):
    """
    We use the Maximum Entropy Model algorithm to determine the class of each utterance.
    We work with our data_list containing all stemmed and processed utterances and our lexicon with occurence probabilities.

    For MEM we need to estimate the weighted feature sum for each class (s1 - s5) and every tweet.
    For this we need to add up the probabilities from our lexicon.

    The weighted feature sums will be used in the MEM-algorithms. For example, for the cyberbullying class it's estimated like this:
        P(class|tweet) = e(s1_feature_sum) divided by (e(s1_feature_sum) + e(s2_feature_sum) + e(s3_feature_sum) + e(s4_feature_sum) + e(s5_feature_sum))
    """

    s1_feature_sum = 0                                   # weighted feature sums
    s2_feature_sum = 0
    s3_feature_sum = 0
    s4_feature_sum = 0
    s5_feature_sum = 0

    strength_class = ""

    for word in utterance:
        for line in open(lex):
            if word in line:
                line_split = line.split()
                s1_feature_sum += float(line_split[1])
                s2_feature_sum += float(line_split[2])
                s3_feature_sum += float(line_split[3])
                s4_feature_sum += float(line_split[4])
                s5_feature_sum += float(line_split[5])

    s1_feature_sum = s1_feature_sum / 10              # values are too big, divide by 10 to make it practical
    s2_feature_sum = s2_feature_sum / 10
    s3_feature_sum = s3_feature_sum / 10
    s4_feature_sum = s4_feature_sum / 10
    s5_feature_sum = s5_feature_sum / 10

    # estimating P(class|tweet)
    e = math.e
    e_s1_feature_sum = e ** s1_feature_sum
    e_s2_feature_sum = e ** s2_feature_sum
    e_s3_feature_sum = e ** s3_feature_sum
    e_s4_feature_sum = e ** s4_feature_sum
    e_s5_feature_sum = e ** s5_feature_sum

    p_s1_utterance = e_s1_feature_sum / (e_s1_feature_sum + e_s2_feature_sum + e_s3_feature_sum + e_s4_feature_sum + e_s5_feature_sum)
    p_s2_utterance = e_s2_feature_sum / (e_s1_feature_sum + e_s2_feature_sum + e_s3_feature_sum + e_s4_feature_sum + e_s5_feature_sum)
    p_s3_utterance = e_s3_feature_sum / (e_s1_feature_sum + e_s2_feature_sum + e_s3_feature_sum + e_s4_feature_sum + e_s5_feature_sum)
    p_s4_utterance = e_s4_feature_sum / (e_s1_feature_sum + e_s2_feature_sum + e_s3_feature_sum + e_s4_feature_sum + e_s5_feature_sum)
    p_s5_utterance = e_s5_feature_sum / (e_s1_feature_sum + e_s2_feature_sum + e_s3_feature_sum + e_s4_feature_sum + e_s5_feature_sum)

    values = [p_s1_utterance, p_s2_utterance, p_s3_utterance, p_s4_utterance, p_s5_utterance]

    if max(values) == values[0]:                                    # determine class (max P(class|tweet))
        strength_class = 1
    elif max(values) == values[1]:
        strength_class = 2
    elif max(values) == values[2]:
        strength_class = 3
    elif max(values) == values[3]:
        strength_class = 4
    else:
        strength_class = 5
    #print(strength_class)

    return strength_class

# function to use the Maximum Entropy Model algorithm and Sentiment on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_sentiment_mem_hs(utterance, lex, sentiment, sentimentlist):
    hs_feature_sum = 0                                   # weighted feature sums
    no_hs_feature_sum = 0
    hs_class = ""

    for word in utterance:
        for line in open(lex):
            if word in line:
                line_split = line.split()
                hs_feature_sum += float(line_split[1])
                no_hs_feature_sum += float(line_split[2])

    hs_feature_sum = hs_feature_sum / 10              # values are too big, divide by 10 to make it practical
    no_hs_feature_sum = no_hs_feature_sum / 10

    # estimating P(class|tweet)
    e = math.e
    e_hs_feature_sum = e ** hs_feature_sum
    e_no_hs_feature_sum = e ** no_hs_feature_sum

    p_hs_utterance = e_hs_feature_sum * 1.2 / (e_hs_feature_sum + e_no_hs_feature_sum)
    p_no_hs_utterance = e_no_hs_feature_sum / (e_no_hs_feature_sum + e_no_hs_feature_sum)

    p_pos_hs = sentimentlist[0]
    p_pos_no_hs = sentimentlist[1]
    p_neut_hs = sentimentlist[2]
    p_neut_no_hs = sentimentlist[3]
    p_neg_hs = sentimentlist[4]
    p_neg_no_hs = sentimentlist[5]

    # multiply by sentiment probability in regard to utterance's sentiment
    if sentiment == 1 or sentiment == "1":
        p_hs_utterance = p_hs_utterance * p_pos_hs
        p_no_hs_utterance = p_no_hs_utterance * p_pos_no_hs
    elif sentiment == 0 or sentiment == "0":
        p_hs_utterance = p_hs_utterance * p_neut_hs
        p_no_hs_utterance = p_no_hs_utterance * p_neut_no_hs
    else:
        p_hs_utterance = p_hs_utterance * p_neg_hs * 500
        p_no_hs_utterance = p_no_hs_utterance * p_neg_no_hs

    values = [p_hs_utterance, p_no_hs_utterance]
    #print(values)

    if max(values) == values[0]:                                    # determine class (max P(class|tweet))
        hs_class = 1
    else:
        hs_class = 0
    #print(hs_class)

    return hs_class

# function to use the Maximum Entropy Model algorithm and Sentiment on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_sentiment_mem_strength(utterance, lex, sentiment, sentimentlist):
    s1_feature_sum = 0                                   # weighted feature sums
    s2_feature_sum = 0
    s3_feature_sum = 0
    s4_feature_sum = 0
    s5_feature_sum = 0

    strength_class = ""

    contains_curses = False
    curses = machine_learning_processing.make_list_of_curse_words("curses.txt")

    for word in utterance:
        if word in curses:
            contains_curses = True                                          # utterances that contain curses will automatically be labeled as cyberbullying later

        for line in open(lex):
            if word in line:
                line_split = line.split()
                s1_feature_sum += float(line_split[1])
                s2_feature_sum += float(line_split[2])
                s3_feature_sum += float(line_split[3])
                s4_feature_sum += float(line_split[4])
                s5_feature_sum += float(line_split[5])

    s1_feature_sum = s1_feature_sum / 10              # values are too big, divide by 10 to make it practical
    s2_feature_sum = s2_feature_sum / 10
    s3_feature_sum = s3_feature_sum / 10
    s4_feature_sum = s4_feature_sum / 10
    s5_feature_sum = s5_feature_sum / 10

    # estimating P(class|tweet)
    e = math.e
    e_s1_feature_sum = e ** s1_feature_sum
    e_s2_feature_sum = e ** s2_feature_sum
    e_s3_feature_sum = e ** s3_feature_sum
    e_s4_feature_sum = e ** s4_feature_sum
    e_s5_feature_sum = e ** s5_feature_sum

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

    p_s1_utterance = e_s1_feature_sum / (e_s1_feature_sum + e_s2_feature_sum + e_s3_feature_sum + e_s4_feature_sum + e_s5_feature_sum)
    p_s2_utterance = e_s2_feature_sum / (e_s1_feature_sum + e_s2_feature_sum + e_s3_feature_sum + e_s4_feature_sum + e_s5_feature_sum)
    p_s3_utterance = e_s3_feature_sum / (e_s1_feature_sum + e_s2_feature_sum + e_s3_feature_sum + e_s4_feature_sum + e_s5_feature_sum)
    p_s4_utterance = e_s4_feature_sum / (e_s1_feature_sum + e_s2_feature_sum + e_s3_feature_sum + e_s4_feature_sum + e_s5_feature_sum)
    p_s5_utterance = e_s5_feature_sum / (e_s1_feature_sum + e_s2_feature_sum + e_s3_feature_sum + e_s4_feature_sum + e_s5_feature_sum)

    # multiply by sentiment probability in regard to utterance's sentiment
    if sentiment == 1 or sentiment == "1":
        p_s1_utterance = p_s1_utterance * p_pos_s1
        p_s2_utterance = p_s2_utterance * p_pos_s2
        p_s3_utterance = p_s3_utterance * p_pos_s3
        p_s4_utterance = p_s4_utterance * p_pos_s4
        p_s5_utterance = p_s5_utterance * p_pos_s5
    elif sentiment == 0 or sentiment == "0":
        p_s1_utterance = p_s1_utterance * p_neut_s1
        p_s2_utterance = p_s2_utterance * p_neut_s2
        p_s3_utterance = p_s3_utterance * p_neut_s3
        p_s4_utterance = p_s4_utterance * p_neut_s4
        p_s5_utterance = p_s5_utterance * p_neut_s5
    else:
        p_s1_utterance = p_s1_utterance * p_neg_s1
        p_s2_utterance = p_s2_utterance * p_neg_s2
        p_s3_utterance = p_s3_utterance * p_neg_s3
        p_s4_utterance = p_s4_utterance * p_neg_s4
        p_s5_utterance = p_s5_utterance * p_neg_s5

    values = [p_s1_utterance, p_s2_utterance, p_s3_utterance, p_s4_utterance, p_s5_utterance]
    #print(values)

    if max(values) == values[0]:                                    # determine class (max P(class|tweet))
        strength_class = 1
    elif max(values) == values[1]:
        strength_class = 2
    elif max(values) == values[2]:
        strength_class = 3
    elif max(values) == values[3]:
        strength_class = 4
    else:
        strength_class = 5
    #print(strength_class)

    return strength_class

# function to label a test set using the Maximum Entropy Model algorithm and to save results in a new file
def do_test_set_mem(utterances_test, filename, lex):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying"])             # header

        x = 0
        for utterance in utterances_test:
            class_cb = do_mem(utterance, lex)                       # determine class of the utterance using do_svm()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_cb])
            x += 1

            if x == 500:
                print(x)

# function to label a test set using the Maximum Entropy Model algorithm and Sentiment and to save results in a new file
def do_test_set_mem_sent(utterances_test, filename, lex, file, column, sentimentfile_train, sentimentfile_test):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying"])             # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities(sentimentfile_train, file, column)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances_test:
            class_cb = do_sentiment_mem(utterance, lex, list_of_sentiments[utterance_id], sentimentlist)                       # determine class of the utterance using do_svm()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_cb])
            utterance_id += 1

            if utterance_id == 500:
                print(utterance_id)

# function to label a test set using the Maximum Entropy Model algorithm and to save results in a new file
def do_test_set_mem_hs(utterances_test, filename, lex):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Hate Speech"])             # header

        x = 0
        for utterance in utterances_test:
            class_hs = do_mem_hs(utterance, lex)                       # determine class of the utterance using do_svm()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_hs])
            x += 1

            if x == 500:
                print(x)

def do_test_set_mem_strength(utterances_test, filename, lex):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying Strength"])             # header

        x = 0
        for utterance in utterances_test:
            class_strength = do_mem_strength(utterance, lex)                       # determine class of the utterance using do_svm()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_strength])
            x += 1

            if x == 500:
                print(x)

# function to label a test set using the Maximum Entropy Model algorithm and Sentiment and to save results in a new file
def do_test_set_mem_sent_hs(utterances_test, filename, lex, file, column, sentimentfile_train, sentimentfile_test):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Hate Speech"])             # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities(sentimentfile_train, file, column)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances_test:
            class_hs = do_sentiment_mem_hs(utterance, lex, list_of_sentiments[utterance_id], sentimentlist)                       # determine class of the utterance using do_svm()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_hs])
            utterance_id += 1

            if utterance_id == 500:
                print(utterance_id)

# function to label a test set using the Maximum Entropy Model algorithm and Sentiment and to save results in a new file
def do_test_set_mem_sent_strength(utterances_test, filename, lex, file, column, sentimentfile_train, sentimentfile_test):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying Strength"])             # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities_strengths(sentimentfile_train, file, column)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances_test:
            class_strength = do_sentiment_mem_strength(utterance, lex, list_of_sentiments[utterance_id], sentimentlist)                       # determine class of the utterance using do_svm()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_strength])
            utterance_id += 1

            if utterance_id == 500:
                print(utterance_id)

utterance = machine_learning_processing.process_utterance("Yup. I can't stand this shit. The left screams and yells Black Lives Matter and the minute a black man or woman disappear")
utterance2 = machine_learning_processing.process_utterance("ban islam")
utterance3 = machine_learning_processing.process_utterance("This is our president. WHO talks like that?!? Our leader does. I cant. How embarrassing. A disgrace to the office.")

#do_mem(utterance, "lexicon_with_occurences.txt")
#do_mem(utterance2, "lexicon_with_occurences.txt")
#do_mem(utterance3, "lexicon_with_occurences.txt")

test_list = machine_learning_processing.process_data("test_set.csv")

#do_test_set_mem(test_list, "twitter_bullying_mem2.csv", "lexicon_with_occurences.txt")
#do_test_set_mem_sent(test_list, "twitter_bullying_mem_sent.csv", "lexicon_with_occurences.txt", "train_set.csv", 7, "train_set_with_sentiment.csv", "test_set_with_sentiment.csv")
#do_test_set_mem(test_list, "twitter_bullying_mem3.csv", "lexicon_with_occurences2.txt")

#do_test_set_mem(test_list, "twitter_bullying_mem_c.csv", "lexicon_with_occurences.txt")
#do_test_set_mem_sent(test_list, "twitter_bullying_mem_sent_c.csv", "lexicon_with_occurences.txt", "train_set.csv", 7, "train_set_with_sentiment.csv", "test_set_with_sentiment.csv")

#estimation.test_results("test_set.csv", 7, "twitter_bullying_mem2.csv", 1)
#estimation.test_results("test_set.csv", 7, "twitter_bullying_mem_sent.csv", 1)
#estimation.test_results("test_set.csv", 7, "twitter_bullying_mem3.csv", 1)

#estimation.test_results("test_set.csv", 7, "twitter_bullying_mem_c.csv", 1)
#estimation.test_results("test_set.csv", 7, "twitter_bullying_mem_sent_c.csv", 1)

# hate speech
#do_test_set_mem_hs(test_list, "twitter_bullying_mem_hs.csv", "lexicon_with_occurences_hs.txt")
#estimation.test_results("test_set.csv", 9, "twitter_bullying_mem_hs.csv", 1)

# hate speech with sentiment
#do_test_set_mem_sent(test_list, "twitter_bullying_mem_sent_hs.csv", "lexicon_with_occurences_hs.txt", "train_set.csv", 9, "train_set_with_sentiment.csv", "test_set_with_sentiment.csv")
#estimation.test_results("test_set.csv", 9, "twitter_bullying_mem_sent_hs.csv", 1)

# strength
test_s_list = machine_learning_processing.process_data("test_cb_set.csv")
#do_test_set_mem_strength(test_s_list, "twitter_bullying_mem_strength.csv", "lexicon_with_occurences_cb.txt")
#estimation.test_results_strengths("test_cb_set.csv", 8, "twitter_bullying_mem_strength.csv", 1)

# strength with sentiment
#do_test_set_mem_sent_strength(test_s_list, "twitter_bullying_mem_sent_strength.csv", "lexicon_with_occurences_cb.txt", "train_cb_set.csv", 8, "train_cb_set_with_sentiment.csv", "test_cb_set_with_sentiment.csv")
#estimation.test_results_strengths("test_cb_set.csv", 8, "twitter_bullying_mem_sent_strength.csv", 1)





