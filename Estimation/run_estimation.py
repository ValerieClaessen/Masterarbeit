import sys
import prettytable
from Machine_Learning.estimation import test_results, estimate, test_results_strengths


#print(test_results_strengths("test_set.csv", 8,"twitter_bullying_naive_bayes_sent_strength.csv",1))

def build_txt(doc_original, doc_compare, titel, header, row1, row2):
    results = test_results(doc_original, row1, doc_compare, row2) #Beispielanwendung
    results_estimate = estimate(doc_original, row1, doc_compare, row2)


    cb = results[0]
    no_cb = results[1]
    tp = results[2]
    tn = results[3]
    fp = results[4]
    fn = results[5]

    recall = results_estimate[0]
    precision = results_estimate[1]
    accuracy = results_estimate[2]



    x = prettytable.PrettyTable(["", "Gold Positive", "Gold Negative"])
    x.add_row(["System Positive", tp, fp])
    x.add_row(["System Negative", fn, tn])

    orig_stdout = sys.stdout
    f = open(titel, 'w')
    sys.stdout = f
    print("Evaluation: ", header)
    print("Column: Cyberbullying \n")
    print("Confusion Matrix")
    print(x, "\n")

    print("Precision = ", precision)
    print("Recall = ", recall)
    print("Accuracy = ", accuracy)

    sys.stdout = orig_stdout
    f.close()

def build_txt_strength(doc_original, doc_compare, titel, header, row1, row2):
    results = test_results_strengths(doc_original, row1, doc_compare, row2)
    #results_estimate = estimate(doc_original, row1, doc_compare, row2)


    s1 = results[0]
    s2 = results[1]
    s3 = results[2]
    s4 = results[3]
    s5 = results[4]

    s1_pos = results[5]
    s2_pos = results[6]
    s3_pos = results[7]
    s4_pos = results[8]
    s5_pos = results[9]

    s1_neg = results[10]
    s2_neg = results[11]
    s3_neg = results[12]
    s4_neg = results[13]
    s5_neg = results[14]

    #recall = results_estimate[0]
    #precision = results_estimate[1]
    #accuracy = results_estimate[2]



    x = prettytable.PrettyTable(["", "Positive", "Negative"])
    x.add_row(["S1", s1_pos, s1_neg])
    x.add_row(["S2", s2_pos, s2_neg])
    x.add_row(["S3", s3_pos, s3_neg])
    x.add_row(["S4", s4_pos, s4_neg])
    x.add_row(["S5", s5_pos, s5_neg])

    orig_stdout = sys.stdout
    f = open(titel, 'w')
    sys.stdout = f
    print("Evaluation: ", header)
    print("Column: Cyberbullying \n")
    print("Confusion Matrix")
    print(x, "\n")



    sys.stdout = orig_stdout
    f.close()


# Cyberbullying Vergleich mit (Cyberbullying-Spalte: 1) = tbt_cb
# 01 =twitter_bullying_naive_bayes2
# 02 =twitter_bullying_naive_bayes_c
# 03 =twitter_bullying_naive_bayes_sent
# 04 =twitter_bullying_naive_bayes_sent_c
# 05 =twitter_bullying_mem3
# 06 =twitter_bullying_mem_c
# 07 =twitter_bullying_mem_sent
# 08 =twitter_bullying_mem_sent_c
# 09 =twitter_bullying_svm_k2
# 10 =twitter_bullying_svm_k2_c
# 11 =twitter_bullying_svm_sent
# 12 =twitter_bullying_svm_sent_c

