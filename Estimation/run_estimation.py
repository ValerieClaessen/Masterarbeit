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

    result_s1 = results[0]
    result_s2 = results[1]
    result_s3 = results[2]
    result_s4 = results[3]
    result_s5 = results[4]

    #results_estimate = estimate(doc_original, row1, doc_compare, row2)


    # s1 = results[0]
    # s2 = results[1]
    # s3 = results[2]
    # s4 = results[3]
    # s5 = results[4]

    s1_pos = result_s1[0]
    s2_pos = result_s2[0]
    s3_pos = result_s3[0]
    s4_pos = result_s4[0]
    s5_pos = result_s5[0]

    wrong_s1_s2 = result_s1[1]
    wrong_s1_s3 = result_s1[2]
    wrong_s1_s4 = result_s1[3]
    wrong_s1_s5 = result_s1[4]

    wrong_s2_s1 = result_s2[1]
    wrong_s2_s3 = result_s2[2]
    wrong_s2_s4 = result_s2[3]
    wrong_s2_s5 = result_s2[4]

    wrong_s3_s1 = result_s3[1]
    wrong_s3_s2 = result_s3[2]
    wrong_s3_s4 = result_s3[3]
    wrong_s3_s5 = result_s3[4]

    wrong_s4_s1 = result_s4[1]
    wrong_s4_s2 = result_s4[2]
    wrong_s4_s3 = result_s4[3]
    wrong_s4_s5 = result_s4[4]

    wrong_s5_s1 = result_s5[1]
    wrong_s5_s2 = result_s5[2]
    wrong_s5_s3 = result_s5[3]
    wrong_s5_s4 = result_s5[4]

    #recall = results_estimate[0]
    #precision = results_estimate[1]
    #accuracy = results_estimate[2]



    x = prettytable.PrettyTable(["", "1", "2", "3", "4", "5" ])
    x.add_row(["S1", s1_pos, wrong_s1_s2, wrong_s1_s3, wrong_s1_s4, wrong_s1_s5])
    x.add_row(["S2", wrong_s2_s1, s2_pos, wrong_s2_s3, wrong_s2_s4, wrong_s2_s5])
    x.add_row(["S3", wrong_s3_s1, wrong_s3_s2, s3_pos, wrong_s3_s4, wrong_s3_s5])
    x.add_row(["S4", wrong_s4_s1, wrong_s4_s2, wrong_s4_s3, s4_pos, wrong_s4_s5])
    x.add_row(["S5", wrong_s5_s1, wrong_s5_s2, wrong_s5_s3, wrong_s5_s4, s5_pos])

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

# FINAL Cyberbullying Vergleich mit (Cyberbullying-Spalte: 1) = tbt_cb_final


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


# FINAL Cyberbullying Vergleich mit (Cyberbullying-Spalte: 1) = tbt_cb_final
# 01 =twitter_bullying_naive_bayes_final
# 02 =twitter_bullying_mem_final
# 03 =twitter_bullying_svm_final



build_txt("test_set.csv", "twitter_bullying_naive_bayes_final.csv", 'Textdocuments/tbt_cb_final_01.txt', 'test_set and twitter_bullying_naive_bayes_final', 7, 1)
build_txt("test_set.csv", "twitter_bullying_mem_final.csv", 'Textdocuments/tbt_cb_final_02.txt', 'test_set and twitter_bullying_mem_final', 7, 1)
build_txt("test_set.csv", "twitter_bullying_svm_final.csv", 'Textdocuments/tbt_cb_final_03.txt', 'test_set and twitter_bullying_svm_final', 7, 1)

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


# FINAL Cyberbullying Vergleich mit (Stärke-Typ-Spalte: 1) = tbt_str_final
# 01 =twitter_bullying_naive_bayes_final_strength
# 02 =twitter_bullying_mem_final_strength
# 03 =twitter_bullying_svm_final_strength



build_txt_strength("test_cb_set.csv", "twitter_bullying_naive_bayes_final_strength.csv", 'Textdocuments/tbt_str_final_01.txt', 'test_cb_set and twitter_bullying_naive_bayes_final_strength', 8, 1)
build_txt_strength("test_cb_set.csv", "twitter_bullying_mem_final_strength.csv", 'Textdocuments/tbt_str_final_02.txt', 'test_cb_set and twitter_bullying_mem_final_strength', 8, 1)
build_txt_strength("test_cb_set.csv", "twitter_bullying_svm_final_strength.csv", 'Textdocuments/tbt_str_final_03.txt', 'test_cb_set and twitter_bullying_svm_final_strength', 8, 1)


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

