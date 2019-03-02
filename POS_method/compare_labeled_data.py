import csv
import numpy as np
from numpy import median

from POS_method.process_single_tweet import process_single_tweet

# c1 = open("labeled_data_cos_dist.csv", "w")
# c1.truncate()
# c1.close()

testsentence_1 = "I love You!"
testsentence_2 = "Donald Trump is the President."
testsentence_3 = "Donald Trump is an Ass and a coward, I HATE him, ban Islam!!!"

# - Kann mit dem Vorgehen von K-Nearest-Neighbors zusammengelegt werden!
##### Berechnung der Cosinus-Distanz zwischen zwei Vektoren #####
# return: Distanz
def cos_sim(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

#####berechnen der knn#####
#input: tweet =Tweet der verglichen werden soll, row_number = Spalte vond er die Nachbarn "eingeholt" werden

def compare_vec_labeled_data_hs(tweet, row_number):
    dist_list = []
    vector = process_single_tweet(tweet)

    ##### Einlesen der Vektoren und berechnung der Cosinus-Distanz #####
    with open('labeled_data_files/labeled_data_train_vec.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            words = []
            int_words = []

            words = row[2].split(',')   #Aufspalten der Vektoren
            for word in words:
                word = int(word)
                int_words.append(word)  #schreiben in Liste als Integer

            cos = cos_sim(int_words, vector)  #Berechnung der Distanz zwischen Test-Vektor und Vektor aus .csv
            dist = {}
            dist["CB"] = row[row_number]
            dist["cos"] = cos
            #dist[row[3]] = cos
            dist_list.append(dist.copy())

    sorted_dist = sorted(dist_list, key=lambda k: k['cos'], reverse=True)
    knn_list = sorted_dist[:11]
    #cb = []
    # for x in knn_list:
    #     cb.append(int(x.get("CB")))
    # print(cb)
    hatespeech = 0
    for x in knn_list:
        if x.get("CB") == "0":
            hatespeech += 1



    return hatespeech/11

def compare_vec_labeled_data_cb(tweet, row_number):
    dist_list = []
    vector = process_single_tweet(tweet)

    ##### Einlesen der Vektoren und berechnung der Cosinus-Distanz #####
    with open('labeled_data_files/labeled_data_train_vec.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            words = []
            int_words = []

            words = row[2].split(',')   #Aufspalten der Vektoren
            for word in words:
                word = int(word)
                int_words.append(word)  #schreiben in Liste als Integer

            cos = cos_sim(int_words, vector)  #Berechnung der Distanz zwischen Test-Vektor und Vektor aus .csv
            dist = {}
            dist["CB"] = row[row_number]
            dist["cos"] = cos
            #dist[row[3]] = cos
            dist_list.append(dist.copy())

    sorted_dist = sorted(dist_list, key=lambda k: k['cos'], reverse=True)
    knn_list = sorted_dist[:11]
    #cb = []
    # for x in knn_list:
    #     cb.append(int(x.get("CB")))
    # print(cb)
    cyberbullying = 0
    for x in knn_list:
        #print(x.get("CB"))
        if x.get("CB") == "0" or x.get("CB") == "1" :
            cyberbullying += 1


    return cyberbullying/11


print("Testsentence 1")
print("Hatespeech Wahrscheinlichkeit= ",compare_vec_labeled_data_hs(testsentence_1, 3))
print("Cyberbullying Wahrscheinlichkeit= ",compare_vec_labeled_data_cb(testsentence_1, 3))

print("Testsentence 2")
print("Hatespeech Wahrscheinlichkeit= ",compare_vec_labeled_data_hs(testsentence_2, 3))
print("Cyberbullying Wahrscheinlichkeit= ",compare_vec_labeled_data_cb(testsentence_2, 3))

print("Testsentence 3")
print("Hatespeech Wahrscheinlichkeit= ",compare_vec_labeled_data_hs(testsentence_3, 3))
print("Cyberbullying Wahrscheinlichkeit= ",compare_vec_labeled_data_cb(testsentence_3, 3))



