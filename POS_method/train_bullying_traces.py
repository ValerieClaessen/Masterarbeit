import csv
import logging

import nltk

from POS_method.POS_test import prepare_POS_text, POS_specials_all



def train_data_bullying_traces():
    ##### Lesen der Ausgangssätze #####
    with open('bullying_traces_train.csv', 'r') as f8:
        reader = csv.reader(f8, delimiter = ";")
        for row in reader:
            text2 = ""
            cleaned = prepare_POS_text(row[0])  #Anwendung der Textbereinigung
            test_tags2 = []
            test_tags2 = nltk.pos_tag(cleaned)  #POS-tagging

            #with open('POS_tagged_data.csv', 'w') as w:
            #    w.write(POS_specials_all(test_tags2))


            logging.info('Starting POS-Tagging')

            ##### Schreiben der Ausgangssätze und POS-tags #####
            with open('bullying_traces_train_pos.csv', 'a') as f3:
                writer = csv.writer(f3, delimiter=';')
                str1 = ','.join(POS_specials_all(test_tags2))   #Anwenden des speziellen Taggens
                writer.writerow([row[0], str1, row[2], row[3], row[4], row[5]])         #Ausgangstext , POS-Tags, Cyberbullying (1/0)
            logging.info('POS-Tagging: END')

    ##### Erstellen der Vektoren der einzelnen Sätze #####
    with open('bullying_traces_train_pos.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            words = row[1].split(',')
            # print(words)

            N_counter = 0
            V_counter = 0
            J_counter = 0
            P_counter = 0
            R_counter = 0
            EXCL_counter = 0
            QUE_counter = 0
            CL_counter = 0
            sw_counter = 0
            name_counter = 0
            n_counter = 0

            for word in words:
                if word == "N" or word == "N ":
                    N_counter += 1
                elif word == "V" or word == "V ":
                    V_counter += 1
                elif word == "J" or word == "J ":
                    J_counter += 1
                elif word == "P" or word == "P ":
                    P_counter += 1
                elif word == "R" or word == "R ":
                    R_counter += 1
                elif word == "EXCL" or word == "EXCL ":
                    EXCL_counter += 1
                elif word == "QUE" or word == "QUE ":
                    QUE_counter += 1
                elif word == "CL" or word == "CL ":
                    CL_counter += 1
                elif word == "sw" or word == "sw ":
                    sw_counter += 1
                elif word == "name" or word == "name ":
                    name_counter += 1
                elif word == "n" or word == "n":
                    n_counter += 1

            # print(
            #     N_counter,
            #     V_counter,
            #     J_counter,
            #     P_counter,
            #     R_counter,
            #     EXCL_counter,
            #     QUE_counter,
            #     CL_counter,
            #     sw_counter,
            #     name_counter,
            #     n_counter)

            vector = []

            vector.extend((N_counter,
                           V_counter,
                           J_counter,
                           P_counter,
                           R_counter,
                           EXCL_counter,
                           QUE_counter,
                           CL_counter,
                           sw_counter,
                           name_counter,
                           n_counter))

            #print(vector)
            logging.info('Starting Vector')

            ##### Aufschreiben der Vektoren in neue .csv #####
            with open('bullying_traces_train_vec.csv', 'a') as f3:
                writer = csv.writer(f3, delimiter=';')
                str1 = ','.join(str(v) for v in vector)
                writer.writerow([row[0], row[1], str1, row[2], row[3], row[4], row[5]])     #Ausgangstext, POS-Tags, Vektoren, Cyberbullying (1/0)
            logging.info('Vector: END')

train_data_bullying_traces()