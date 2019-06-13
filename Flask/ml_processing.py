import csv
import nltk
import re
from nltk.tokenize import word_tokenize

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

# function to further process the trainset
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

    This function will return a list of lists containing all stemmed words of every tweet from the trainset (data_list)
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

# function to process a chat message
def process_utterance(utterance):
    """
    Before we can label the chat message, we need to process it.
    This includes:
        - converting all words to lowercase
        - deleting punctuation marks
        - deleting numbers
        - tokenize tweets to get a list of words
        - deleting stopwords or not deleting stopwords depending on the results
        - stem all words

    This function will return the processed chat message.
    """
    print(utterance)
    punctuation_numbers = r'[^a-zA-Z ]'

    stopwords = nltk.corpus.stopwords.words("english")                      # list of english stopwords

    utterance = utterance.lower()                                           # utterance to lowercase

    non_alpha = re.findall(punctuation_numbers, utterance)
    print(non_alpha)

    for x in non_alpha:
        utterance = utterance.replace(x, '')                             # delete punctuation marks
    utterance = word_tokenize(utterance)                                    # tokenize utterance
    utterance = [w for w in utterance if w not in stopwords]                # delete stopwords (depending on results we may not remvove stopwords)

    for i, word in enumerate(utterance):                                    # stem words in utterance
        word = nltk.SnowballStemmer("english").stem(word)
        utterance[i] = str(word)

    print(utterance)
    return utterance