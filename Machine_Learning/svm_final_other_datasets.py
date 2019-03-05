import csv
import machine_learning_processing
import estimation
import numpy as np
import support_vector_machine
import compare_labeled_data
import compare_twitter_bullying

# function to use the support vector machine algorithm on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_svm_sent_pos_ld(data_list, utterance_unprocessed, lex, test_utterance, file, column, matrix, mode):
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

    distances = []                                              # array of distances to each vector of the training set
    np_vec = np.array(vec_test_utterance)
    vec_len = np.linalg.norm(np_vec)                            # length of test_vector

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

    # find the classes of the utterances corresponding to the most similar vectors
    classes = []
    cb_list = machine_learning_processing.make_list_of_column(file, column)
    classes.append(cb_list[k1])
    classes.append(cb_list[k2])
    classes.append(cb_list[k3])
    classes.append(cb_list[k4])
    classes.append(cb_list[k5])

    if mode == 2:
        cb = classes.count("1") + classes.count("0")                            # number of most similiar utterances with the class cyberbulling
        no_cb = classes.count("2")                                              # number of most similiar utterances with the class no_cyberbulling
    else:
        cb = classes.count("1") + classes.count("2")
        no_cb = classes.count("0")

    cb_class = ""                                               # determine class of the test_utterance

    # probability that utterance is in class cyberbullying / no cyberbullying based on pos-tagging
    cb_pos_prob = compare_labeled_data.compare_vec_labeled_data_cb(utterance_unprocessed, 3)
    no_cb_pos_prob = 1 - cb_pos_prob

    cb = cb * cb_pos_prob
    no_cb = no_cb * no_cb_pos_prob

    contains_curses = False
    curses = machine_learning_processing.make_list_of_curse_words("curses.txt")

    for word in test_utterance:
        if word in curses:
            contains_curses = True                              # utterances that contain curses will automatically be labeled as cyberbullying later

    if cb >= no_cb:
        cb_class = 1
    elif contains_curses == True:                                                               # utterances that contain curses will automatically be labeled as cyberbullying
        cb_class = 1
    else:
        cb_class = 0

    return cb_class

# function to use the support vector machine algorithm on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_svm_sent_pos_ths(data_list, utterance_unprocessed, lex, test_utterance, file, column, matrix, mode):
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

    # find the classes of the utterances corresponding to the most similar vectors
    classes = []
    cb_list = machine_learning_processing.make_list_of_column(file, column)
    classes.append(cb_list[k1])
    classes.append(cb_list[k2])
    classes.append(cb_list[k3])
    classes.append(cb_list[k4])
    classes.append(cb_list[k5])

    if mode == 2:
        cb = classes.count("1") + classes.count("0")                            # number of most similiar utterances with the class cyberbulling
        no_cb = classes.count("2")                                              # number of most similiar utterances with the class no_cyberbulling
    else:
        cb = classes.count("1") + classes.count("2")
        no_cb = classes.count("0")

    cb_class = ""                                               # determine class of the test_utterance

    # probability that utterance is in class cyberbullying / no cyberbullying based on pos-tagging
    cb_pos_prob = compare_twitter_bullying.compare_vec_twitter_bullying_cb(utterance_unprocessed, 3)
    no_cb_pos_prob = 1 - cb_pos_prob

    cb = cb * cb_pos_prob
    no_cb = no_cb * no_cb_pos_prob

    contains_curses = False
    curses = machine_learning_processing.make_list_of_curse_words("curses.txt")

    for word in test_utterance:
        if word in curses:
            contains_curses = True                              # utterances that contain curses will automatically be labeled as cyberbullying later

    if cb >= no_cb:
        cb_class = 1
    elif contains_curses == True:                                                               # utterances that contain curses will automatically be labeled as cyberbullying
        cb_class = 1
    else:
        cb_class = 0

    return cb_class

