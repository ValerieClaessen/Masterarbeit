import csv
import machine_learning_processing
import estimation
import senti_strength
import math
import compare_tweets_cyberbullying
import compare_tweets_hatespeech
import compare_bullying_traces

# function to use the Maximum Entropy Model algorithm and Sentiment and Pos-Tagging on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_mem_sent_pos(utterance, utterance_unprocessed, lex, sentiment, sentimentlist):
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
    #p_cyberbullying_utterance = e_cyberbullying_feature_sum / (e_cyberbullying_feature_sum + e_no_cyberbullying_feature_sum)
    p_no_cyberbullying_utterance = e_no_cyberbullying_feature_sum / (e_cyberbullying_feature_sum + e_no_cyberbullying_feature_sum)

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
        #p_cyberbullying_utterance = p_cyberbullying_utterance * p_neg_cb
        p_no_cyberbullying_utterance = p_no_cyberbullying_utterance * p_neg_no_cb

    # probability that utterance is in class cyberbullying / no cyberbullying based on pos-tagging
    cb_pos_prob = compare_tweets_cyberbullying.compare_vec_tweet(utterance_unprocessed, 3)
    no_cb_pos_prob = 1 - cb_pos_prob
    cb_pos_prob = 5 * cb_pos_prob

    # multiply p_class_utterance by the pos-tag-class-probability
    # if it's zero, multiply by 0.1 to avoid having 0.0 as the final value
    if cb_pos_prob != 0 and no_cb_pos_prob != 0:
        p_cyberbullying_utterance = p_cyberbullying_utterance * cb_pos_prob
        p_no_cyberbullying_utterance = p_no_cyberbullying_utterance * no_cb_pos_prob
    elif cb_pos_prob == 0:
        p_cyberbullying_utterance = p_cyberbullying_utterance * 0.1
        p_no_cyberbullying_utterance = p_no_cyberbullying_utterance * no_cb_pos_prob
    else:
        p_cyberbullying_utterance = p_cyberbullying_utterance * cb_pos_prob
        p_no_cyberbullying_utterance = p_no_cyberbullying_utterance * 0.1

    values = [p_cyberbullying_utterance, p_no_cyberbullying_utterance]

    if max(values) == values[0]:                                    # determine class (max P(class|tweet))
        cb_class = 1
    elif contains_curses == True:                                                               # utterances that contain curses will automatically be labeled as cyberbullying
        cb_class = 1
    else:
        cb_class = 0

    return cb_class

# function to use the Maximum Entropy Model algorithm and Sentiment and Pos-Taggin on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_mem_sent_pos_hs(utterance, utterance_unprocessed, lex, sentiment, sentimentlist):
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

    # probability that utterance is in class cyberbullying / no cyberbullying based on pos-tagging
    hs_pos_prob = compare_tweets_cyberbullying.compare_vec_tweet(utterance_unprocessed, 3)
    no_hs_pos_prob = 1 - hs_pos_prob
    hs_pos_prob = 5 * hs_pos_prob

    # multiply p_class_utterance by the pos-tag-class-probability
    # if it's zero, multiply by 0.1 to avoid having 0.0 as the final value
    if hs_pos_prob != 0 and no_hs_pos_prob != 0:
        p_hs_utterance = p_hs_utterance * hs_pos_prob
        p_no_hs_utterance = p_no_hs_utterance * no_hs_pos_prob
    elif hs_pos_prob == 0:
        p_hs_utterance = p_hs_utterance * 0.1
        p_no_hs_utterance = p_no_hs_utterance * no_hs_pos_prob
    else:
        p_hs_utterance = p_hs_utterance * hs_pos_prob
        p_no_hs_utterance = p_no_hs_utterance * 0.1

    values = [p_hs_utterance, p_no_hs_utterance]

    if max(values) == values[0]:                                    # determine class (max P(class|tweet))
        hs_class = 1
    else:
        hs_class = 0

    return hs_class