build_txt("test_set.csv", "twitter_bullying_naive_bayes2.csv", 'Textdocuments/tbt_cb_01.txt', 'test_set and twitter_bullying_naive_bayes2', 7, 1)
build_txt("test_set.csv", "twitter_bullying_naive_bayes_c.csv", 'Textdocuments/tbt_cb_02.txt', 'test_set and twitter_bullying_naive_bayes_c', 7, 1)
build_txt("test_set.csv", "twitter_bullying_naive_bayes_sent.csv", 'Textdocuments/tbt_cb_03.txt', 'test_set and twitter_bullying_naive_bayes_sent', 7, 1)
build_txt("test_set.csv", "twitter_bullying_naive_bayes_sent_c.csv", 'Textdocuments/tbt_cb_04.txt', 'test_set and twitter_bullying_naive_bayes_sent_c', 7, 1)
build_txt("test_set.csv", "twitter_bullying_mem3.csv", 'Textdocuments/tbt_cb_05.txt', 'test_set and twitter_bullying_mem3', 7, 1)
build_txt("test_set.csv", "twitter_bullying_mem_c.csv", 'Textdocuments/tbt_cb_06.txt', 'test_set and twitter_bullying_mem_c', 7, 1)
build_txt("test_set.csv", "twitter_bullying_mem_sent.csv", 'Textdocuments/tbt_cb_07.txt', 'test_set and twitter_bullying_mem_sent', 7, 1)
build_txt("test_set.csv", "twitter_bullying_mem_sent_c.csv", 'Textdocuments/tbt_cb_08.txt', 'test_set and twitter_bullying_mem_sent_c', 7, 1)
build_txt("test_set.csv", "twitter_bullying_svm_k2.csv", 'Textdocuments/tbt_cb_09.txt', 'test_set and twitter_bullying_svm_k2', 7, 1)
build_txt("test_set.csv", "twitter_bullying_svm_k2_c.csv", 'Textdocuments/tbt_cb_10.txt', 'test_set and twitter_bullying_svm_k2_c', 7, 1)
build_txt("test_set.csv", "twitter_bullying_svm_sent.csv", 'Textdocuments/tbt_cb_11.txt', 'test_set and twitter_bullying_svm_sent', 7, 1)
build_txt("test_set.csv", "twitter_bullying_svm_sent_c.csv", 'Textdocuments/tbt_cb_12.txt', 'test_set and twitter_bullying_svm_sent_c', 7, 1)

# Stärke-Vergleich mit (Stärke-Typ-Spalte: 1) = tbt_str
# 01 =twitter_bullying_naive_bayes_strength
# 02 =twitter_bullying_naive_bayes_sent_strength
# 03 =twitter_bullying_mem_strength
# 04 =twitter_bullying_mem_sent_strength
# 05 =twitter_bullying_svm_k2_strength
# 06 =twitter_bullying_svm_sent_strength
#
build_txt_strength("test_cb_set.csv", "twitter_bullying_naive_bayes_strength.csv", 'Textdocuments/tbt_str_01.txt', 'test_cb_set and twitter_bullying_naive_bayes_strength', 8, 1)
build_txt_strength("test_cb_set.csv", "twitter_bullying_naive_bayes_sent_strength.csv", 'Textdocuments/tbt_str_02.txt', 'test_cb_set and twitter_bullying_naive_bayes_sent_strength', 8, 1)
build_txt_strength("test_cb_set.csv", "twitter_bullying_mem_strength.csv", 'Textdocuments/tbt_str_03.txt', 'test_cb_set and twitter_bullying_mem_strength', 8, 1)
build_txt_strength("test_cb_set.csv", "twitter_bullying_mem_sent_strength.csv", 'Textdocuments/tbt_str_04.txt', 'test_cb_set and twitter_bullying_mem_sent_strength', 8, 1)
build_txt_strength("test_cb_set.csv", "twitter_bullying_svm_k2_strength.csv", 'Textdocuments/tbt_str_05.txt', 'test_cb_set and twitter_bullying_svm_k2_strength', 8, 1)
build_txt_strength("test_cb_set.csv", "twitter_bullying_svm_sent_strength.csv", 'Textdocuments/tbt_str_06.txt', 'test_cb_set and twitter_bullying_svm_sent_strength', 8, 1)

# Hate-Speech-Vergleich mit (Hate-Speech-Spalte: 1) = tbt_hs
# 01 =twitter_bullying_naive_bayes_hs
# 02 =twitter_bullying_naive_bayes_sent_hs
# 03 =twitter_bullying_mem_hs
# 04 =twitter_bullying_mem_sent_hs
# 05 =twitter_bullying_svm_k2_hs
# 06 =twitter_bullying_svm_sent_hs

build_txt("test_set.csv", "twitter_bullying_naive_bayes_hs.csv", 'Textdocuments/tbt_hs_01.txt', 'test_set and twitter_bullying_naive_bayes_hs', 9, 1)
build_txt("test_set.csv", "twitter_bullying_naive_bayes_sent_hs.csv", 'Textdocuments/tbt_hs_02.txt', 'test_set and twitter_bullying_naive_bayes_sent_hs', 9, 1)
build_txt("test_set.csv", "twitter_bullying_mem_hs.csv", 'Textdocuments/tbt_hs_03.txt', 'test_set and twitter_bullying_mem_hs', 9, 1)
build_txt("test_set.csv", "twitter_bullying_mem_sent_hs.csv", 'Textdocuments/tbt_hs_04.txt', 'test_set and twitter_bullying_mem_sent_hs', 9, 1)
build_txt("test_set.csv", "twitter_bullying_svm_k2_hs.csv", 'Textdocuments/tbt_hs_05.txt', 'test_set and twitter_bullying_svm_k2_hs', 9, 1)
build_txt("test_set.csv", "twitter_bullying_svm_sent_hs.csv", 'Textdocuments/tbt_hs_06.txt', 'test_set and twitter_bullying_svm_sent_hs', 9, 1)