# function to use the support vector machine algorithm on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_svm_sent_pos_hs_ld(data_list, utterance_unprocessed, lex, test_utterance, file, column, matrix, mode):
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

    distances = []                                              # array of distances to each vector of the training set
    np_vec = np.array(vec_test_utterance)
    vec_len = np.linalg.norm(np_vec)                            # length of test_vector

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

    # find the classes of the utterances corresponding to the most similar vectors
    classes = []
    cb_list = machine_learning_processing.make_list_of_column(file, column)
    classes.append(cb_list[k1])
    classes.append(cb_list[k2])
    classes.append(cb_list[k3])
    classes.append(cb_list[k4])
    classes.append(cb_list[k5])

    if mode == 2:
        cb = classes.count("0")                                         # number of most similiar utterances with the class cyberbulling
        no_cb = classes.count("2") + classes.count("1")                 # number of most similiar utterances with the class no_cyberbulling
    else:
        cb = classes.count("2")
        no_cb = classes.count("0") + classes.count("1")

    cb_class = ""                                               # determine class of the test_utterance

    # probability that utterance is in class cyberbullying / no cyberbullying based on pos-tagging
    cb_pos_prob = compare_labeled_data.compare_vec_labeled_data_hs(utterance_unprocessed, 3)
    no_cb_pos_prob = 1 - cb_pos_prob

    cb = cb * cb_pos_prob
    no_cb = no_cb * no_cb_pos_prob

    contains_curses = False
    curses = machine_learning_processing.make_list_of_curse_words("curses.txt")

    for word in test_utterance:
        if word in curses:
            contains_curses = True                              # utterances that contain curses will automatically be labeled as cyberbullying later

    if cb >= no_cb:
        cb_class = 1
    elif contains_curses == True:                                                               # utterances that contain curses will automatically be labeled as cyberbullying
        cb_class = 1
    else:
        cb_class = 0

    return cb_class

# function to use the support vector machine algorithm on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_svm_sent_pos_hs_ths(data_list, utterance_unprocessed, lex, test_utterance, file, column, matrix, mode):
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

    distances = []                                              # array of distances to each vector of the training set
    np_vec = np.array(vec_test_utterance)
    vec_len = np.linalg.norm(np_vec)                            # length of test_vector

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

    # probability that utterance is in class cyberbullying / no cyberbullying based on pos-tagging
    cb_pos_prob = compare_twitter_bullying.compare_vec_twitter_bullying_cb(utterance_unprocessed, 3)
    no_cb_pos_prob = 1 - cb_pos_prob

    cb = cb * cb_pos_prob
    no_cb = no_cb * no_cb_pos_prob

    contains_curses = False
    curses = machine_learning_processing.make_list_of_curse_words("curses.txt")

    for word in test_utterance:
        if word in curses:
            contains_curses = True                              # utterances that contain curses will automatically be labeled as cyberbullying later

    if cb >= no_cb:
        cb_class = 1
    elif contains_curses == True:                                                               # utterances that contain curses will automatically be labeled as cyberbullying
        cb_class = 1
    else:
        cb_class = 0

    return cb_class

# function to label a test set using the Support Vector Machine algorithm and to save results in a new file
def do_test_set_svm_sent_ld(utterances_test, utterances_unprocessed, utterances_training, filename, lex_pos, lex_neut, lex_neg, file, column, matrix_pos, matrix_neut, matrix_neg, sentimentfile, columnname, mode):
    # annotation using svm will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", columnname])  # header

        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile, 1)

        utterance_id = 0
        for utterance in utterances_test:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            # use lexicon with positive, neutral or negative vocabulary based on the sentiment of the utterance
            if list_of_sentiments[utterance_id] == 1 or list_of_sentiments[utterance_id] == "1":
                class_cb = do_svm_sent_pos_ld(utterances_training, utterance_unprocessed, lex_pos, utterance, file, column, matrix_pos, mode)                        # determine class of the utterance using do_svm()
            elif list_of_sentiments[utterance_id] == 0 or list_of_sentiments[utterance_id] == "0":
                class_cb = do_svm_sent_pos_ld(utterances_training, utterance_unprocessed, lex_neut, utterance, file, column, matrix_neut, mode)
            else:
                class_cb = do_svm_sent_pos_ld(utterances_training, utterance_unprocessed, lex_neg, utterance, file, column, matrix_neg, mode)

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

