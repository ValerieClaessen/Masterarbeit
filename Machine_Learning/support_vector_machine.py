import csv
import machine_learning_processing
import estimation
import senti_strength
import math
import numpy as np

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
        #print(vec_utterance)
        term_utterance_matrix.append(vec_utterance)             # append vector to the list of vectors

    return term_utterance_matrix

# function to use the support vector machine algorithm on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_svm(data_list, lex, test_utterance, file, column, matrix):
    """
    We use the Support Vector Machine (with k-nearest neighbour) algorithm to determine the class of each tweet.
    We work with our data_list containing all stemmed and processed utterances and our lexicon without occurence probabilities.

    First we need to estimate the vectors for each utterance of the training set.
    The values of the vector are the number of times each word of our lexicon appears in our utterance.
    Then we compare for each utterance its vector with all other vectors to find the ones most similar.
    To do this, we need to estimate the normalized dot product.

    The class of our tweet is estimated by the (intellectually assigned) class of the k tweets with the most similar vector
    (k=3 or k=5, whichever gets the better results).
    """

    # make vector from the utterance of the test set
    vec_test_utterance = []                                     # vector of the utterance from the test_set
    for line in open(lex):
        line_split = line.split()
        n = 0
        m = 0
        if line_split[0] in test_utterance:
            #print(line_split[0])
            while m < len(test_utterance):
                if line_split[0] == test_utterance[m]:
                    n += 1                                      # count how often the word appears in the utterance
                    m += 1                                      # loop through the words of the utterance
                else:
                    m += 1
        vec_test_utterance.append(n)
    #print(vec_test_utterance)

    distances = []                                              # array of distances to each vector of the training set
    np_vec = np.array(vec_test_utterance)
    vec_len = np.linalg.norm(np_vec)                            # length of test_vector
    #print(vec_len)

    for vector in matrix:                                    # loop through all vectors from the training set
        np_vec2 = np.array(vector)
        vec2_len = np.linalg.norm(np_vec2)                                  # length of vector from training set

        # estimate normalized dot product between the test vector and all vectors from the training set to calculate the distance
        dot_product_first = 0
        i = 0
        while i < len(vec_test_utterance):
            dot_product_first = dot_product_first + vec_test_utterance[i] * vector[i]
            i += 1
        if vec_len != 0 and vec2_len != 0:
            dot_product = dot_product_first / (vec_len * vec2_len)          # normalized dot product
        else:
            dot_product = 0
        distances.append(dot_product)                                       # save all dot products into the list

    # find the 3 or 5 most similar vectors for our test vector
    k1 = distances.index(max(distances))
    k1_distance = max(distances)
    distances[k1] = 0                                                       # set dot product to 0 to determine the next best vector
    k2 = distances.index(max(distances))
    k2_distance = max(distances)
    distances[k2] = 0
    k3 = distances.index(max(distances))
    k3_distance = max(distances)
    distances[k3] = 0                                                       # if k=5 is used instead of k=3
    k4 = distances.index(max(distances))
    k4_distance = max(distances)
    distances[k4] = 0
    k5 = distances.index(max(distances))
    k5_distance = max(distances)
    distances[k5] = 0

    u1 = ""                                                                 # utterances to which the dot products belong
    u2 = ""
    u3 = ""
    u4 = ""                                                                 # if k=5 is used instead of k=3
    u5 = ""

    u1 = data_list[k1]
    u2 = data_list[k2]
    u3 = data_list[k3]
    u4 = data_list[k4]                                                      # if k=5 is used instead of k=3
    u5 = data_list[k5]

    #print(k1, k1_distance, u1)
    #print(k2, k2_distance, u2)
    #print(k3, k3_distance, u3)
    #print(k4, k4_distance, u4)
    #print(k5, k5_distance, u5)

    # find the classes of the utterances corresponding to the most similar vectors
    classes = []
    cb_list = machine_learning_processing.make_list_of_column(file, column)
    classes.append(cb_list[k1])
    classes.append(cb_list[k2])
    classes.append(cb_list[k3])
    classes.append(cb_list[k4])
    classes.append(cb_list[k5])
    #print(classes)

    cb = classes.count("1")                                     # number of most similiar utterances with the class cyberbulling
    no_cb = classes.count("0")                                  # number of most similiar utterances with the class no_cyberbulling
    cb_class = ""                                               # determine class of the test_utterance
    #if cb == max([cb, no_cb]):
    #    cb_class = 1
    #else:
    #    cb_class = 0
    #print(cb_class)

    contains_curses = False
    curses = machine_learning_processing.make_list_of_curse_words("curses.txt")

    for word in test_utterance:
        if word in curses:
            contains_curses = True                              # utterances that contain curses will automatically be labeled as cyberbullying later

    if cb >= 2:
        cb_class = 1
    elif contains_curses == True:                                                               # utterances that contain curses will automatically be labeled as cyberbullying
        cb_class = 1
    else:
        cb_class = 0

    return cb_class