# Cyberbullying Vergleich mit (Cyberbullying-Spalte: 1) = bt_cb
# 01 =bullying_traces_naive_bayes
# 02 =bullying_traces_mem
# 03 =bullying_traces_svm

build_txt("bullying_traces_test.csv", "bullying_traces_naive_bayes.csv", 'Textdocuments/bt_cb_01.txt', 'bullying_traces_test and bullying_traces_naive_bayes', 3, 1)
build_txt("bullying_traces_test.csv", "bullying_traces_mem.csv", 'Textdocuments/bt_cb_02.txt', 'bullying_traces_test and bullying_traces_mem', 3, 1)
#build_txt("bullying_traces_test.csv", "bullying_traces_svm.csv", 'Textdocuments/bt_cb_03.txt', 'bullying_traces_test and bullying_traces_svm', 3, 1)


# Cyberbullying Vergleich mit (Cyberbullying-Spalte: 1) = ld_cb
# 01 =labeled_data_naive_bayes
# 02 =labeled_data_mem
# 03 =labeled_data_svm

build_txt("labeled_data_test.csv", "labeled_data_naive_bayes.csv", 'Textdocuments/ld_cb_01.txt', 'labeled_data_test and labeled_data_naive_bayes', 5, 1)
build_txt("labeled_data_test.csv", "labeled_data_mem.csv", 'Textdocuments/ld_cb_02.txt', 'labeled_data_test and labeled_data_mem', 5, 1)
#build_txt("labeled_data_test.csv", "labeled_data_svm.csv", 'Textdocuments/ld_cb_03.txt', 'labeled_data_test and labeled_data_svm', 5, 1)


# Hate-Speech-Vergleich mit (Hate-Speech-Spalte: 1) = ld_hs
# labeled_data_naive_bayes_hs
# labeled_data_mem_hs
# labeled_data_svm_hs

build_txt("labeled_data_test.csv", "labeled_data_naive_bayes_hs.csv", 'Textdocuments/ld_hs_01.txt', 'labeled_data_test and labeled_data_naive_bayes_hs', 5, 1)
build_txt("labeled_data_test.csv", "labeled_data_mem_hs.csv", 'Textdocuments/ld_hs_02.txt', 'labeled_data_test and labeled_data_mem_hs', 5, 1)
#build_txt("labeled_data_test.csv", "labeled_data_svm_hs.csv", 'Textdocuments/ld_hs_03.txt', 'labeled_data_test and labeled_data_svm_hs', 5, 1)


# Cyberbullying Vergleich mit (Cyberbullying-Spalte: 1) = thst_cb
# 01 =twitter_hate_speech_naive_bayes
# 02 =twitter_hate_speech_mem
# 03 =twitter_hate_speech_svm

build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_naive_bayes.csv", 'Textdocuments/thst_cb_01.txt', 'twitter_hate_speech_test and twitter_hate_speech_naive_bayes', 2, 1)
build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_mem.csv", 'Textdocuments/thst_cb_02.txt', 'twitter_hate_speech_test and twitter_hate_speech_mem', 2, 1)
#build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_svm.csv", 'Textdocuments/thst_cb_03.txt', 'twitter_hate_speech_test and twitter_hate_speech_svm', 2, 1)


# Hate-Speech-Vergleich mit (Hate-Speech-Spalte: 1) = thst_hs
# 01 =twitter_hate_speech_naive_bayes_hs
# 02 =twitter_hate_speech_mem_hs
# 03 =twitter_hate_speech_svm_hs

build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_naive_bayes_hs.csv", 'Textdocuments/thst_hs_01.txt', 'twitter_hate_speech_test and twitter_hate_speech_naive_bayes_hs', 2, 1)
build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_mem_hs.csv", 'Textdocuments/thst_hs_02.txt', 'twitter_hate_speech_test and twitter_hate_speech_mem_hs', 2, 1)
#build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_svm_hs.csv", 'Textdocuments/thst_hs_03.txt', 'twitter_hate_speech_test and twitter_hate_speech_svm_hs', 2, 1)


