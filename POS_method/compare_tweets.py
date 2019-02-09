# Hier sollen die Vectoren der Trainingsdaten mit den Testdaten verglichen werden
#
import csv
# print(cosine_similarity(int_words, test_vec))

import numpy as np

c1 = open("POS_Testdaten_cos_dist.csv", "w")
c1.truncate()
c1.close()

def cos_sim(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)


test_vec = [7,1,2,1,0,0,0,0,0,1,2]

with open('POS_Testdaten_vec.csv', 'r') as f:
    reader = csv.reader(f, delimiter=";")
    for row in reader:
        words = []
        int_words = []

        words = row[2].split(',')
        for word in words:
            word = int(word)
            # print(type(word))
            int_words.append(word)

        cos = cos_sim(int_words, test_vec)

        with open('POS_Testdaten_cos_dist.csv', 'a') as c:
            writer2 = csv.writer(c, delimiter=';')
            writer2.writerow([row[0], row[1], row[2], row[3], cos])

with open('POS_Testdaten_cos_dist.csv', 'r') as c2:
    reader2 = csv.reader(c2, delimiter=";")
    d = []
    for row in reader2:
        d.append(float(row[4]))

sorted_list = sorted(d, key=float, reverse=True)
knn = sorted_list[:10]
#print(knn)


with open('POS_Testdaten_cos_dist.csv', 'r') as c3:
    reader3 = csv.reader(c3, delimiter=";")
    percent = 0

    for row in reader3:
        for value in knn:
            if float(row[4]) == value:
                percent += int(row[3])
                #print(value)
                #print(float(row[4]))
                break

    print(percent)