# Hate-Speech-Vergleich mit (Hate-Speech-Spalte: 1) = tbt_hs
# 01 =twitter_bullying_naive_bayes_final_hs
# 02 =twitter_bullying_mem_final_hs
# 03 =twitter_bullying_svm_final_hs

build_txt("test_set.csv", "twitter_bullying_naive_bayes_final_hs.csv", 'Textdocuments/tbt_hs_final_01.txt', 'test_set and twitter_bullying_naive_bayes_final_hs', 9, 1)
build_txt("test_set.csv", "twitter_bullying_mem_final_hs.csv", 'Textdocuments/tbt_hs_final_02.txt', 'test_set and twitter_bullying_mem_final_hs', 9, 1)
build_txt("test_set.csv", "twitter_bullying_svm_final_hs.csv", 'Textdocuments/tbt_hs_final_03.txt', 'test_set and twitter_bullying_svm_final_hs', 9, 1)



# Cyberbullying Vergleich mit (Cyberbullying-Spalte: 1) = bt_cb
# 01 =bullying_traces_naive_bayes
# 02 =bullying_traces_mem
# 03 =bullying_traces_svm

build_txt("bullying_traces_test.csv", "bullying_traces_naive_bayes.csv", 'Textdocuments/bt_cb_01.txt', 'bullying_traces_test and bullying_traces_naive_bayes', 3, 1)
build_txt("bullying_traces_test.csv", "bullying_traces_mem.csv", 'Textdocuments/bt_cb_02.txt', 'bullying_traces_test and bullying_traces_mem', 3, 1)
build_txt("bullying_traces_test.csv", "bullying_traces_svm.csv", 'Textdocuments/bt_cb_03.txt', 'bullying_traces_test and bullying_traces_svm', 3, 1)

# FINAL Cyberbullying Vergleich mit (Cyberbullying-Spalte: 1) = bt_cb_final
# 01 =bullying_traces_naive_bayes_final
# 02 =bullying_traces_mem_final
# 03 =bullying_traces_svm_final

build_txt("bullying_traces_test.csv", "bullying_traces_naive_bayes_final.csv", 'Textdocuments/bt_cb_final_01.txt', 'bullying_traces_test and bullying_traces_naive_bayes_final', 3, 1)
build_txt("bullying_traces_test.csv", "bullying_traces_mem_final.csv", 'Textdocuments/bt_cb_final_02.txt', 'bullying_traces_test and bullying_traces_mem_final', 3, 1)
build_txt("bullying_traces_test.csv", "bullying_traces_svm_final.csv", 'Textdocuments/bt_cb_final_03.txt', 'bullying_traces_test and bullying_traces_svm_final', 3, 1)


# Cyberbullying Vergleich mit (Cyberbullying-Spalte: 1) = ld_cb
# 01 =labeled_data_naive_bayes
# 02 =labeled_data_mem
# 03 =labeled_data_svm

build_txt("labeled_data_test.csv", "labeled_data_naive_bayes.csv", 'Textdocuments/ld_cb_01.txt', 'labeled_data_test and labeled_data_naive_bayes', 5, 1)
build_txt("labeled_data_test.csv", "labeled_data_mem.csv", 'Textdocuments/ld_cb_02.txt', 'labeled_data_test and labeled_data_mem', 5, 1)
build_txt("labeled_data_test.csv", "labeled_data_svm.csv", 'Textdocuments/ld_cb_03.txt', 'labeled_data_test and labeled_data_svm', 5, 1)

# FINAL Cyberbullying Vergleich mit (Cyberbullying-Spalte: 1) = ld_cb_final
# 01 =labeled_data_naive_bayes_final
# 02 =labeled_data_mem_final
# 03 =labeled_data_svm_final

build_txt("labeled_data_test.csv", "labeled_data_naive_bayes_final.csv", 'Textdocuments/ld_cb_final_01.txt', 'labeled_data_test and labeled_data_naive_bayes_final', 5, 1)
build_txt("labeled_data_test.csv", "labeled_data_mem_final.csv", 'Textdocuments/ld_cb_final_02.txt', 'labeled_data_test and labeled_data_mem_final', 5, 1)
build_txt("labeled_data_test.csv", "labeled_data_svm_final.csv", 'Textdocuments/ld_cb_final_03.txt', 'labeled_data_test and labeled_data_svm_final', 5, 1)


# Hate-Speech-Vergleich mit (Hate-Speech-Spalte: 1) = ld_hs
# labeled_data_naive_bayes_hs
# labeled_data_mem_hs
# labeled_data_svm_hs

