import csv
import numpy as np
from numpy import median

from POS_method.process_single_tweet import process_single_tweet

text = "Donald Trump is an Ass and a coward, I HATE him!!!"
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

def compare_vec_twitter_bullying(tweet, row_number):
    dist_list = []
    vector = process_single_tweet(tweet)

    ##### Einlesen der Vektoren und berechnung der Cosinus-Distanz #####
    with open('twitter_bullying_files/twitter_bullying_train_vec.csv', 'r') as f:
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
    cb = []
    for x in knn_list:
        cb.append(int(x.get("CB")))
    print(cb)
    #TODO: Ist hier wirklich der Median angemessen oder soll doch eine Art Mittelwert angegeben werden?
    return median(cb)


print("Cyberbullying Wahrscheinlichkeit= ",compare_vec_twitter_bullying(text, 3))