# function to use the support vector machine algorithm on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_svm_strength(data_list, lex, test_utterance, file, column, matrix):
    """
    We use the Support Vector Machine (with k-nearest neighbour) algorithm to determine the class of each tweet.
    We work with our data_list containing all stemmed and processed utterances and our lexicon without occurence probabilities.

    First we need to estimate the vectors for each utterance of the training set.
    The values of the vector are the number of times each word of our lexicon appears in our utterance.
    Then we compare for each utterance its vector with all other vectors to find the ones most similar.
    To do this, we need to estimate the normalized dot product.

    The class of our tweet is estimated by the (intellectually assigned) class of the k tweets with the most similar vector
    (k=3 or k=5, whichever gets the better results).
    """

    # make vector from the utterance of the test set
    vec_test_utterance = []                                     # vector of the utterance from the test_set
    for line in open(lex):
        line_split = line.split()
        n = 0
        m = 0
        if line_split[0] in test_utterance:
            #print(line_split[0])
            while m < len(test_utterance):
                if line_split[0] == test_utterance[m]:
                    n += 1                                      # count how often the word appears in the utterance
                    m += 1                                      # loop through the words of the utterance
                else:
                    m += 1
        vec_test_utterance.append(n)
    #print(vec_test_utterance)

    distances = []                                              # array of distances to each vector of the training set
    np_vec = np.array(vec_test_utterance)
    vec_len = np.linalg.norm(np_vec)                            # length of test_vector
    #print(vec_len)

    for vector in matrix:                                    # loop through all vectors from the training set
        np_vec2 = np.array(vector)
        vec2_len = np.linalg.norm(np_vec2)                                  # length of vector from training set

        # estimate normalized dot product between the test vector and all vectors from the training set to calculate the distance
        dot_product_first = 0
        i = 0
        while i < len(vec_test_utterance):
            dot_product_first = dot_product_first + vec_test_utterance[i] * vector[i]
            i += 1
        if vec_len != 0 and vec2_len != 0:
            dot_product = dot_product_first / (vec_len * vec2_len)          # normalized dot product
        else:
            dot_product = 0
        distances.append(dot_product)                                       # save all dot products into the list

    # find the 3 or 5 most similar vectors for our test vector
    k1 = distances.index(max(distances))
    k1_distance = max(distances)
    distances[k1] = 0                                                       # set dot product to 0 to determine the next best vector
    k2 = distances.index(max(distances))
    k2_distance = max(distances)
    distances[k2] = 0
    k3 = distances.index(max(distances))
    k3_distance = max(distances)
    distances[k3] = 0                                                       # if k=5 is used instead of k=3
    k4 = distances.index(max(distances))
    k4_distance = max(distances)
    distances[k4] = 0
    k5 = distances.index(max(distances))
    k5_distance = max(distances)
    distances[k5] = 0

    u1 = ""                                                                 # utterances to which the dot products belong
    u2 = ""
    u3 = ""
    u4 = ""                                                                 # if k=5 is used instead of k=3
    u5 = ""

    u1 = data_list[k1]
    u2 = data_list[k2]
    u3 = data_list[k3]
    u4 = data_list[k4]                                                      # if k=5 is used instead of k=3
    u5 = data_list[k5]

    #print(k1, k1_distance, u1)
    #print(k2, k2_distance, u2)
    #print(k3, k3_distance, u3)
    #print(k4, k4_distance, u4)
    #print(k5, k5_distance, u5)

    # find the classes of the utterances corresponding to the most similar vectors
    classes = []
    cb_list = machine_learning_processing.make_list_of_column(file, column)
    classes.append(cb_list[k1])
    classes.append(cb_list[k2])
    classes.append(cb_list[k3])
    classes.append(cb_list[k4])
    classes.append(cb_list[k5])
    #print(classes)

    s1 = classes.count("1")                                     # number of most similiar utterances with the class s1
    s2 = classes.count("2")                                     # number of most similiar utterances with the class s2
    s3 = classes.count("3")                                     # number of most similiar utterances with the class s3
    s4 = classes.count("4")                                     # number of most similiar utterances with the class s4
    s5 = classes.count("5")                                     # number of most similiar utterances with the class s5
    values = [s1,s2,s3,s4,s5]
    strength_class = ""                                         # determine class of the test_utterance

    if max(values) == values[0]:                                # determine class (max P(class|tweet))
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

