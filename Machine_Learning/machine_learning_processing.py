import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

# function to further process the datasets
def process_data(file, class_column):
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
    punctuation = ['.', ',', ';', '!', '?', '(', ')', '[', ']',             # list of english punctuation marks (used in utterances)
                   '&', ':', '-', '/', '\\', '$', '*', '"', "'", '+',
                   '=', '@', '%', '~', '{', '}', '|', '<', '>', '`', '']
    stopwords = nltk.corpus.stopwords.words("english")                      # list of english stopwords

    with open(file, 'r') as csvfile:                                        # collect tweets from csv-data in list
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                  # skip header
        for row in reader:
            data_list.append(row[class_column])

    for index, element in enumerate(data_list):
        element = element.lower()                                           # utterance to lowercase
        for mark in punctuation:
            element = element.replace(mark, '')                             # delete punctuation marks
        element = ''.join([i for i in element if not i.isdigit()])          # delete numbers
        element = word_tokenize(element)                                    # tokenize utterance
        element = [w for w in element if w not in stopwords]                # delete stopwords (depending on results we may not remvove stopwords)

        for i, word in enumerate(element):                                  # stem words in utterance
            word = nltk.SnowballStemmer("english").stem(word)
            element[i] = str(word)

        data_list[index] = element

    return data_list

#train_list = process_data("twitter_bullying_training.csv", 5)
#print(test_list)
#train_list = process_data("train_set.csv", 5)
#train_list_cb = process_data("train_cb_set.csv",5)
#train_list_bt = process_data("bullying_traces_train.csv", 2)
#train_list_ld = process_data("labeled_data_train.csv", 6)
#train_list_ths = process_data("twitter_hate_speech_train.csv", 1)

# function to process an utterance of the test set
def process_utterance(utterance):
    """
    Before we can label our utterance from the test set, we need to process it.
    This includes:
        - converting all words to lowercase
        - deleting punctuation marks
        - deleting numbers
        - tokenize tweets to get a list of words
        - deleting stopwords or not deleting stopwords depending on the results
        - stem all words

    This function will the processed utterance.
    """

    punctuation = ['.', ',', ';', '!', '?', '(', ')', '[', ']',             # list of english punctuation marks (used in utterances)
                   '&', ':', '-', '/', '\\', '$', '*', '"', "'", '+',
                   '=', '@', '%', '~', '{', '}', '|', '<', '>', '`', '']
    stopwords = nltk.corpus.stopwords.words("english")                      # list of english stopwords

    utterance = utterance.lower()                                           # utterance to lowercase
    for mark in punctuation:
        utterance = utterance.replace(mark, '')                             # delete punctuation marks
    utterance = ''.join([i for i in utterance if not i.isdigit()])          # delete numbers
    utterance = word_tokenize(utterance)                                    # tokenize utterance
    utterance = [w for w in utterance if w not in stopwords]                # delete stopwords (depending on results we may not remvove stopwords)

    for i, word in enumerate(utterance):                                    # stem words in utterance
        word = nltk.SnowballStemmer("english").stem(word)
        utterance[i] = str(word)

    return utterance

#test_utterance = process_utterance("Yup. I can't stand this shit. The left screams and yells Black Lives Matter and the minute a black man or woman disappear")
#print(test_utterance)

# function to make a lexicon containing all vocabulary of our dataset
def make_lexicon(data_list, mode):
    lex = []

    for list in data_list:
        for word in list:
            if word not in lex:
                lex.append(word)
            #else:
                #print("already in lexicon")

    lex = sorted(lex)                                                       # sort list alphabetically

    # only words that occur at least twice in the dataset will be part of the lexicon
    lex2 = []
    for word in lex:
        count = sum(x.count(word) for x in data_list)
        if count > 1:
            lex2.append(word)

    if mode == 1:
        return lex
    else:
        return lex2

