import nltk
import csv



def build_vector(tagged_tweet):


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

        for word in tagged_tweet:
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

        return vector