# function to use the support vector machine algorithm on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_svm_other(data_list, lex, test_utterance, file, column, matrix, mode):
    """
    We use the Support Vector Machine (with k-nearest neighbour) algorithm to determine the class of each tweet.
    We work with our data_list containing all stemmed and processed utterances and our lexicon without occurence probabilities.

    First we need to estimate the vectors for each utterance of the training set.
    The values of the vector are the number of times each word of our lexicon appears in our utterance.
    Then we compare for each utterance its vector with all other vectors to find the ones most similar.
    To do this, we need to estimate the normalized dot product.

    The class of our tweet is estimated by the (intellectually assigned) class of the k tweets with the most similar vector
    (k=3 or k=5, whichever gets the better results).
    """

    # make vector from the utterance of the test set
    vec_test_utterance = []                                     # vector of the utterance from the test_set
    for line in open(lex):
        line_split = line.split()
        n = 0
        m = 0
        if line_split[0] in test_utterance:
            #print(line_split[0])
            while m < len(test_utterance):
                if line_split[0] == test_utterance[m]:
                    n += 1                                      # count how often the word appears in the utterance
                    m += 1                                      # loop through the words of the utterance
                else:
                    m += 1
        vec_test_utterance.append(n)
    #print(vec_test_utterance)

    distances = []                                              # array of distances to each vector of the training set
    np_vec = np.array(vec_test_utterance)
    vec_len = np.linalg.norm(np_vec)                            # length of test_vector
    #print(vec_len)

    for vector in matrix:                                    # loop through all vectors from the training set
        np_vec2 = np.array(vector)
        vec2_len = np.linalg.norm(np_vec2)                                  # length of vector from training set

        # estimate normalized dot product between the test vector and all vectors from the training set to calculate the distance
        dot_product_first = 0
        i = 0
        while i < len(vec_test_utterance):
            dot_product_first = dot_product_first + vec_test_utterance[i] * vector[i]
            i += 1
        if vec_len != 0 and vec2_len != 0:
            dot_product = dot_product_first / (vec_len * vec2_len)          # normalized dot product
        else:
            dot_product = 0
        distances.append(dot_product)                                       # save all dot products into the list

    # find the 3 or 5 most similar vectors for our test vector
    k1 = distances.index(max(distances))
    k1_distance = max(distances)
    distances[k1] = 0                                                       # set dot product to 0 to determine the next best vector
    k2 = distances.index(max(distances))
    k2_distance = max(distances)
    distances[k2] = 0
    k3 = distances.index(max(distances))
    k3_distance = max(distances)
    distances[k3] = 0                                                       # if k=5 is used instead of k=3
    k4 = distances.index(max(distances))
    k4_distance = max(distances)
    distances[k4] = 0
    k5 = distances.index(max(distances))
    k5_distance = max(distances)
    distances[k5] = 0

    u1 = ""                                                                 # utterances to which the dot products belong
    u2 = ""
    u3 = ""
    u4 = ""                                                                 # if k=5 is used instead of k=3
    u5 = ""

    u1 = data_list[k1]
    u2 = data_list[k2]
    u3 = data_list[k3]
    u4 = data_list[k4]                                                      # if k=5 is used instead of k=3
    u5 = data_list[k5]

    #print(k1, k1_distance, u1)
    #print(k2, k2_distance, u2)
    #print(k3, k3_distance, u3)
    #print(k4, k4_distance, u4)
    #print(k5, k5_distance, u5)

    # find the classes of the utterances corresponding to the most similar vectors
    classes = []
    cb_list = machine_learning_processing.make_list_of_column(file, column)
    classes.append(cb_list[k1])
    classes.append(cb_list[k2])
    classes.append(cb_list[k3])
    classes.append(cb_list[k4])
    classes.append(cb_list[k5])
    #print(classes)

    if mode == 2:
        cb = classes.count("1") + classes.count("0")                            # number of most similiar utterances with the class cyberbulling
        no_cb = classes.count("2")                                              # number of most similiar utterances with the class no_cyberbulling
    else:
        cb = classes.count("1") + classes.count("2")
        no_cb = classes.count("0")

    cb_class = ""                                               # determine class of the test_utterance
    #if cb == max([cb, no_cb]):
    #    cb_class = 1
    #else:
    #    cb_class = 0
    #print(cb_class)

    contains_curses = False
    curses = machine_learning_processing.make_list_of_curse_words("curses.txt")

    for word in test_utterance:
        if word in curses:
            contains_curses = True                              # utterances that contain curses will automatically be labeled as cyberbullying later

    if cb >= 3:
        cb_class = 1
    elif contains_curses == True:                                                               # utterances that contain curses will automatically be labeled as cyberbullying
        cb_class = 1
    else:
        cb_class = 0

    return cb_class

