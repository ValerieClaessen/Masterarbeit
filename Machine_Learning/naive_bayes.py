import csv
import machine_learning_processing
import estimation

# global variables
freq_cb = 0
freq_no_cb = 0

# function to estimate the frequencies of each class in the training dataset
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

estimate_class_frequency("twitter_bullying_training.csv")

#function to use the naive bayes algorithm on an utterance of the test_set
# returns the class for the utterances assigned by the algorithm
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
    p_class_utterance_1 = p_utterance_class_1 * freq_cb                 # p(class|tweet)
    p_class_utterance_0 = p_utterance_class_0 * freq_no_cb

    # class with the higher probability will be assigned to the utterance
    values = [p_class_utterance_1, p_class_utterance_0]
    if max(values) == values[0]:                                        # determine class (max p(class|tweet))
        class_cb = 1
    else:
        class_cb = 0
    #print(class_cb)

    return class_cb

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

utterance = machine_learning_processing.process_utterance("Yup. I can't stand this shit. The left screams and yells Black Lives Matter and the minute a black man or woman disappear")
utterance2 = machine_learning_processing.process_utterance("ban islam")
utterance3 = machine_learning_processing.process_utterance("This is our president. WHO talks like that?!? Our leader does. I cant. How embarrassing. A disgrace to the office.")

test_list = machine_learning_processing.process_data("twitter_bullying_test.csv")

#do_naive_bayes(utterance, "lexicon_with_occurences.txt")
#do_naive_bayes(utterance2, "lexicon_with_occurences.txt")
#do_naive_bayes(utterance3, "lexicon_with_occurences.txt")

#do_test_set_naive_bayes(test_list, "twitter_bullying_naive_bayes_test.csv", "lexicon_with_occurences.txt")
#do_test_set_naive_bayes(training_list, "twitter_bullying_naive_bayes_test_no_laplace.csv", "lexicon_with_occurences_without_laplace.txt")

estimation.test_results("twitter_bullying_test.csv", 7, "twitter_bullying_naive_bayes_test.csv", 1)