# function to use the Maximum Entropy Model algorithm and Sentiment on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_mem_sent_pos_strength(utterance, utterance_unprocessed, lex, sentiment, sentimentlist):
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

    # most likely strength of cyberbullying based on pos-tagging
    probable_strength = compare_tweets_hatespeech.compare_vec_tweet_strenght(utterance_unprocessed, 4)

    # multiply p_class_utterance by two for the most probable strength
    if probable_strength == 1:
        p_s1_utterance = p_s1_utterance * 2
    elif probable_strength == 2:
        p_s2_utterance = p_s2_utterance * 2
    elif probable_strength == 3:
        p_s3_utterance = p_s3_utterance * 2
    elif probable_strength == 4:
        p_s4_utterance = p_s4_utterance * 2
    elif probable_strength == 5:
        p_s5_utterance = p_s5_utterance * 2

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

    return strength_class

# function to use the Maximum Entropy Model algorithm and Sentiment and Pos-Tagging on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_mem_sent_pos_bt(utterance, utterance_unprocessed, lex, sentiment, sentimentlist):
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
    #p_cyberbullying_utterance = e_cyberbullying_feature_sum / (e_cyberbullying_feature_sum + e_no_cyberbullying_feature_sum)
    p_no_cyberbullying_utterance = e_no_cyberbullying_feature_sum / (e_cyberbullying_feature_sum + e_no_cyberbullying_feature_sum)

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
        #p_cyberbullying_utterance = p_cyberbullying_utterance * p_neg_cb
        p_no_cyberbullying_utterance = p_no_cyberbullying_utterance * p_neg_no_cb

    # probability that utterance is in class cyberbullying / no cyberbullying based on pos-tagging
    cb_pos_prob = compare_bullying_traces.compare_vec_bullying_traces(utterance_unprocessed, 3)
    no_cb_pos_prob = 1 - cb_pos_prob
    cb_pos_prob = 5 * cb_pos_prob

    # multiply p_class_utterance by the pos-tag-class-probability
    # if it's zero, multiply by 0.1 to avoid having 0.0 as the final value
    if cb_pos_prob != 0 and no_cb_pos_prob != 0:
        p_cyberbullying_utterance = p_cyberbullying_utterance * cb_pos_prob
        p_no_cyberbullying_utterance = p_no_cyberbullying_utterance * no_cb_pos_prob
    elif cb_pos_prob == 0:
        p_cyberbullying_utterance = p_cyberbullying_utterance * 0.1
        p_no_cyberbullying_utterance = p_no_cyberbullying_utterance * no_cb_pos_prob
    else:
        p_cyberbullying_utterance = p_cyberbullying_utterance * cb_pos_prob
        p_no_cyberbullying_utterance = p_no_cyberbullying_utterance * 0.1

    values = [p_cyberbullying_utterance, p_no_cyberbullying_utterance]

    if max(values) == values[0]:                                    # determine class (max P(class|tweet))
        cb_class = 1
    elif contains_curses == True:                                                               # utterances that contain curses will automatically be labeled as cyberbullying
        cb_class = 1
    else:
        cb_class = 0

    return cb_class

# function to label a test set using the Maximum Entropy Model algorithm and Sentiment and to save results in a new file
def do_test_set_mem_sent_pos(utterances_test, utterances_unprocessed, filename, lex, file, column, sentimentfile_train, sentimentfile_test):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying"])             # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities(sentimentfile_train, file, column)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances_test:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            class_cb = do_mem_sent_pos(utterance, utterance_unprocessed, lex, list_of_sentiments[utterance_id], sentimentlist)                       # determine class of the utterance using do_svm()

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

# function to label a test set using the Maximum Entropy Model algorithm and Sentiment and to save results in a new file
def do_test_set_mem_sent_pos_hs(utterances_test, utterances_unprocessed, filename, lex, file, column, sentimentfile_train, sentimentfile_test):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Hate Speech"])             # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities(sentimentfile_train, file, column)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances_test:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            class_hs = do_mem_sent_pos_hs(utterance, utterance_unprocessed, lex, list_of_sentiments[utterance_id], sentimentlist)                       # determine class of the utterance using do_svm()

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