# function to use the support vector machine algorithm on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_svm_other_hs(data_list, lex, test_utterance, file, column, matrix, mode):
    """
    We use the Support Vector Machine (with k-nearest neighbour) algorithm to determine the class of each tweet.
    We work with our data_list containing all stemmed and processed utterances and our lexicon without occurence probabilities.

    First we need to estimate the vectors for each utterance of the training set.
    The values of the vector are the number of times each word of our lexicon appears in our utterance.
    Then we compare for each utterance its vector with all other vectors to find the ones most similar.
    To do this, we need to estimate the normalized dot product.

    The class of our tweet is estimated by the (intellectually assigned) class of the k tweets with the most similar vector
    (k=3 or k=5, whichever gets the better results).
    """

    # make vector from the utterance of the test set
    vec_test_utterance = []                                     # vector of the utterance from the test_set
    for line in open(lex):
        line_split = line.split()
        n = 0
        m = 0
        if line_split[0] in test_utterance:
            #print(line_split[0])
            while m < len(test_utterance):
                if line_split[0] == test_utterance[m]:
                    n += 1                                      # count how often the word appears in the utterance
                    m += 1                                      # loop through the words of the utterance
                else:
                    m += 1
        vec_test_utterance.append(n)
    #print(vec_test_utterance)

    distances = []                                              # array of distances to each vector of the training set
    np_vec = np.array(vec_test_utterance)
    vec_len = np.linalg.norm(np_vec)                            # length of test_vector
    #print(vec_len)

    for vector in matrix:                                    # loop through all vectors from the training set
        np_vec2 = np.array(vector)
        vec2_len = np.linalg.norm(np_vec2)                                  # length of vector from training set

        # estimate normalized dot product between the test vector and all vectors from the training set to calculate the distance
        dot_product_first = 0
        i = 0
        while i < len(vec_test_utterance):
            dot_product_first = dot_product_first + vec_test_utterance[i] * vector[i]
            i += 1
        if vec_len != 0 and vec2_len != 0:
            dot_product = dot_product_first / (vec_len * vec2_len)          # normalized dot product
        else:
            dot_product = 0
        distances.append(dot_product)                                       # save all dot products into the list

    # find the 3 or 5 most similar vectors for our test vector
    k1 = distances.index(max(distances))
    k1_distance = max(distances)
    distances[k1] = 0                                                       # set dot product to 0 to determine the next best vector
    k2 = distances.index(max(distances))
    k2_distance = max(distances)
    distances[k2] = 0
    k3 = distances.index(max(distances))
    k3_distance = max(distances)
    distances[k3] = 0                                                       # if k=5 is used instead of k=3
    k4 = distances.index(max(distances))
    k4_distance = max(distances)
    distances[k4] = 0
    k5 = distances.index(max(distances))
    k5_distance = max(distances)
    distances[k5] = 0

    u1 = ""                                                                 # utterances to which the dot products belong
    u2 = ""
    u3 = ""
    u4 = ""                                                                 # if k=5 is used instead of k=3
    u5 = ""

    u1 = data_list[k1]
    u2 = data_list[k2]
    u3 = data_list[k3]
    u4 = data_list[k4]                                                      # if k=5 is used instead of k=3
    u5 = data_list[k5]

    #print(k1, k1_distance, u1)
    #print(k2, k2_distance, u2)
    #print(k3, k3_distance, u3)
    #print(k4, k4_distance, u4)
    #print(k5, k5_distance, u5)

    # find the classes of the utterances corresponding to the most similar vectors
    classes = []
    cb_list = machine_learning_processing.make_list_of_column(file, column)
    classes.append(cb_list[k1])
    classes.append(cb_list[k2])
    classes.append(cb_list[k3])
    classes.append(cb_list[k4])
    classes.append(cb_list[k5])
    #print(classes)

    if mode == 2:
        cb = classes.count("0")                                         # number of most similiar utterances with the class cyberbulling
        no_cb = classes.count("2") + classes.count("1")                 # number of most similiar utterances with the class no_cyberbulling
    else:
        cb = classes.count("2")
        no_cb = classes.count("0") + classes.count("1")

    cb_class = ""                                               # determine class of the test_utterance
    #if cb == max([cb, no_cb]):
    #    cb_class = 1
    #else:
    #    cb_class = 0
    #print(cb_class)

    contains_curses = False
    curses = machine_learning_processing.make_list_of_curse_words("curses.txt")

    for word in test_utterance:
        if word in curses:
            contains_curses = True                              # utterances that contain curses will automatically be labeled as cyberbullying later

    if cb >= 2:
        cb_class = 1
    elif contains_curses == True:                                                               # utterances that contain curses will automatically be labeled as cyberbullying
        cb_class = 1
    else:
        cb_class = 0

    return cb_class