#test_lex = make_lexicon(test_list)
#print(test_lex)
#lex = make_lexicon(train_list, 1)
#lex2 = make_lexicon(train_list, 0)
#lex = make_lexicon(train_list_cb, 1)
#lex_bt = make_lexicon(train_list_bt, 1)
#lex_ld = make_lexicon(train_list_ld, 1)
#lex_ths = make_lexicon(train_list_ths, 1)

# function to save lexicon in a txt file
def lex_into_txt(lex, filename):
    with open(filename, 'w') as f:
        for word in lex:
            f.write("%s\n" % word)

#lex_into_txt(test_lex)
#lex_into_txt(lex, "lexicon.txt")
#lex_into_txt(lex2, "lexicon2.txt")
#lex_into_txt(lex, "lexicon_cb.txt")
#lex_into_txt(lex_bt, "lexicon_bt.txt")
#lex_into_txt(lex_ld, "lexicon_ld.txt")
#lex_into_txt(lex_ths, "lexicon_ths.txt")

# function to make a list of all values from a column from a dataset
def make_list_of_column(file, column):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)  # skip header

        list = []
        for row in reader:
            list.append(row[column])

    return list

# function to make a list of all curse words
def make_list_of_curse_words(file):
    with open(file, 'r') as f:
        curses = [line.strip() for line in f]

    return curses

#curses = make_list_of_curse_words("curses.txt")
#print(curses)

# function to make a lexicon containing all vocabulary of our dataset + their relative occurences in tweets labeled as
# cyberbullying / no cyberbullying
def make_lexicon_with_occurence(file, column, lex, utterances, filename):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                  # skip header

        lex_size = len(lex)                                                 # size of the lexicon that is needed to apply laplace smoothing
        cyberbuylling_list = make_list_of_column(file, column)              # list of all cyberbullying values

        # write new lexicon that contains the word plus its relative occurence in both classes (cyberbullying & no_cyberbullying)
        file = open(filename, "w")
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

# function to make a lexicon containing all vocabulary of our dataset + their relative occurences in tweets labeled as
# hate speech / no hate speech
def make_lexicon_with_occurence_hs(file, column, lex, utterances, filename):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                  # skip header

        lex_size = len(lex)                                                 # size of the lexicon that is needed to apply laplace smoothing
        hate_speech_list = make_list_of_column(file, column)                # list of all cyberbullying values

        # write new lexicon that contains the word plus its relative occurence in both classes (hate speech & no hate speech)
        file = open(filename, "w")
        for word in lex:
            glob_count = 0
            hs_count = 0
            no_hs_count = 0

            # count how often each word occurs in our dataset
            for utterance in utterances:
                utterance_string = ""
                for item in utterance:
                    utterance_string = utterance_string + " " + item
                glob_count += utterance_string.count(word)

            x = 0
            for value in hate_speech_list:
                sentence = utterances[x]
                sentence_string = ""
                for item in sentence:
                    sentence_string = sentence_string + " " + item

                if value == 1 or value == "1":
                    hs_count += sentence_string.count(word)      # count how often each word occurs in utterances labeled as cyberbullying
                else:
                    no_hs_count += sentence_string.count(word)   # count how often each word occurs in utterances labeled as no_cyberbullying
                x += 1

            #print(word + " " + str(glob_count) + " " + str(cyberbullying_count) + " " + str(no_cyberbullying_count))

            # with Laplace Smoothing
            # We add 1 to all word occurences in the two classes and divide that value by their total occurences plus the size
            # of the lexicon. The result is multiplied by 100 to achieve more practical values.
            occurence_hs = ((hs_count + 1) / (glob_count + lex_size)) * 100
            occurence_no_hs = ((no_hs_count + 1) / (glob_count + lex_size)) * 100

            # the word and its relative occurence in each class is saved into a new lexicon
            line = word + " " + str(round(occurence_hs, 3)) + " " + str(round(occurence_no_hs, 3)) + "\n"
            file.write(line)
        file.close()

