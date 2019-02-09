import csv
import machine_learning_processing

# global variables
freq_cb = 0
freq_no_cb = 0

# function to estimate the frequencies of each class in the dataset
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

estimate_class_frequency("twitter_bullying_test.csv")

#function to use the naive bayes algorithm on a dataset
def do_naive_bayes(utterances, lex):
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

    # annotation using naive_bayes will be saved in a new file
    with open("twitter_bullying_naive_bayes_test.csv", 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying"]) # header

        for utterance in utterances:
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

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_cb])

test_list = machine_learning_processing.process_data("twitter_bullying_test.csv")
#print(test_list)

do_naive_bayes(test_list, "lexicon_with_occurences.txt")
#do_naive_bayes(test_list, "lexicon_with_occurences_without_laplace.txt")