# function to label a test set using the Support Vector Machine algorithm and to save results in a new file
def do_test_set_svm(utterances_test, utterances_training, filename, lex, file, column, matrix, columnname):
    # annotation using svm will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", columnname])  # header

        x = 0
        for utterance in utterances_test:
            class_cb = do_svm(utterances_training, lex, utterance, file, column, matrix)        # determine class of the utterance using do_svm()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_cb])
            x += 1

            if x == 500:
                print(x)
            #print(x, class_cb)                                                                # count of utterances already labeled

# function to label a test set using the Support Vector Machine algorithm and to save results in a new file
def do_test_set_svm_sent(utterances_test, utterances_training, filename, lex_pos, lex_neut, lex_neg, file, column, matrix_pos, matrix_neut, matrix_neg, sentimentfile, columnname):
    # annotation using svm will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", columnname])  # header

        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile, 1)

        utterance_id = 0
        for utterance in utterances_test:
            # use lexicon with positive, neutral or negative vocabulary based on the sentiment of the utterance
            if list_of_sentiments[utterance_id] == 1 or list_of_sentiments[utterance_id] == "1":
                class_cb = do_svm(utterances_training, lex_pos, utterance, file, column, matrix_pos)                        # determine class of the utterance using do_svm()
            elif list_of_sentiments[utterance_id] == 0 or list_of_sentiments[utterance_id] == "0":
                class_cb = do_svm(utterances_training, lex_neut, utterance, file, column, matrix_neut)
            else:
                class_cb = do_svm(utterances_training, lex_neg, utterance, file, column, matrix_neg)

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_cb])
            utterance_id += 1

            if utterance_id == 100:
                print(utterance_id)
            elif utterance_id == 200:
                print(utterance_id)
            elif utterance_id == 300:
                print(utterance_id)
            elif utterance_id == 400:
                print(utterance_id)
            elif utterance_id == 500:
                print(utterance_id)
            elif utterance_id == 600:
                print(utterance_id)
            elif utterance_id == 700:
                print(utterance_id)
            elif utterance_id == 800:
                print(utterance_id)
            elif utterance_id == 900:
                print(utterance_id)
            # print(x, class_cb)                                                                # count of utterances already labeled

# function to label a test set using the Support Vector Machine algorithm and to save results in a new file
def do_test_set_svm_strength(utterances_test, utterances_training, filename, lex, file, column, matrix):
    # annotation using svm will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying Strength"])  # header

        x = 0
        for utterance in utterances_test:
            class_strength = do_svm_strength(utterances_training, lex, utterance, file, column, matrix)        # determine class of the utterance using do_svm_strength()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_strength])
            x += 1

            if x == 500:
                print(x)
            #print(x, class_cb)                                                                # count of utterances already labeled

# function to label a test set using the Support Vector Machine algorithm and to save results in a new file
def do_test_set_svm_sent_strength(utterances_test, utterances_training, filename, lex_pos, lex_neut, lex_neg, file, column, matrix_pos, matrix_neut, matrix_neg, sentimentfile):
    # annotation using svm will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying Strength"])  # header

        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile, 1)

        utterance_id = 0
        for utterance in utterances_test:
            # use lexicon with positive, neutral or negative vocabulary based on the sentiment of the utterance
            if list_of_sentiments[utterance_id] == 1 or list_of_sentiments[utterance_id] == "1":
                class_strength = do_svm_strength(utterances_training, lex_pos, utterance, file, column, matrix_pos)                        # determine class of the utterance using do_svm()
            elif list_of_sentiments[utterance_id] == 0 or list_of_sentiments[utterance_id] == "0":
                class_strength = do_svm_strength(utterances_training, lex_neut, utterance, file, column, matrix_neut)
            else:
                class_strength = do_svm_strength(utterances_training, lex_neg, utterance, file, column, matrix_neg)

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_strength])
            utterance_id += 1

            if utterance_id == 100:
                print(utterance_id)
            elif utterance_id == 200:
                print(utterance_id)
            elif utterance_id == 300:
                print(utterance_id)
            elif utterance_id == 400:
                print(utterance_id)
            elif utterance_id == 500:
                print(utterance_id)
            elif utterance_id == 600:
                print(utterance_id)
            elif utterance_id == 700:
                print(utterance_id)
            elif utterance_id == 800:
                print(utterance_id)
            elif utterance_id == 900:
                print(utterance_id)
            # print(x, class_cb)                                                                # count of utterances already labeled