# function to make a lexicon containing all vocabulary of our dataset + their relative occurences in tweets labeled as
# s1 / s2 / s3 / s4 / s5
def make_lexicon_with_occurence_cb(file, column, lex, utterances, filename):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                  # skip header

        lex_size = len(lex)                                                 # size of the lexicon that is needed to apply laplace smoothing
        strength_list = make_list_of_column(file, column)              # list of all cyberbullying values

        # write new lexicon that contains the word plus its relative occurence in all strength classes
        file = open(filename, "w")
        for word in lex:
            glob_count = 0
            s1_count = 0
            s2_count = 0
            s3_count = 0
            s4_count = 0
            s5_count = 0

            # count how often each word occurs in our dataset
            for utterance in utterances:
                utterance_string = ""
                for item in utterance:
                    utterance_string = utterance_string + " " + item
                glob_count += utterance_string.count(word)

            x = 0
            for value in strength_list:
                sentence = utterances[x]
                sentence_string = ""
                for item in sentence:
                    sentence_string = sentence_string + " " + item

                if value == 1 or value == "1":
                    s1_count += sentence_string.count(word)                 # count how often each word occurs in utterances labeled as s1
                elif value == 2 or value == "2":
                    s2_count += sentence_string.count(word)                 # count how often each word occurs in utterances labeled as s2
                elif value == 3 or value == "3":
                    s3_count += sentence_string.count(word)                 # count how often each word occurs in utterances labeled as s3
                elif value == 4 or value == "4":
                    s4_count += sentence_string.count(word)                 # count how often each word occurs in utterances labeled as s4
                else:
                    s5_count += sentence_string.count(word)                 # count how often each word occurs in utterances labeled as s5
                x += 1

            # with Laplace Smoothing
            # We add 1 to all word occurences in the two classes and divide that value by their total occurences plus the size
            # of the lexicon. The result is multiplied by 100 to achieve more practical values.
            occurence_s1 = ((s1_count + 1) / (glob_count + lex_size)) * 100
            occurence_s2 = ((s2_count + 1) / (glob_count + lex_size)) * 100
            occurence_s3 = ((s3_count + 1) / (glob_count + lex_size)) * 100
            occurence_s4 = ((s4_count + 1) / (glob_count + lex_size)) * 100
            occurence_s5 = ((s5_count + 1) / (glob_count + lex_size)) * 100

            # the word and its relative occurence in each class is saved into a new lexicon (lexicon_with_occurences.txt)
            line = word + " " + str(round(occurence_s1, 3)) + " " + str(round(occurence_s2, 3)) + " " + str(round(occurence_s3, 3)) + " " + str(round(occurence_s4, 3)) + " " + str(round(occurence_s5, 3)) + "\n"
            file.write(line)
        file.close()

# function to make a lexicon containing all vocabulary of the other datasets + their relative occurences in tweets labeled as
# cyberbullying / no cyberbullying
def make_lexicon_with_occurence_other(file, column, lex, utterances, filename, mode):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                  # skip header

        lex_size = len(lex)                                                 # size of the lexicon that is needed to apply laplace smoothing
        cyberbuylling_list = make_list_of_column(file, column)              # list of all cyberbullying values

        # write new lexicon that contains the word plus its relative occurence in both classes (cyberbullying & no_cyberbullying)
        file = open(filename, "w")
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

                if mode == 2:
                    if value == 1 or value == "1":
                        cyberbullying_count += sentence_string.count(word)      # count how often each word occurs in utterances labeled as cyberbullying
                    elif value == 0 or value == "0":
                        cyberbullying_count += sentence_string.count(word)
                    else:
                        no_cyberbullying_count += sentence_string.count(word)   # count how often each word occurs in utterances labeled as no_cyberbullying
                    x += 1
                else:
                    if value == 1 or value == "1":
                        cyberbullying_count += sentence_string.count(word)      # count how often each word occurs in utterances labeled as cyberbullying
                    elif value == 2 or value == "2":
                        cyberbullying_count += sentence_string.count(word)
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