# function to label a test set using the Support Vector Machine algorithm and to save results in a new file
def do_test_set_svm_sent_ths(utterances_test, utterances_unprocessed, utterances_training, filename, lex_pos, lex_neut, lex_neg, file, column, matrix_pos, matrix_neut, matrix_neg, sentimentfile, columnname, mode):
    # annotation using svm will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", columnname])  # header

        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile, 1)

        utterance_id = 0
        for utterance in utterances_test:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            # use lexicon with positive, neutral or negative vocabulary based on the sentiment of the utterance
            if list_of_sentiments[utterance_id] == 1 or list_of_sentiments[utterance_id] == "1":
                class_cb = do_svm_sent_pos_ths(utterances_training, utterance_unprocessed, lex_pos, utterance, file, column, matrix_pos, mode)                        # determine class of the utterance using do_svm()
            elif list_of_sentiments[utterance_id] == 0 or list_of_sentiments[utterance_id] == "0":
                class_cb = do_svm_sent_pos_ths(utterances_training, utterance_unprocessed, lex_neut, utterance, file, column, matrix_neut, mode)
            else:
                class_cb = do_svm_sent_pos_ths(utterances_training, utterance_unprocessed, lex_neg, utterance, file, column, matrix_neg, mode)

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

# function to label a test set using the Support Vector Machine algorithm and to save results in a new file
def do_test_set_svm_sent_hs_ld(utterances_test, utterances_unprocessed, utterances_training, filename, lex_pos, lex_neut, lex_neg, file, column, matrix_pos, matrix_neut, matrix_neg, sentimentfile, columnname, mode):
    # annotation using svm will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", columnname])  # header

        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile, 1)

        utterance_id = 0
        for utterance in utterances_test:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            # use lexicon with positive, neutral or negative vocabulary based on the sentiment of the utterance
            if list_of_sentiments[utterance_id] == 1 or list_of_sentiments[utterance_id] == "1":
                class_cb = do_svm_sent_pos_hs_ld(utterances_training, utterance_unprocessed, lex_pos, utterance, file, column, matrix_pos, mode)                        # determine class of the utterance using do_svm()
            elif list_of_sentiments[utterance_id] == 0 or list_of_sentiments[utterance_id] == "0":
                class_cb = do_svm_sent_pos_hs_ld(utterances_training, utterance_unprocessed, lex_neut, utterance, file, column, matrix_neut, mode)
            else:
                class_cb = do_svm_sent_pos_hs_ld(utterances_training, utterance_unprocessed, lex_neg, utterance, file, column, matrix_neg, mode)

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

# function to label a test set using the Support Vector Machine algorithm and to save results in a new file
def do_test_set_svm_sent_hs_ths(utterances_test, utterances_unprocessed, utterances_training, filename, lex_pos, lex_neut, lex_neg, file, column, matrix_pos, matrix_neut, matrix_neg, sentimentfile, columnname, mode):
    # annotation using svm will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", columnname])  # header

        list_of_sentiments = machine_learning_processing.make_list_of_column(sentimentfile, 1)

        utterance_id = 0
        for utterance in utterances_test:
            utterance_unprocessed = utterances_unprocessed[utterance_id]
            # use lexicon with positive, neutral or negative vocabulary based on the sentiment of the utterance
            if list_of_sentiments[utterance_id] == 1 or list_of_sentiments[utterance_id] == "1":
                class_cb = do_svm_sent_pos_hs_ths(utterances_training, utterance_unprocessed, lex_pos, utterance, file, column, matrix_pos, mode)                        # determine class of the utterance using do_svm()
            elif list_of_sentiments[utterance_id] == 0 or list_of_sentiments[utterance_id] == "0":
                class_cb = do_svm_sent_pos_hs_ths(utterances_training, utterance_unprocessed, lex_neut, utterance, file, column, matrix_neut, mode)
            else:
                class_cb = do_svm_sent_pos_hs_ths(utterances_training, utterance_unprocessed, lex_neg, utterance, file, column, matrix_neg, mode)

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