# function to label a test set using the Support Vector Machine algorithm and to save results in a new file
def do_test_set_svm_sent_other(utterances_test, utterances_training, filename, lex_pos, lex_neut, lex_neg, file, column, matrix_pos, matrix_neut, matrix_neg, sentimentfile, columnname, mode):
    # annotation using svm will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", columnname])  # header

        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile, 1)

        utterance_id = 0
        for utterance in utterances_test:
            # use lexicon with positive, neutral or negative vocabulary based on the sentiment of the utterance
            if list_of_sentiments[utterance_id] == 1 or list_of_sentiments[utterance_id] == "1":
                class_cb = do_svm_other(utterances_training, lex_pos, utterance, file, column, matrix_pos, mode)                        # determine class of the utterance using do_svm()
            elif list_of_sentiments[utterance_id] == 0 or list_of_sentiments[utterance_id] == "0":
                class_cb = do_svm_other(utterances_training, lex_neut, utterance, file, column, matrix_neut, mode)
            else:
                class_cb = do_svm_other(utterances_training, lex_neg, utterance, file, column, matrix_neg, mode)

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_cb])
            utterance_id += 1

            if utterance_id == 100:
                print(utterance_id)
            elif utterance_id == 200:
                print(utterance_id)
            elif utterance_id == 300:
                print(utterance_id)
            elif utterance_id == 400:
                print(utterance_id)
            elif utterance_id == 500:
                print(utterance_id)
            elif utterance_id == 600:
                print(utterance_id)
            elif utterance_id == 700:
                print(utterance_id)
            elif utterance_id == 800:
                print(utterance_id)
            elif utterance_id == 900:
                print(utterance_id)
            # print(x, class_cb)                                                                # count of utterances already labeled

# function to label a test set using the Support Vector Machine algorithm and to save results in a new file
def do_test_set_svm_sent_other_hs(utterances_test, utterances_training, filename, lex_pos, lex_neut, lex_neg, file, column, matrix_pos, matrix_neut, matrix_neg, sentimentfile, columnname, mode):
    # annotation using svm will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", columnname])  # header

        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile, 1)

        utterance_id = 0
        for utterance in utterances_test:
            # use lexicon with positive, neutral or negative vocabulary based on the sentiment of the utterance
            if list_of_sentiments[utterance_id] == 1 or list_of_sentiments[utterance_id] == "1":
                class_cb = do_svm_other_hs(utterances_training, lex_pos, utterance, file, column, matrix_pos, mode)                        # determine class of the utterance using do_svm()
            elif list_of_sentiments[utterance_id] == 0 or list_of_sentiments[utterance_id] == "0":
                class_cb = do_svm_other_hs(utterances_training, lex_neut, utterance, file, column, matrix_neut, mode)
            else:
                class_cb = do_svm_other_hs(utterances_training, lex_neg, utterance, file, column, matrix_neg, mode)

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_cb])
            utterance_id += 1

            if utterance_id == 100:
                print(utterance_id)
            elif utterance_id == 200:
                print(utterance_id)
            elif utterance_id == 300:
                print(utterance_id)
            elif utterance_id == 400:
                print(utterance_id)
            elif utterance_id == 500:
                print(utterance_id)
            elif utterance_id == 600:
                print(utterance_id)
            elif utterance_id == 700:
                print(utterance_id)
            elif utterance_id == 800:
                print(utterance_id)
            elif utterance_id == 900:
                print(utterance_id)
            # print(x, class_cb)                                                                # count of utterances already labeled

utterance = machine_learning_processing.process_utterance("Yup. I can't stand this shit. The left screams and yells Black Lives Matter and the minute a black man or woman disappear")
utterance2 = machine_learning_processing.process_utterance("ban islam")
utterance3 = machine_learning_processing.process_utterance("This is our president. WHO talks like that?!? Our leader does. I cant. How embarrassing. A disgrace to the office.")

#test_list = machine_learning_processing.process_data("test_set.csv")
#training_list = machine_learning_processing.process_data("train_set.csv")

#term_utterance_matrix = do_matrix(training_list, "lexicon.txt")
#term_utterance_matrix2 = do_matrix(training_list, "lexicon2.txt")
#matrix_pos = do_matrix(training_list, "lexicon_pos.txt")
#matrix_neut = do_matrix(training_list, "lexicon_neut.txt")
#matrix_neg = do_matrix(training_list, "lexicon_neg.txt")
#matrix_pos2 = do_matrix(training_list, "lexicon_pos2.txt")
#matrix_neut2 = do_matrix(training_list, "lexicon_neut2.txt")
#matrix_neg2 = do_matrix(training_list, "lexicon_neg2.txt")

