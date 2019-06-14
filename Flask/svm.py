import ml_processing
import numpy as np
import pickle

# this method should be called as soon as the chat is loaded to avoid creating the matrix over and over again (time-consuming)
def do_matrix(data_list, lex):
    # create a list of lists (term_utterance_matrix) representing the vectors of each utterance
    term_utterance_matrix = []
    for utterance in data_list:
        vec_utterance = []                                      # vector of the utterance
        for line in open(lex):
            line_split = line.split()
            n = 0
            m = 0
            if line_split[0] in utterance:
                while m < len(utterance):
                    if line_split[0] == utterance[m]:
                        n += 1                                  # count how often the word appears in the utterance
                        m += 1                                  # loop through the words of the utterance
                    else:
                        m += 1
            vec_utterance.append(n)
        term_utterance_matrix.append(vec_utterance)             # append vector to the list of vectors

    return term_utterance_matrix

# function to use the support vector machine algorithm on a chat message that is to be sent
# returns the class for the utterances assigned by the algorithm
def do_svm(data_list, lex, test_utterance, file, column, matrix):
    """
    We use the Support Vector Machine (with k-nearest neighbour) algorithm to determine the class of each chat message.
    We work with our data_list containing all stemmed and processed utterances and our lexicon without occurence probabilities.

    First we need to estimate the vectors for each utterance of the training set.
    The values of the vector are the number of times each word of our lexicon appears in our utterance.
    Then we compare for each utterance its vector with all other vectors to find the ones most similar.
    To do this, we need to estimate the normalized dot product.

    The class of our tweet is estimated by the (intellectually assigned) class of the k tweets with the most similar vector
    (k=5, which got the better results).
    """

    # make vector from chat message
    vec_test_utterance = []                                     # vector of the chat message
    for line in open(lex):
        line_split = line.split()
        n = 0
        m = 0
        if line_split[0] in test_utterance:
            while m < len(test_utterance):
                if line_split[0] == test_utterance[m]:
                    n += 1                                      # count how often the word appears in the chat message
                    m += 1                                      # loop through the words of the chat message
                else:
                    m += 1
        vec_test_utterance.append(n)

    distances = []                                              # array of distances to each vector of the training set
    np_vec = np.array(vec_test_utterance)
    vec_len = np.linalg.norm(np_vec)                            # length of test_vector

    for vector in matrix:                                       # loop through all vectors from the training set
        np_vec2 = np.array(vector)
        vec2_len = np.linalg.norm(np_vec2)                      # length of vector from training set

        # estimate normalized dot product between the chat vector and all vectors from the training set to calculate the distance
        dot_product_first = 0
        i = 0
        while i < len(vec_test_utterance):
            dot_product_first = dot_product_first + vec_test_utterance[i] * vector[i]
            i += 1
        if vec_len != 0 and vec2_len != 0:
            dot_product = dot_product_first / (vec_len * vec2_len)      # normalized dot product
        else:
            dot_product = 0
        distances.append(dot_product)                                   # save all dot products into the list

    # find the 3 or 5 most similar vectors for our chat vector
    k1 = distances.index(max(distances))
    k1_distance = max(distances)
    distances[k1] = 0                                                   # set dot product to 0 to determine the next best vector
    k2 = distances.index(max(distances))
    k2_distance = max(distances)
    distances[k2] = 0
    k3 = distances.index(max(distances))
    k3_distance = max(distances)
    distances[k3] = 0
    k4 = distances.index(max(distances))
    k4_distance = max(distances)
    distances[k4] = 0
    k5 = distances.index(max(distances))
    k5_distance = max(distances)
    distances[k5] = 0

    u1 = ""                                                             # utterances to which the dot products belong
    u2 = ""
    u3 = ""
    u4 = ""
    u5 = ""

    u1 = data_list[k1]
    u2 = data_list[k2]
    u3 = data_list[k3]
    u4 = data_list[k4]
    u5 = data_list[k5]

    # find the classes of the utterances corresponding to the most similar vectors
    classes = []
    cb_list = ml_processing.make_list_of_column(file, column)
    classes.append(cb_list[k1])
    classes.append(cb_list[k2])
    classes.append(cb_list[k3])
    classes.append(cb_list[k4])
    classes.append(cb_list[k5])

    cb = classes.count("1")                                     # number of most similiar utterances with the class cyberbulling
    cb_class = ""                                               # determine class of the test_utterance

    contains_curses = False
    curses = pickle.load(open("curses.p", "rb"))

    for word in test_utterance:
        if word in curses:
            contains_curses = True              # messages that contain curses will automatically be labeled as cyberbullying later

    if cb >= 2:
        cb_class = 1
    elif contains_curses is True:               # messages that contain curses will automatically be labeled as cyberbullying
        cb_class = 1
    else:
        cb_class = 0

    return cb_class
