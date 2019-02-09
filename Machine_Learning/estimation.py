import machine_learning_processing

# function to quickly test the results of the algorithms
def test_results(file1, column1, file2, column2):
    # make lists of assigned cyberbullying values (0 / 1)
    cyberbullying1 = machine_learning_processing.make_list_of_column(file1, column1)
    cyberbullying2 = machine_learning_processing.make_list_of_column(file2, column2)

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

# function to estimate precision, recall and accuracy of the algorithm
def estimate():
    return