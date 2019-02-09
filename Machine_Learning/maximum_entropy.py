import csv
import machine_learning_processing
import estimation
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
    for word in utterance:
        for line in open(lex):
            if word in line:
                line_split = line.split()
                cyberbullying_feature_sum += float(line_split[1])
                no_cyberbullying_feature_sum += float(line_split[2])

    # estimating P(class|tweet)
    e = math.e
    e_cyberbullying_feature_sum = e ** cyberbullying_feature_sum
    e_no_cyberbullying_feature_sum = e ** no_cyberbullying_feature_sum

    p_cyberbullying_utterance = e_cyberbullying_feature_sum / (e_cyberbullying_feature_sum + e_no_cyberbullying_feature_sum)
    p_no_cyberbullying_utterance = e_no_cyberbullying_feature_sum / (e_no_cyberbullying_feature_sum + e_no_cyberbullying_feature_sum)
    values = [p_cyberbullying_utterance, p_no_cyberbullying_utterance]

    if max(values) == values[0]:                                    # determine class (max P(class|tweet))
        cb_class = 1
    else:
        cb_class = 0
    #print(cb_class)

    return cb_class


# function to label a test set using the Maximum Entropy Model algorithm and to save results in a new file
def do_test_set_mem(utterances_test, filename, lex):
    # annotation using maximum entropy model will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying"])             # header

        for utterance in utterances_test:
            class_cb = do_mem(utterance, lex)                       # determine class of the utterance using do_svm()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_cb])


utterance = machine_learning_processing.process_utterance("Yup. I can't stand this shit. The left screams and yells Black Lives Matter and the minute a black man or woman disappear")
utterance2 = machine_learning_processing.process_utterance("ban islam")
utterance3 = machine_learning_processing.process_utterance("This is our president. WHO talks like that?!? Our leader does. I cant. How embarrassing. A disgrace to the office.")

#do_mem(utterance, "lexicon_with_occurences.txt")
#do_mem(utterance2, "lexicon_with_occurences.txt")
#do_mem(utterance3, "lexicon_with_occurences.txt")

test_list = machine_learning_processing.process_data("twitter_bullying_test.csv")

#do_test_set_mem(test_list, "twitter_bullying_mem_test.csv", "lexicon_with_occurences.txt")

estimation.test_results("twitter_bullying_test.csv", 7, "twitter_bullying_mem_test.csv", 1)



