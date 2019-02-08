#function to further process the datasets
# function to process twitter data
import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import math
from decimal import *

# global variables
freq_cb = 0
freq_no_cb = 0

def process_data(file):
    """
    Before we can analyize our data, we need to process it.
    This includes:
        - converting all words to lowercase
        - deleting punctuation marks
        - deleting numbers
        - tokenize tweets to get a list of words
        - deleting stopwords or not deleting stopwords depending on the results
        - stem all words

    This function will return a list of lists containing all stemmed words of every tweets (data_list)
    """

    data_list = []
    punctuation = ['.', ',', ';', '!', '?', '(', ')', '[', ']',             # list of english punctuation marks (used in tweets)
                   '&', ':', '-', '/', '\\', '$', '*', '"', "'", '+',
                   '=', '@', '%', '~', '{', '}', '|', '<', '>', '`', '']
    stopwords = nltk.corpus.stopwords.words("english")                      # list of english stopwords

    with open(file, 'r') as csvfile:                                        # collect tweets from csv-data in list
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                  # skip header
        for row in reader:
            data_list.append(row[5])

    for index, element in enumerate(data_list):
        element = element.lower()                                           # tweet to lowercase
        for mark in punctuation:
            element = element.replace(mark, '')                             # delete punctuation marks
        element = ''.join([i for i in element if not i.isdigit()])          # delete numbers
        element = word_tokenize(element)                                    # tokenize tweet
        element = [w for w in element if w not in stopwords]                # delete stopwords (depending on results we may not remvove stopwords)

        for i, word in enumerate(element):                                  # stem words in tweet
            word = nltk.SnowballStemmer("english").stem(word)
            element[i] = str(word)

        data_list[index] = element

    return data_list

test_list = process_data("twitter_bullying_test.csv")
#print(test_list)

# function to make a lexicon containing all vocabulary of our dataset
def make_lexicon(data_list):
    lex = []

    for list in data_list:
        for word in list:
            if word not in lex:
                lex.append(word)
            #else:
                #print("already in lexicon")

    lex = sorted(lex)                                                       # sort list alphabetically

    return lex

test_lex = make_lexicon(test_list)
#print(test_lex)

# function to save lexicon in a txt file
def lex_into_txt(lex):
    with open("lexicon.txt", 'w') as f:
        for word in lex:
            f.write("%s\n" % word)

#lex_into_txt(test_lex)

# function to make a list of all values from a column from a dataset
def make_list_of_column(file, column):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)  # skip header

        list = []
        for row in reader:
            list.append(row[column])

    return list

# function to make a lexicon containing all vocabulary of our dataset + their relative occurences in tweets labeled as
# cyberbullying / no cyberbullying
def make_lexicon_with_occurence(file, column, lex, utterances):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                  # skip header

        lex_size = len(lex)                                                 # size of the lexicon that is needed to apply laplace smoothing
        cyberbuylling_list = make_list_of_column(file, column)              # list of all cyberbullying values

        # write new lexicon that contains the word plus its relative occurence in both classes (cyberbullying & no_cyberbullying)
        file = open("lexicon_with_occurences.txt", "w")
        for word in lex:
            glob_count = 0
            cyberbullying_count = 0
            no_cyberbullying_count = 0

            # count how often each word occurs in our dataset
            for utterance in utterances:
                utterance_string = ""
                for item in utterance:
                    utterance_string = utterance_string + " " + item
                glob_count += utterance_string.count(word)

            x = 0
            for value in cyberbuylling_list:
                sentence = utterances[x]
                sentence_string = ""
                for item in sentence:
                    sentence_string = sentence_string + " " + item

                if value == 1 or value == "1":
                    cyberbullying_count += sentence_string.count(word)      # count how often each word occurs in utterances labeled as cyberbullying
                else:
                    no_cyberbullying_count += sentence_string.count(word)   # count how often each word occurs in utterances labeled as no_cyberbullying
                x += 1

            #print(word + " " + str(glob_count) + " " + str(cyberbullying_count) + " " + str(no_cyberbullying_count))

            # with Laplace Smoothing
            # We add 1 to all word occurences in the two classes and divide that value by their total occurences plus the size
            # of the lexicon. The result is multiplied by 100 to achieve more practical values.
            occurence_cyberbullying = ((cyberbullying_count + 1) / (glob_count + lex_size)) * 100
            occurence_no_cyberbullying = ((no_cyberbullying_count + 1) / (glob_count + lex_size)) * 100

            # without laplace_smoothing
            #occurence_cyberbullying = cyberbullying_count / glob_count
            #occurence_no_cyberbullying = no_cyberbullying_count / glob_count

            # the word and its relative occurence in each class is saved into a new lexicon (lexicon_with_occurences.txt)
            line = word + " " + str(round(occurence_cyberbullying, 3)) + " " + str(round(occurence_no_cyberbullying, 3)) + "\n"
            file.write(line)
        file.close()

#make_lexicon_with_occurence("twitter_bullying_test.csv", 7, test_lex, test_list)

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
    with open("twitter_bullying_naive_bayes_test_no_laplace.csv", 'w') as f:
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

#do_naive_bayes(test_list, "lexicon_with_occurences.txt")
#do_naive_bayes(test_list, "lexicon_with_occurences_without_laplace.txt")

# function to test the results of the algorithms
def test_results(file1, file2):
    # make lists of assigned cyberbullying values (0 / 1)
    cyberbullying1 = make_list_of_column(file1, 7)
    cyberbullying2 = make_list_of_column(file2, 1)

    right_cyberbullying = 0                     # utterance contains cyberbullying and was assigned cyberbullying
    right_no_cyberbullying = 0                  # utterance doesn't contain cyberbullying and was assigned no_cyberbullying
    wrong_cyberbullying = 0                     # utterance doesn't contain cyberbullying and was assigned cyberbullying
    wrong_no_cyberbullying = 0                  # utterance contains cyberbullying and was assigned no_cyberbullying

    cyberbullying = 0                           # number of utterances that contain cyberbullying
    no_cyberbullying = 0                        # number of utterances that don't contain cyberbullying

    # compare assigned cyberbullying values
    x = 0
    for item in cyberbullying1:
        if item == 1 or item == "1":
            cyberbullying += 1
            if cyberbullying2[x] == 1 or cyberbullying2[x] == "1":
                right_cyberbullying += 1
            elif cyberbullying2[x] == 0 or cyberbullying2[x] == "0":
                wrong_no_cyberbullying += 1
        if item == 0 or item == "0":
            no_cyberbullying += 1
            if cyberbullying2[x] == 0 or cyberbullying2[x] == "0":
                right_no_cyberbullying += 1
            elif cyberbullying2[x] == 1 or cyberbullying2[x] == "1":
                wrong_cyberbullying += 1
        x += 1

    print(cyberbullying, no_cyberbullying)
    print(right_cyberbullying, right_no_cyberbullying, wrong_cyberbullying, wrong_no_cyberbullying)

#test_results("twitter_bullying_test.csv", "twitter_bullying_naive_bayes_test.csv")

#function to use the support vector machine algorithm on a dataset
def do_svm():
    return

#function to use the maximum entropy model algorithm on a dataset
def do_mem():
    return