#do_svm(training_list, "lexicon.txt", utterance, "train_set.csv", 7, term_utterance_matrix)
#do_svm(training_list, "lexicon.txt", utterance2, "train_set.csv", 7, term_utterance_matrix)
#do_svm(training_list, "lexicon.txt", utterance3, "train_set.csv", 7, term_utterance_matrix)

#do_test_set_svm(test_list, training_list, "twitter_bullying_svm_k2.csv", "lexicon.txt", "train_set.csv", 7, term_utterance_matrix, "Cyberbullying")
#do_test_set_svm_sent(test_list, training_list, "twitter_bullying_svm_sent.csv", "lexicon_pos.txt", "lexicon_neut.txt", "lexicon_neg.txt", "train_set.csv", 7, matrix_pos, matrix_neut, matrix_neg, "test_set_with_sentiment.csv", "Cyberbullying")

#do_test_set_svm(test_list, training_list, "twitter_bullying_svm_k2_2.csv", "lexicon2.txt", "train_set.csv", 7, term_utterance_matrix2, "Cyberbullying")
#do_test_set_svm_sent(test_list, training_list, "twitter_bullying_svm_sent_2.csv", "lexicon_pos2.txt", "lexicon_neut2.txt", "lexicon_neg2.txt", "train_set.csv", 7, matrix_pos2, matrix_neut2, matrix_neg2, "test_set_with_sentiment.csv")

#do_test_set_svm(test_list, training_list, "twitter_bullying_svm_k2_c.csv", "lexicon.txt", "train_set.csv", 7, term_utterance_matrix, "Cyberbullying")
#do_test_set_svm_sent(test_list, training_list, "twitter_bullying_svm_sent_c.csv", "lexicon_pos.txt", "lexicon_neut.txt", "lexicon_neg.txt", "train_set.csv", 7, matrix_pos, matrix_neut, matrix_neg, "test_set_with_sentiment.csv", "Cyberbullying")

#estimation.test_results("test_set.csv", 7, "twitter_bullying_svm_k2.csv", 1)
#estimation.test_results("test_set.csv", 7, "twitter_bullying_svm_k2_2.csv", 1)
#estimation.test_results("test_set.csv", 7, "twitter_bullying_svm_sent.csv", 1)
#estimation.test_results("test_set.csv", 7, "twitter_bullying_svm_sent_2.csv", 1)

#estimation.test_results("test_set.csv", 7, "twitter_bullying_svm_k2.csv", 1)
#estimation.test_results("test_set.csv", 7, "twitter_bullying_svm_sent.csv", 1)
#estimation.test_results("test_set.csv", 7, "twitter_bullying_svm_k2_c.csv", 1)
#estimation.test_results("test_set.csv", 7, "twitter_bullying_svm_sent_c.csv", 1)

# hate speech
#do_test_set_svm(test_list, training_list, "twitter_bullying_svm_k2_hs.csv", "lexicon.txt", "train_set.csv", 9, term_utterance_matrix, "Hate Speech")
#estimation.test_results("test_set.csv", 9, "twitter_bullying_svm_k2_hs.csv", 1)

# hate speech with sentiment
#do_test_set_svm_sent(test_list, training_list, "twitter_bullying_svm_sent_hs.csv", "lexicon_pos.txt", "lexicon_neut.txt", "lexicon_neg.txt", "train_set.csv", 9, matrix_pos, matrix_neut, matrix_neg, "test_set_with_sentiment.csv", "Hate Speech")
#estimation.test_results("test_set.csv", 9, "twitter_bullying_svm_sent_hs.csv", 1)

# strengths
#test_s_list = machine_learning_processing.process_data("test_cb_set.csv")
#training_s_list = machine_learning_processing.process_data("train_cb_set.csv")
#term_utterance_matrix_s = do_matrix(training_s_list, "lexicon_cb.txt")
#do_test_set_svm_strength(test_s_list, training_s_list, "twitter_bullying_svm_k2_strength.csv", "lexicon_cb.txt", "train_cb_set.csv", 8, term_utterance_matrix_s)
#estimation.test_results_strengths("test_cb_set.csv", 8, "twitter_bullying_svm_k2_strength.csv", 1)

# strengths with sentiment
#matrix_pos_s = do_matrix(training_s_list, "lexicon_pos_cb.txt")
#matrix_neut_s = do_matrix(training_s_list, "lexicon_neut_cb.txt")
#matrix_neg_s = do_matrix(training_s_list, "lexicon_neg_cb.txt")
#do_test_set_svm_sent_strength(test_s_list, training_s_list, "twitter_bullying_svm_sent_strength.csv", "lexicon_pos_cb.txt", "lexicon_neut_cb.txt", "lexicon_neg_cb.txt", "train_cb_set.csv", 8, matrix_pos_s, matrix_neut_s, matrix_neg_s, "test_cb_set_with_sentiment.csv")
#estimation.test_results_strengths("test_cb_set.csv", 8, "twitter_bullying_svm_sent_strength.csv", 1)

