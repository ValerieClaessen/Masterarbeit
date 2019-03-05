import csv
import machine_learning_processing
import estimation
import senti_strength
import math
import compare_labeled_data
import compare_twitter_bullying

# function to use the Maximum Entropy Model algorithm and Sentiment and Pos-Tagging on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_mem_sent_pos_ld(utterance, utterance_unprocessed, lex, sentiment, sentimentlist):
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
    cb_pos_prob = compare_labeled_data.compare_vec_labeled_data_cb(utterance_unprocessed, 3)
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

# function to use the Maximum Entropy Model algorithm and Sentiment and Pos-Tagging on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_mem_sent_pos_ths(utterance, utterance_unprocessed, lex, sentiment, sentimentlist):
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
    cb_pos_prob = compare_twitter_bullying.compare_vec_twitter_bullying_cb(utterance_unprocessed, 3)
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
def do_mem_sent_pos_hs_ld(utterance, utterance_unprocessed, lex, sentiment, sentimentlist):
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
    hs_pos_prob = compare_labeled_data.compare_vec_labeled_data_hs(utterance_unprocessed, 3)
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

# function to use the Maximum Entropy Model algorithm and Sentiment and Pos-Taggin on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_mem_sent_pos_hs_ths(utterance, utterance_unprocessed, lex, sentiment, sentimentlist):
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
    hs_pos_prob = compare_twitter_bullying.compare_vec_twitter_bullying_hs(utterance_unprocessed, 3)
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

# function to label a test set using the Maximum Entropy Model algorithm and Sentiment and to save results in a new file
def do_test_set_mem_sent_pos_ld(utterances_test, utterances_unprocessed, filename, lex, file, column, sentimentfile_train, sentimentfile_test, mode):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying"])             # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities_other_datasets(sentimentfile_train, file, column, mode)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances_test:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            class_cb = do_mem_sent_pos_ld(utterance, utterance_unprocessed, lex, list_of_sentiments[utterance_id], sentimentlist)                       # determine class of the utterance using do_svm()

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

# function to label a test set using the Maximum Entropy Model algorithm and Sentiment and to save results in a new file
def do_test_set_mem_sent_pos_ths(utterances_test, utterances_unprocessed, filename, lex, file, column, sentimentfile_train, sentimentfile_test, mode):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying"])             # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities_other_datasets(sentimentfile_train, file, column, mode)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances_test:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            class_cb = do_mem_sent_pos_ths(utterance, utterance_unprocessed, lex, list_of_sentiments[utterance_id], sentimentlist)                       # determine class of the utterance using do_svm()

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

# function to label a test set using the Maximum Entropy Model algorithm and Sentiment and to save results in a new file for other datasets
def do_test_set_mem_sent_pos_hs_ld(utterances_test, utterances_unprocessed, filename, lex, file, column, sentimentfile_train, sentimentfile_test, mode):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Hate Speech"])             # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities_other_datasets(sentimentfile_train, file, column, mode)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances_test:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            class_hs = do_mem_sent_pos_hs_ld(utterance, utterance_unprocessed, lex, list_of_sentiments[utterance_id], sentimentlist)                       # determine class of the utterance using do_svm()

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

# function to label a test set using the Maximum Entropy Model algorithm and Sentiment and to save results in a new file for other datasets
def do_test_set_mem_sent_pos_hs_ths(utterances_test, utterances_unprocessed, filename, lex, file, column, sentimentfile_train, sentimentfile_test, mode):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Hate Speech"])             # header

        sentimentlist = senti_strength.estimate_sentiment_probabilities_other_datasets(sentimentfile_train, file, column, mode)
        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile_test, 1)

        utterance_id = 0
        for utterance in utterances_test:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            class_hs = do_mem_sent_pos_hs_ths(utterance, utterance_unprocessed, lex, list_of_sentiments[utterance_id], sentimentlist)                       # determine class of the utterance using do_svm()

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
test_list_ld = machine_learning_processing.process_data("labeled_data_test.csv", 6)
test_list_ld_unprocessed = machine_learning_processing.make_list_of_column("labeled_data_test.csv", 6)
do_test_set_mem_sent_pos_ld(test_list_ld, test_list_ld_unprocessed, "labeled_data_mem_final.csv", "lexicon_with_occurences_ld.txt", "labeled_data_train.csv", 5, "labeled_data_train_with_sentiment.csv", "labeled_data_test_with_sentiment.csv", 2)
do_test_set_mem_sent_pos_hs_ld(test_list_ld, test_list_ld_unprocessed, "labeled_data_mem_final_hs.csv", "lexicon_with_occurences_hs_ld.txt", "labeled_data_train.csv", 5, "labeled_data_train_with_sentiment.csv", "labeled_data_test_with_sentiment.csv", 2)
estimation.test_results("labeled_data_test.csv", 5, "labeled_data_mem_final.csv", 1)
estimation.test_results("labeled_data_test.csv", 5, "labeled_data_mem_final_hs.csv", 1)

estimation.test_results("labeled_data_test.csv", 5, "labeled_data_mem.csv", 1)
estimation.test_results("labeled_data_test.csv", 5, "labeled_data_mem_hs.csv", 1)

# twitter hate speech
test_list_ths = machine_learning_processing.process_data("twitter_hate_speech_test.csv", 1)
test_list_ths_unprocessed = machine_learning_processing.make_list_of_column("twitter_hate_speech_test.csv", 1)
do_test_set_mem_sent_pos_ths(test_list_ths, test_list_ths_unprocessed, "twitter_hate_speech_mem_final.csv", "lexicon_with_occurences_ths.txt", "twitter_hate_speech_train.csv", 2, "twitter_hate_speech_train_with_sentiment.csv", "twitter_hate_speech_test_with_sentiment.csv", 3)
do_test_set_mem_sent_pos_hs_ths(test_list_ths, test_list_ths_unprocessed, "twitter_hate_speech_mem_final_hs.csv", "lexicon_with_occurences_hs_ths.txt", "twitter_hate_speech_train.csv", 2, "twitter_hate_speech_train_with_sentiment.csv", "twitter_hate_speech_test_with_sentiment.csv", 3)
estimation.test_results("twitter_hate_speech_test.csv", 2, "twitter_hate_speech_mem_final.csv", 1)
estimation.test_results("twitter_hate_speech_test.csv", 2, "twitter_hate_speech_mem_final_hs.csv", 1)

estimation.test_results("twitter_hate_speech_test.csv", 2, "twitter_hate_speech_mem.csv", 1)
estimation.test_results("twitter_hate_speech_test.csv", 2, "twitter_hate_speech_mem_hs.csv", 1)