# labeled data
test_list_ld = machine_learning_processing.process_data("labeled_data_test.csv", 6)
training_list_ld = machine_learning_processing.process_data("labeled_data_test.csv", 6)
test_list_ld_unprocessed = machine_learning_processing.make_list_of_column("labeled_data_test.csv", 6)
term_utterance_matrix_ld = support_vector_machine.do_matrix(training_list_ld, "lexicon_ld.txt")
matrix_pos_ld = support_vector_machine.do_matrix(training_list_ld, "lexicon_pos_ld.txt")
matrix_neut_ld = support_vector_machine.do_matrix(training_list_ld, "lexicon_neut_ld.txt")
matrix_neg_ld = support_vector_machine.do_matrix(training_list_ld, "lexicon_neg_ld.txt")
do_test_set_svm_sent_ld(test_list_ld, test_list_ld_unprocessed, training_list_ld, "labeled_data_svm_final.csv", "lexicon_pos_ld.txt", "lexicon_neut_ld.txt", "lexicon_neg_ld.txt", "labeled_data_train.csv", 5, matrix_pos_ld, matrix_neut_ld, matrix_neg_ld, "labeled_data_test_with_sentiment.csv", "Cyberbullying", 2)
do_test_set_svm_sent_hs_ld(test_list_ld, test_list_ld_unprocessed, training_list_ld, "labeled_data_svm_final_hs.csv", "lexicon_pos_ld.txt", "lexicon_neut_ld.txt", "lexicon_neg_ld.txt", "labeled_data_train.csv", 5, matrix_pos_ld, matrix_neut_ld, matrix_neg_ld, "labeled_data_test_with_sentiment.csv", "Hate Speech", 2)
estimation.test_results("labeled_data_test.csv", 5, "labeled_data_svm_final.csv", 1)
estimation.test_results("labeled_data_test.csv", 5, "labeled_data_svm_final_hs.csv", 1)

estimation.test_results("labeled_data_test.csv", 5, "labeled_data_svm.csv", 1)
estimation.test_results("labeled_data_test.csv", 5, "labeled_data_svm_hs.csv", 1)

# twitter hate speech
test_list_ths = machine_learning_processing.process_data("twitter_hate_speech_test.csv", 1)
training_list_ths = machine_learning_processing.process_data("twitter_hate_speech_test.csv", 1)
test_list_ths_unprocessed = machine_learning_processing.make_list_of_column("twitter_hate_speech_test.csv", 1)
term_utterance_matrix_ths = support_vector_machine.do_matrix(training_list_ths, "lexicon_ths.txt")
matrix_pos_ths = support_vector_machine.do_matrix(training_list_ths, "lexicon_pos_ths.txt")
matrix_neut_ths = support_vector_machine.do_matrix(training_list_ths, "lexicon_neut_ths.txt")
matrix_neg_ths = support_vector_machine.do_matrix(training_list_ths, "lexicon_neg_ths.txt")
do_test_set_svm_sent_ths(test_list_ths, test_list_ths_unprocessed, training_list_ths, "twitter_hate_speech_svm_final.csv", "lexicon_pos_ths.txt", "lexicon_neut_ths.txt", "lexicon_neg_ths.txt", "twitter_hate_speech_train.csv", 2, matrix_pos_ths, matrix_neut_ths, matrix_neg_ths, "twitter_hate_speech_test_with_sentiment.csv", "Cyberbullying", 3)
do_test_set_svm_sent_hs_ths(test_list_ths, test_list_ths_unprocessed, training_list_ths, "twitter_hate_speech_svm_final_hs.csv", "lexicon_pos_ths.txt", "lexicon_neut_ths.txt", "lexicon_neg_ths.txt", "twitter_hate_speech_train.csv", 2, matrix_pos_ths, matrix_neut_ths, matrix_neg_ths, "twitter_hate_speech_test_with_sentiment.csv", "Hate Speech", 3)
estimation.test_results("twitter_hate_speech_test.csv", 2, "twitter_hate_speech_svm_final.csv", 1)
estimation.test_results("twitter_hate_speech_test.csv", 2, "twitter_hate_speech_svm_final_hs.csv", 1)

estimation.test_results("twitter_hate_speech_test.csv", 2, "twitter_hate_speech_svm.csv", 1)
estimation.test_results("twitter_hate_speech_test.csv", 2, "twitter_hate_speech_svm_hs.csv", 1)