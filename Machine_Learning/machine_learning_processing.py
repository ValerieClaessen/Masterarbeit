import csv
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

# function to further process the datasets
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
    punctuation = ['.', ',', ';', '!', '?', '(', ')', '[', ']',             # list of english punctuation marks (used in utterances)
                   '&', ':', '-', '/', '\\', '$', '*', '"', "'", '+',
                   '=', '@', '%', '~', '{', '}', '|', '<', '>', '`', '']
    stopwords = nltk.corpus.stopwords.words("english")                      # list of english stopwords

    with open(file, 'r') as csvfile:                                        # collect tweets from csv-data in list
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)                                                  # skip header
        for row in reader:
            data_list.append(row[5])

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

#train_list = process_data("twitter_bullying_training.csv")
#print(test_list)
#train_list = process_data("train_set.csv")

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

#test_lex = make_lexicon(test_list)
#print(test_lex)
#lex = make_lexicon(train_list)

# function to save lexicon in a txt file
def lex_into_txt(lex):
    with open("lexicon.txt", 'w') as f:
        for word in lex:
            f.write("%s\n" % word)

#lex_into_txt(test_lex)
#lex_into_txt(lex)

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

#make_lexicon_with_occurence("twitter_bullying_training.csv", 7, test_lex, test_list)
#make_lexicon_with_occurence("/machinelearning/train_set.csv", 7, lex, train_list)