# bullying traces
#test_list_bt = machine_learning_processing.process_data("bullying_traces_test.csv", 2)
#training_list_bt = machine_learning_processing.process_data("bullying_traces_test.csv", 2)
#term_utterance_matrix_bt = do_matrix(training_list_bt, "lexicon_bt.txt")
#matrix_pos_bt = do_matrix(training_list_bt, "lexicon_pos_bt.txt")
#matrix_neut_bt = do_matrix(training_list_bt, "lexicon_neut_bt.txt")
#matrix_neg_bt = do_matrix(training_list_bt, "lexicon_neg_bt.txt")
#do_test_set_svm_sent(test_list_bt, training_list_bt, "bullying_traces_svm.csv", "lexicon_pos_bt.txt", "lexicon_neut_bt.txt", "lexicon_neg_bt.txt", "bullying_traces_train.csv", 3, matrix_pos_bt, matrix_neut_bt, matrix_neg_bt, "bullying_traces_test_with_sentiment.csv", "Cyberbullying")
#estimation.test_results("bullying_traces_test.csv", 3, "bullying_traces_svm.csv", 1)

# labeled data
test_list_ld = machine_learning_processing.process_data("labeled_data_test.csv", 6)
training_list_ld = machine_learning_processing.process_data("labeled_data_test.csv", 6)
term_utterance_matrix_ld = do_matrix(training_list_ld, "lexicon_ld.txt")
matrix_pos_ld = do_matrix(training_list_ld, "lexicon_pos_ld.txt")
matrix_neut_ld = do_matrix(training_list_ld, "lexicon_neut_ld.txt")
matrix_neg_ld = do_matrix(training_list_ld, "lexicon_neg_ld.txt")
do_test_set_svm_sent_other(test_list_ld, training_list_ld, "labeled_data_svm.csv", "lexicon_pos_ld.txt", "lexicon_neut_ld.txt", "lexicon_neg_ld.txt", "labeled_data_train.csv", 5, matrix_pos_ld, matrix_neut_ld, matrix_neg_ld, "labeled_data_test_with_sentiment.csv", "Cyberbullying", 2)
do_test_set_svm_sent_other_hs(test_list_ld, training_list_ld, "labeled_data_svm_hs.csv", "lexicon_pos_ld.txt", "lexicon_neut_ld.txt", "lexicon_neg_ld.txt", "labeled_data_train.csv", 5, matrix_pos_ld, matrix_neut_ld, matrix_neg_ld, "labeled_data_test_with_sentiment.csv", "Hate Speech", 2)
estimation.test_results("labeled_data_test.csv", 5, "labeled_data_svm.csv", 1)
estimation.test_results("labeled_data_test.csv", 5, "labeled_data_svm_hs.csv", 1)

# twitter hate speech
test_list_ths = machine_learning_processing.process_data("twitter_hate_speech_test.csv", 1)
training_list_ths = machine_learning_processing.process_data("twitter_hate_speech_test.csv", 1)
term_utterance_matrix_ths = do_matrix(training_list_ths, "lexicon_ths.txt")
matrix_pos_ths = do_matrix(training_list_ths, "lexicon_pos_ths.txt")
matrix_neut_ths = do_matrix(training_list_ths, "lexicon_neut_ths.txt")
matrix_neg_ths = do_matrix(training_list_ths, "lexicon_neg_ths.txt")
do_test_set_svm_sent_other(test_list_ths, training_list_ths, "twitter_hate_speech_svm.csv", "lexicon_pos_ths.txt", "lexicon_neut_ths.txt", "lexicon_neg_ths.txt", "twitter_hate_speech_train.csv", 2, matrix_pos_ths, matrix_neut_ths, matrix_neg_ths, "twitter_hate_speech_test_with_sentiment.csv", "Cyberbullying", 3)
do_test_set_svm_sent_other_hs(test_list_ths, training_list_ths, "twitter_hate_speech_svm_hs.csv", "lexicon_pos_ths.txt", "lexicon_neut_ths.txt", "lexicon_neg_ths.txt", "twitter_hate_speech_train.csv", 2, matrix_pos_ths, matrix_neut_ths, matrix_neg_ths, "twitter_hate_speech_test_with_sentiment.csv", "Hate Speech", 3)
estimation.test_results("twitter_hate_speech_test.csv", 2, "twitter_hate_speech_svm.csv", 1)
estimation.test_results("twitter_hate_speech_test.csv", 2, "twitter_hate_speech_svm_hs.csv", 1)



