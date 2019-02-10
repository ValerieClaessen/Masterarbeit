import csv
import numpy as np

c1 = open("POS_Testdaten_cos_dist.csv", "w")
c1.truncate()
c1.close()

test_vec = [7,1,2,1,0,0,0,0,0,1,2]
#TODO: Distanz nicht komplett für jeden Vergleichstweet in ein Dokument schreiben sondern direkt nur die 10 größten Werte in einer Liste zwischenspeichern
# - Kann mit dem Vorgehen von K-Nearest-Neighbors zusammengelegt werden!
##### Berechnung der Cosinus-Distanz zwischen zwei Vektoren #####
# return: Distanz
def cos_sim(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

##### Einlesen der Vektoren und berechnung der Cosinus-Distanz #####
with open('POS_Testdaten_vec.csv', 'r') as f:
    reader = csv.reader(f, delimiter=";")
    for row in reader:
        words = []
        int_words = []

        words = row[2].split(',')   #Ausspalten der Vektoren
        for word in words:
            word = int(word)
            int_words.append(word)  #schreiben in Liste als Integer

        cos = cos_sim(int_words, test_vec)  #Berechnung der Distanz zwischen Test-Vektor und Vektor aus .csv

        ##### Schreiben der Distanz in neue .csv #####
        with open('POS_Testdaten_cos_dist.csv', 'a') as c:
            writer2 = csv.writer(c, delimiter=';')
            writer2.writerow([row[0], row[1], row[2], row[3], cos]) #Ausgangstext, POS-Tags, Vektoren, Cyberbullying (1/0), Distanz zu Testvector

##### K-Nearest-Neighbors #####
with open('POS_Testdaten_cos_dist.csv', 'r') as c2:
    reader2 = csv.reader(c2, delimiter=";")
    d = []
    for row in reader2: #Liste aus allen Distanzen
        d.append(float(row[4]))

sorted_list = sorted(d, key=float, reverse=True)    #Liste in umgekehrter Reihenfolge Sortieren
knn = sorted_list[:10]  #nur die 10 größten Distanzen behalten


##### Werte wieder den Ausgangssätzen zuordnen #####
# - Aus den Einsen und Nullen der Cyberbullying-Zuordnung entsteht nun aus den KNN ein Prozentwert für die Wahrscheinlichkeit von CB des verglichenen Tweets
with open('POS_Testdaten_cos_dist.csv', 'r') as c3:
    reader3 = csv.reader(c3, delimiter=";")
    percent = 0

    for row in reader3:
        for value in knn:
            if float(row[4]) == value:
                percent += int(row[3])  #Zusammenaddieren aller CB-Werte
                #print(value)
                #print(float(row[4]))
                break

    print(percent)