# function to make a lexicon containing all vocabulary of the other dataset + their relative occurences in tweets labeled as
# hate speech / no hate speech
def make_lexicon_with_occurence_hs_other(file, column, lex, utterances, filename, mode):
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                  # skip header

        lex_size = len(lex)                                                 # size of the lexicon that is needed to apply laplace smoothing
        hate_speech_list = make_list_of_column(file, column)                # list of all cyberbullying values

        # write new lexicon that contains the word plus its relative occurence in both classes (hate speech & no hate speech)
        file = open(filename, "w")
        for word in lex:
            glob_count = 0
            hs_count = 0
            no_hs_count = 0

            # count how often each word occurs in our dataset
            for utterance in utterances:
                utterance_string = ""
                for item in utterance:
                    utterance_string = utterance_string + " " + item
                glob_count += utterance_string.count(word)

            x = 0
            for value in hate_speech_list:
                sentence = utterances[x]
                sentence_string = ""
                for item in sentence:
                    sentence_string = sentence_string + " " + item

                if mode == 2:
                    if value == 0 or value == "0":
                        hs_count += sentence_string.count(word)      # count how often each word occurs in utterances labeled as cyberbullying
                    else:
                        no_hs_count += sentence_string.count(word)   # count how often each word occurs in utterances labeled as no_cyberbullying
                    x += 1
                else:
                    if value == 2 or value == "2":
                        hs_count += sentence_string.count(word)      # count how often each word occurs in utterances labeled as cyberbullying
                    else:
                        no_hs_count += sentence_string.count(word)   # count how often each word occurs in utterances labeled as no_cyberbullying
                    x += 1

            #print(word + " " + str(glob_count) + " " + str(cyberbullying_count) + " " + str(no_cyberbullying_count))

            # with Laplace Smoothing
            # We add 1 to all word occurences in the two classes and divide that value by their total occurences plus the size
            # of the lexicon. The result is multiplied by 100 to achieve more practical values.
            occurence_hs = ((hs_count + 1) / (glob_count + lex_size)) * 100
            occurence_no_hs = ((no_hs_count + 1) / (glob_count + lex_size)) * 100

            # the word and its relative occurence in each class is saved into a new lexicon
            line = word + " " + str(round(occurence_hs, 3)) + " " + str(round(occurence_no_hs, 3)) + "\n"
            file.write(line)
        file.close()

#make_lexicon_with_occurence("twitter_bullying_training.csv", 7, test_lex, test_list, "lexicon_with_occurences.txt")
#make_lexicon_with_occurence("train_set.csv", 7, lex, train_list, "lexicon_with_occurences.txt")
#make_lexicon_with_occurence("train_set.csv", 7, lex2, train_list, "lexicon_with_occurences2.txt")

# hate speech
#make_lexicon_with_occurence_hs("train_set.csv", 9, lex, train_list, "lexicon_with_occurences_hs.txt")

# strength
#make_lexicon_with_occurence_cb("train_cb_set.csv", 8, lex, train_list_cb, "lexicon_with_occurences_cb.txt")

# bullying traces
#make_lexicon_with_occurence("bullying_traces_train.csv", 3, lex_bt, train_list_bt, "lexicon_with_occurences_bt.txt")

# labeled data
#make_lexicon_with_occurence_other("labeled_data_train.csv", 5, lex_ld, train_list_ld, "lexicon_with_occurences_ld.txt", 2)
#make_lexicon_with_occurence_hs_other("labeled_data_train.csv", 5, lex_ld, train_list_ld, "lexicon_with_occurences_hs_ld.txt", 2)

# twitter bullying
#make_lexicon_with_occurence_other("twitter_hate_speech_train.csv", 2, lex_ths, train_list_ths, "lexicon_with_occurences_ths.txt", 3)
#make_lexicon_with_occurence_hs_other("twitter_hate_speech_train.csv", 2, lex_ths, train_list_ths, "lexicon_with_occurences_hs_ths.txt", 3)