# function to label a test set using the Maximum Entropy Model algorithm and Sentiment and to save results in a new file
def do_test_set_mem_sent_pos_strength(utterances_test, utterances_unprocessed, filename, lex, file, column, sentimentfile_train, sentimentfile_test):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying Strength"])             # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities_strengths(sentimentfile_train, file, column)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances_test:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            class_strength = do_mem_sent_pos_strength(utterance, utterance_unprocessed, lex, list_of_sentiments[utterance_id], sentimentlist)                       # determine class of the utterance using do_svm()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_strength])

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

# function to label a test set using the Maximum Entropy Model algorithm and Sentiment and to save results in a new file
def do_test_set_mem_sent_pos_bt(utterances_test, utterances_unprocessed, filename, lex, file, column, sentimentfile_train, sentimentfile_test):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying"])             # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities(sentimentfile_train, file, column)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances_test:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            class_cb = do_mem_sent_pos_bt(utterance, utterance_unprocessed, lex, list_of_sentiments[utterance_id], sentimentlist)                       # determine class of the utterance using do_svm()

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

# cyberbullying
#test_list = machine_learning_processing.process_data("test_set.csv", 5)
#test_list_unprocessed = machine_learning_processing.make_list_of_column("test_set.csv", 5)
#do_test_set_mem_sent_pos(test_list, test_list_unprocessed, "twitter_bullying_mem_final.csv", "lexicon_with_occurences.txt", "train_set.csv", 7, "train_set_with_sentiment.csv", "test_set_with_sentiment.csv")
#estimation.test_results("test_set.csv", 7, "twitter_bullying_mem_final.csv", 1)

#estimation.test_results("test_set.csv", 7, "twitter_bullying_mem_sent_c.csv", 1)

# hate speech
#do_test_set_mem_sent_pos_hs(test_list, test_list_unprocessed, "twitter_bullying_mem_final_hs.csv", "lexicon_with_occurences_hs.txt", "train_set.csv", 9, "train_set_with_sentiment.csv", "test_set_with_sentiment.csv")
#estimation.test_results("test_set.csv", 9, "twitter_bullying_mem_final_hs.csv", 1)

#estimation.test_results("test_set.csv", 9, "twitter_bullying_mem_sent_hs.csv", 1)

# strengths
#test_s_list = machine_learning_processing.process_data("test_cb_set.csv", 5)
#test_s_list_unprocessed = machine_learning_processing.make_list_of_column("test_cb_set.csv", 5)
#do_test_set_mem_sent_pos_strength(test_s_list, test_s_list_unprocessed,  "twitter_bullying_mem_final_strength.csv", "lexicon_with_occurences_cb.txt", "train_cb_set.csv", 8, "train_cb_set_with_sentiment.csv", "test_cb_set_with_sentiment.csv")
#estimation.test_results_strengths("test_cb_set.csv", 8, "twitter_bullying_mem_final_strength.csv", 1)

#estimation.test_results_strengths("test_cb_set.csv", 8, "twitter_bullying_mem_sent_strength.csv", 1)

# bullying traces
#test_list_bt = machine_learning_processing.process_data("bullying_traces_test.csv", 2)
#test_list_bt_unprocessed = machine_learning_processing.make_list_of_column("bullying_traces_test.csv", 2)
#do_test_set_mem_sent_pos_bt(test_list_bt, test_list_bt_unprocessed, "bullying_traces_mem_final.csv", "lexicon_with_occurences_bt.txt", "bullying_traces_train.csv", 3, "bullying_traces_train_with_sentiment.csv", "bullying_traces_test_with_sentiment.csv")
#estimation.test_results("bullying_traces_test.csv", 3, "bullying_traces_mem_final.csv", 1)

#estimation.test_results("bullying_traces_test.csv", 3, "bullying_traces_mem.csv", 1)
