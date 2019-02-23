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

    str_cyberbullying = str(cyberbullying)
    str_no_cyberbullying = str(no_cyberbullying)
    str_right_cyberbullying = str(right_cyberbullying)
    str_right_no_cyberbullying = str(right_no_cyberbullying)
    str_wrong_cyberbullying = str(wrong_cyberbullying)
    str_wrong_no_cyberbullying = str(wrong_no_cyberbullying)

    print("Cyberbullying:" + " ", str_cyberbullying, " " + "No Cyberbullying:" + " " + str_no_cyberbullying)
    print("True Positive: ", str_right_cyberbullying, " " + "True Negative: ", str_right_no_cyberbullying, " " + "False Positive: ", str_wrong_cyberbullying, " " + "False Negative: ", str_wrong_no_cyberbullying)

# function to quickly test the strength results of the algorithms
def test_results_strengths(file1, column1, file2, column2):
    # make lists of assigned strength values (1 / 2 / 3 / 4 / 5)
    strength1 = machine_learning_processing.make_list_of_column(file1, column1)
    strength2 = machine_learning_processing.make_list_of_column(file2, column2)

    right_s1 = 0
    right_s2 = 0
    right_s3 = 0
    right_s4 = 0
    right_s5 = 0
    wrong_s1 = 0
    wrong_s2 = 0
    wrong_s3 = 0
    wrong_s4 = 0
    wrong_s5 = 0

    s1_count = 0                            # number of utterances labeled with s1
    s2_count = 0                            # number of utterances labeled with s2
    s3_count = 0                            # number of utterances labeled with s3
    s4_count = 0                            # number of utterances labeled with s4
    s5_count = 0                            # number of utterances labeled with s5

    # compare assigned cyberbullying values
    x = 0
    for item in strength1:
        if item == 1 or item == "1":
            s1_count += 1
            if strength2[x] == 1 or strength2[x] == "1":
                right_s1 += 1
            else:
                wrong_s1 += 1
        elif item == 2 or item == "2":
            s2_count += 1
            if strength2[x] == 2 or strength2[x] == "2":
                right_s2 += 1
            else:
                wrong_s2 += 1
        elif item == 3 or item == "3":
            s3_count += 1
            if strength2[x] == 3 or strength2[x] == "3":
                right_s3 += 1
            else:
                wrong_s3 += 1
        elif item == 4 or item == "4":
            s4_count += 1
            if strength2[x] == 4 or strength2[x] == "4":
                right_s4 += 1
            else:
                wrong_s4 += 1
        elif item == 5 or item == "5":
            s5_count += 1
            if strength2[x] == 5 or strength2[x] == "5":
                right_s5 += 1
            else:
                wrong_s5 += 1
        x += 1

    str_s1 = str(s1_count)
    str_right_s1 = str(right_s1)
    str_wrong_s1 = str(wrong_s1)
    str_s2 = str(s2_count)
    str_right_s2 = str(right_s2)
    str_wrong_s2 = str(wrong_s2)
    str_s3 = str(s3_count)
    str_right_s3 = str(right_s3)
    str_wrong_s3 = str(wrong_s3)
    str_s4 = str(s4_count)
    str_right_s4 = str(right_s4)
    str_wrong_s4 = str(wrong_s4)
    str_s5 = str(s5_count)
    str_right_s5 = str(right_s5)
    str_wrong_s5 = str(wrong_s5)

    print("s1:" + " ", str_s1, " " + "s2:" + " " + str_s2 + " " + "s3:" + " " + str_s3 + " " + "s4:" + " " + str_s4 + " " + "s5:" + " " + str_s5)
    print("S1 Positive: ", str_right_s1, " " + "S1 Negative: ", str_wrong_s1)
    print("S2 Positive: ", str_right_s2, " " + "S2 Negative: ", str_wrong_s2)
    print("S3 Positive: ", str_right_s3, " " + "S3 Negative: ", str_wrong_s3)
    print("S4 Positive: ", str_right_s4, " " + "S4 Negative: ", str_wrong_s4)
    print("S5 Positive: ", str_right_s5, " " + "S5 Negative: ", str_wrong_s5)

# function to estimate precision, recall and accuracy of the algorithm
def estimate():
    return