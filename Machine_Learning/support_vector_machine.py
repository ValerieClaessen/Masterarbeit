import csv
import machine_learning_processing
import estimation
import math
import numpy as np

# function to use the support vector machine algorithm on an utterance of the test set
# returns the class for the utterances assigned by the algorithm
def do_svm(data_list, lex, test_utterance, file, column):
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

    for vector in term_utterance_matrix:                                    # loop through all vectors from the training set
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
    if cb == max([cb, no_cb]):
        cb_class = 1
    else:
        cb_class = 0
    #print(cb_class)

    return cb_class

# function to label a test set using the Support Vector Machine algorithm and to save results in a new file
def do_test_set_svm(utterances_test, utterances_training, filename, lex, file, column):
    # annotation using svm will be saved in a new file
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Utterance", "Cyberbullying"])  # header

        x = 0
        for utterance in utterances_test:
            class_cb = do_svm(utterances_training, lex, utterance, file, column)        # determine class of the utterance using do_svm()

            # write utterance and its assigned class into the file
            utterance_string = ""
            for word in utterance:
                utterance_string = utterance_string + word + " "
            writer.writerow([utterance_string, class_cb])
            x += 1

            print(x, class_cb)                                                                # count of utterances already labeled


utterance = machine_learning_processing.process_utterance("Yup. I can't stand this shit. The left screams and yells Black Lives Matter and the minute a black man or woman disappear")
utterance2 = machine_learning_processing.process_utterance("ban islam")
utterance3 = machine_learning_processing.process_utterance("This is our president. WHO talks like that?!? Our leader does. I cant. How embarrassing. A disgrace to the office.")

test_list = machine_learning_processing.process_data("twitter_bullying_test.csv")
training_list = machine_learning_processing.process_data("twitter_bullying_training.csv")

#do_svm(test_list, "lexicon.txt", utterance, "twitter_bullying_test.csv", 7)
#do_svm(test_list, "lexicon.txt", utterance2, "twitter_bullying_test.csv", 7)
#do_svm(test_list, "lexicon.txt", utterance3, "twitter_bullying_test.csv", 7)

#do_test_set_svm(test_list, training_list, "twitter_bullying_svm_test.csv", "lexicon.txt", "twitter_bullying_training.csv", 7)

estimation.test_results("twitter_bullying_test.csv", 7, "twitter_bullying_svm_test.csv", 1)