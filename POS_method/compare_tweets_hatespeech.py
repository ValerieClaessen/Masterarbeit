import csv
import numpy as np

from POS_method.process_single_tweet import process_single_tweet

c1 = open("POS_Testdaten_cos_dist_cb.csv", "w")
c1.truncate()
c1.close()

text = "Donald Trump is an Ass and a coward, I HATE him, ban Islam!!!"
#TODO: Distanz nicht komplett für jeden Vergleichstweet in ein Dokument schreiben sondern direkt nur die 10 größten Werte in einer Liste zwischenspeichern
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

def compare_vec_tweet(tweet, row_number):
    dist_list = []
    vector = process_single_tweet(tweet)

    ##### Einlesen der Vektoren und berechnung der Cosinus-Distanz #####
    with open('POS_Testdaten_vec_cb.csv', 'r') as f:
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
    knn_list = sorted_dist[:10]
    count_cb = 0
    for x in knn_list:
        cb = x.get("CB")
        count_cb += int(cb)
        #print(cb)

    percent = count_cb/10

    return percent


print("Hatespeech Wahrscheinlichkeit= " ,compare_vec_tweet(text, 5))   #Hate-Speech bei Cyberbullying = pos
print("Durchschnittsstärke des Cyberbullying (gerundet auf ganze Zahl)= " ,round(compare_vec_tweet(text, 4)))   #Stärke des Cyberbullying bei Cyberbullying = pos TODO: Hier muss noch besprochen werden, wie mit diesem Wert weiterhin umgegangen wird da er die aufaddierung aller Werte ist. Vorschlag: /10 weil das der Durchschnitt ist, wird so durch die Prozentberechnung gemacht, aktuell wird gerundet!