build_txt("labeled_data_test.csv", "labeled_data_naive_bayes_hs.csv", 'Textdocuments/ld_hs_01.txt', 'labeled_data_test and labeled_data_naive_bayes_hs', 5, 1)
build_txt("labeled_data_test.csv", "labeled_data_mem_hs.csv", 'Textdocuments/ld_hs_02.txt', 'labeled_data_test and labeled_data_mem_hs', 5, 1)
build_txt("labeled_data_test.csv", "labeled_data_svm_hs.csv", 'Textdocuments/ld_hs_03.txt', 'labeled_data_test and labeled_data_svm_hs', 5, 1)

# FINAL Hate-Speech-Vergleich mit (Hate-Speech-Spalte: 1) = ld_hs_final
# labeled_data_naive_bayes_hs_final
# labeled_data_mem_hs_final
# labeled_data_svm_hs_final

build_txt("labeled_data_test.csv", "labeled_data_naive_bayes_final_hs.csv", 'Textdocuments/ld_hs_final_01.txt', 'labeled_data_test and labeled_data_naive_bayes_hs_final', 5, 1)
build_txt("labeled_data_test.csv", "labeled_data_mem_final_hs.csv", 'Textdocuments/ld_hs_final_02.txt', 'labeled_data_test and labeled_data_mem_hs_final', 5, 1)
build_txt("labeled_data_test.csv", "labeled_data_svm_final_hs.csv", 'Textdocuments/ld_hs_final_03.txt', 'labeled_data_test and labeled_data_svm_hs_final', 5, 1)


# Cyberbullying Vergleich mit (Cyberbullying-Spalte: 1) = thst_cb
# 01 =twitter_hate_speech_naive_bayes
# 02 =twitter_hate_speech_mem
# 03 =twitter_hate_speech_svm

build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_naive_bayes.csv", 'Textdocuments/thst_cb_01.txt', 'twitter_hate_speech_test and twitter_hate_speech_naive_bayes', 2, 1)
build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_mem.csv", 'Textdocuments/thst_cb_02.txt', 'twitter_hate_speech_test and twitter_hate_speech_mem', 2, 1)
build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_svm.csv", 'Textdocuments/thst_cb_03.txt', 'twitter_hate_speech_test and twitter_hate_speech_svm', 2, 1)

# FINAL Cyberbullying Vergleich mit (Cyberbullying-Spalte: 1) = thst_cb_final
# 01 =twitter_hate_speech_naive_bayes_final
# 02 =twitter_hate_speech_mem_final
# 03 =twitter_hate_speech_svm_final

build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_naive_bayes_final.csv", 'Textdocuments/thst_cb_final_01.txt', 'twitter_hate_speech_test and twitter_hate_speech_naive_bayes_final', 2, 1)
build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_mem_final.csv", 'Textdocuments/thst_cb_final_02.txt', 'twitter_hate_speech_test and twitter_hate_speech_mem_final', 2, 1)
build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_svm_final.csv", 'Textdocuments/thst_cb_final_03.txt', 'twitter_hate_speech_test and twitter_hate_speech_svm_final', 2, 1)


# Hate-Speech-Vergleich mit (Hate-Speech-Spalte: 1) = thst_hs
# 01 =twitter_hate_speech_naive_bayes_hs
# 02 =twitter_hate_speech_mem_hs
# 03 =twitter_hate_speech_svm_hs

build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_naive_bayes_hs.csv", 'Textdocuments/thst_hs_01.txt', 'twitter_hate_speech_test and twitter_hate_speech_naive_bayes_hs', 2, 1)
build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_mem_hs.csv", 'Textdocuments/thst_hs_02.txt', 'twitter_hate_speech_test and twitter_hate_speech_mem_hs', 2, 1)
build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_svm_hs.csv", 'Textdocuments/thst_hs_03.txt', 'twitter_hate_speech_test and twitter_hate_speech_svm_hs', 2, 1)

# FINAL Hate-Speech-Vergleich mit (Hate-Speech-Spalte: 1) = thst_hs_final
# 01 =twitter_hate_speech_naive_bayes_hs_final
# 02 =twitter_hate_speech_mem_hs_final
# 03 =twitter_hate_speech_svm_hs_final

build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_naive_bayes_final_hs.csv", 'Textdocuments/thst_hs_final_01.txt', 'twitter_hate_speech_test and twitter_hate_speech_naive_bayes_hs_final', 2, 1)
build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_mem_final_hs.csv", 'Textdocuments/thst_hs_final_02.txt', 'twitter_hate_speech_test and twitter_hate_speech_mem_hs_final', 2, 1)
build_txt("twitter_hate_speech_test.csv", "twitter_hate_speech_svm_final_hs.csv", 'Textdocuments/thst_hs_final_03.txt', 'twitter_hate_speech_test and twitter_hate_speech_svm_hs_final', 2, 1)

