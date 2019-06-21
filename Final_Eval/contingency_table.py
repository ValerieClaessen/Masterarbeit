from Flask.ml_processing import make_list_of_column


def test_chat(file1, column1, column2):
    # make lists of assigned cyberbullying values (0 / 1)
    cyberbullying1 = make_list_of_column(file1, column1)
    cyberbullying2 = make_list_of_column(file1, column2)

    right_cyberbullying = 0                     # utterance contains cyberbullying and was assigned cyberbullying
    right_no_cyberbullying = 0                  # utterance doesn't contain cyberbullying and was assigned no_cyberbullying
    wrong_cyberbullying = 0                     # utterance doesn't contain cyberbullying and was assigned cyberbullying
    wrong_no_cyberbullying = 0                  # utterance contains cyberbullying and was assigned no_cyberbullying

    cyberbullying = 0                           # number of utterances that contain cyberbullying
    no_cyberbullying = 0                        # number of utterances that don't contain cyberbullying

    # compare assigned cyberbullying values
    x = 0
    for item in cyberbullying1:
        print(item, cyberbullying2[x])
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

    #Liste to return: Cyberbullying, No Cyberbullying

    results = [str_cyberbullying, str_no_cyberbullying,"tp= ", str_right_cyberbullying, "tn= ",str_right_no_cyberbullying, "fp= ",str_wrong_cyberbullying,"fn= ", str_wrong_no_cyberbullying]

    return results

test_results_cb = test_chat("Testdatensatz.csv", 5, 3)
test_results_hs = test_chat("Testdatensatz.csv", 6, 4)
print("Cyberbullying: ",test_results_cb)
print("Hate Speech: ",test_results_hs)