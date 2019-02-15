import nltk
import csv
import logging
from nltk import word_tokenize
from nltk.corpus import stopwords
#nltk.download()
from POS_method.build_single_vector import build_vector

# c1 = open("POS_Testdaten_vec.csv", "w")
# c1.truncate()
# c1.close()
#
# c2 = open("POS_Testdaten_test.csv", "w")
# c2.truncate()
# c2.close()
#
# c3 = open("POS_Testdaten_compare.csv", "w")
# c3.truncate()
# c3.close()

swearword_tag = "sw"
text = "I hate my fucking ugly friend who is called LISA Marie Schuster!!!!"
upper_test = "HAfTgggE"

##### Methode bereitet Zeilen auf POS-Tagging vor #####
# - bei Bedarf Stopworte entfernen
# - bei Bedarf nicht-alphanumerische Zeichen entfernen (wird aktuell nicht gemacht damit Satzzeichen beachtet werden können)
# return: Zeile mit veränderter Zeile
def prepare_POS_text(row):
    tokens = word_tokenize(row)
    stop_words = set(stopwords.words('english'))
    #words = [word for word in tokens if word.isalpha()] #auf alphanumerische Zeichen prüfen
    words = [w for w in tokens if not w in stop_words]   #Stopworte entfernen
    return words



tokens = nltk.word_tokenize(text)   #tokenizing

test_tags= nltk.pos_tag(prepare_POS_text(text)) #POS-tagging

##### Methode untersucht wie viele Buchstaben in einem Wort großgeschrieben sind #####
# return: Anzhal an großgeschriebenen Buchstaben in einem Wort
def check_upper_word(word):
    char_count = 0
    for char in word:
        if char >= 'A' and char <= 'Z':
            char_count += 1
    return char_count




##### Methode fügt die gewünschten POS-Tag veränderungen ein #####
# - POS-Tags zu Gruppen zusammenfügen
# - Fragezeichen und Ausrufezeichen markieren
# - Capslock erkennen und markieren, danach werden die worte in lower case umgewandelt und normal weiter getagged   [CL]
# - Abgleich der getaggten Wörter mit Wörterbüchern:
#       1. Schimpfworte [sw]
#       2. Namen (Vornamen > Nachnamen > Zweite Vornamen)   [name]
#       3. negative Worte   [n]
#       --> Reichenfolge ist dabei zu beachten da diese Tags nicht doppelt vergeben werden können
# TODO: Smileyerkennung


def POS_specials_all(pos_tags):
    pos_tags_man = []   #Liste mit fertiger Taggung die zurückgegeben wird (jeweils eine Zeile)

    for tag in pos_tags:
        if tag[1] == "NNP" or tag[1] == "NNS" or tag[1] == "NN" or tag[1] == "NNPS":    #Nomen
            new_pos = list(tag)
            new_pos[1] = "N"

        elif tag[1] == "VBG" or tag[1] == "VBP" or tag[1] == "VB" or tag[1] == "VBN" or tag[1] == "VBZ" or tag[1] == "VBD": #Verben
            new_pos = list(tag)
            new_pos[1] = "V"

        elif tag[1] == "JJ" or tag[1] == "JJR" or tag[1] == "JJS":  #Adjektive
            new_pos = list(tag)
            new_pos[1] = "J"

        elif tag[1] == "PDT" or tag[1] == "POS" or tag[1] == "PRP" or tag[1] == "PRP$": #Pronomen
            new_pos = list(tag)
            new_pos[1] = "P"

        elif tag[1] == "RB" or tag[1] == "RBR" or tag[1] == "RBS" or tag[1] == "RP":    #Adverbien
            new_pos = list(tag)
            new_pos[1] = "R"

        elif tag[0] == "!" :    #Ausrufezeichen
            new_pos = list(tag)
            new_pos[1] = "EXCL"

        elif tag[0] == "?" :    #Fragezeichen
            new_pos = list(tag)
            new_pos[1] = "QUE"

        else:
            new_pos = list(tag)
            new_pos[1] = tag[1]



        if check_upper_word(tag[0]) >= 2:   #Capslock (bei mind. 2 großgeschriebenen Zeichen)

            to_lower = ''.join(tag[0])
            low = nltk.tag.pos_tag([to_lower.lower()])
            for item in low:

                if item[1] == "NNP" or item[1] == "NNS" or item[1] == "NN" or item[1] == "NNPS":  # Nomen
                    item = list(item)
                    item[1] = "N"

                elif item[1] == "VBG" or item[1] == "VBP" or item[1] == "VB" or item[1] == "VBN" or item[1] == "VBZ" or item[
                    1] == "VBD":  # Verben
                    item = list(item)
                    item[1] = "V"

                elif item[1] == "JJ" or item[1] == "JJR" or item[1] == "JJS":  # Adjektive
                    item = list(item)
                    item[1] = "J"

                elif item[1] == "PDT" or item[1] == "POS" or item[1] == "PRP" or item[1] == "PRP$":  # Pronomen
                    item = list(item)
                    item[1] = "P"

                elif item[1] == "RB" or item[1] == "RBR" or tag[1] == "RBS" or tag[1] == "RP":  # Adverbien
                    item = list(item)
                    item[1] = "R"



                new_pos[1] = item[1] + " ,CL"



        else:
            new_pos[1] = new_pos[1]


        written = False
        f = open('list.txt', 'r')
        for line in f:
            if tag[0].lower() == line.lower().strip():
                new_pos[1] = new_pos[1] + " ,sw"

                written = True
                break
        f1 = open('first-names.txt', 'r')
        for line in f1:
            if tag[0].lower() == line.lower().strip():
                new_pos[1] = new_pos[1] + " ,name"

                written = True
                break
        f2 = open('names.txt', 'r')
        for line in f2:
            if tag[0].lower() == line.lower().strip() and written == False: #wichtig: Vornamen werden Nachnamen bevorzugt
                new_pos[1] = new_pos[1] + " ,name"

                written = True
                break
        f3 = open('middle-names.txt', 'r')
        for line in f3:
            if tag[0].lower() == line.lower().strip() and written == False:  # wichtig: Vornamen werden Nachnamen bevorzugt
                new_pos[1] = new_pos[1] + " ,name"

                written = True
                break
        f4 = open('negative-words.txt', 'r')
        for line in f4:
            if tag[0].lower() == line.lower().strip() and written == False:  # wichtig: Vornamen werden Nachnamen bevorzugt
                new_pos[1] = new_pos[1] + " ,n"

                written = True
                break
        # f5 = open('smileys.txt', 'r')
        # for line in f5:
        #     if tag[0].strip("<").strip(">") == line and written == False:  # wichtig: Vornamen werden Nachnamen bevorzugt
        #         new_pos[1] = "smiley"
        #
        #         written = True
        #         break
        #if written == False:
        #    #new_pos = list(tag)
        #    new_pos[1] = new_pos[1]

        new_tag = tuple(new_pos)    #Umwandlung zurück in Tupel
        pos_tags_man.append(new_tag[1])


    return pos_tags_man

# def train_data():
#     ##### Lesen der Ausgangssätze #####
#     with open('POS_Testdaten.csv', 'r') as f8:
#         reader = csv.reader(f8, delimiter = ";")
#         for row in reader:
#             text2 = ""
#             cleaned = prepare_POS_text(row[0])  #Anwendung der Textbereinigung
#             test_tags2 = []
#             test_tags2 = nltk.pos_tag(cleaned)  #POS-tagging
#
#             #with open('POS_tagged_data.csv', 'w') as w:
#             #    w.write(POS_specials_all(test_tags2))
#
#
#             logging.info('Starting POS-Tagging')
#
#             ##### Schreiben der Ausgangssätze und POS-tags #####
#             with open('POS_Testdaten_test.csv', 'a') as f3:
#                 writer = csv.writer(f3, delimiter=';')
#                 str1 = ','.join(POS_specials_all(test_tags2))   #Anwenden des speziellen Taggens
#                 writer.writerow([row[0], str1, row[2]])         #Ausgangstext , POS-Tags, Cyberbullying (1/0)
#             logging.info('POS-Tagging: END')
#
#     ##### Erstellen der Vektoren der einzelnen Sätze #####
#     with open('POS_Testdaten_test.csv', 'r') as f:
#         reader = csv.reader(f, delimiter=";")
#         for row in reader:
#             words = row[1].split(',')
#             # print(words)
#
#             N_counter = 0
#             V_counter = 0
#             J_counter = 0
#             P_counter = 0
#             R_counter = 0
#             EXCL_counter = 0
#             QUE_counter = 0
#             CL_counter = 0
#             sw_counter = 0
#             name_counter = 0
#             n_counter = 0
#
#             for word in words:
#                 if word == "N" or word == "N ":
#                     N_counter += 1
#                 elif word == "V" or word == "V ":
#                     V_counter += 1
#                 elif word == "J" or word == "J ":
#                     J_counter += 1
#                 elif word == "P" or word == "P ":
#                     P_counter += 1
#                 elif word == "R" or word == "R ":
#                     R_counter += 1
#                 elif word == "EXCL" or word == "EXCL ":
#                     EXCL_counter += 1
#                 elif word == "QUE" or word == "QUE ":
#                     QUE_counter += 1
#                 elif word == "CL" or word == "CL ":
#                     CL_counter += 1
#                 elif word == "sw" or word == "sw ":
#                     sw_counter += 1
#                 elif word == "name" or word == "name ":
#                     name_counter += 1
#                 elif word == "n" or word == "n":
#                     n_counter += 1
#
#             # print(
#             #     N_counter,
#             #     V_counter,
#             #     J_counter,
#             #     P_counter,
#             #     R_counter,
#             #     EXCL_counter,
#             #     QUE_counter,
#             #     CL_counter,
#             #     sw_counter,
#             #     name_counter,
#             #     n_counter)
#
#             vector = []
#
#             vector.extend((N_counter,
#                            V_counter,
#                            J_counter,
#                            P_counter,
#                            R_counter,
#                            EXCL_counter,
#                            QUE_counter,
#                            CL_counter,
#                            sw_counter,
#                            name_counter,
#                            n_counter))
#
#             #print(vector)
#             logging.info('Starting Vector')
#
#             ##### Aufschreiben der Vektoren in neue .csv #####
#             with open('POS_Testdaten_vec.csv', 'a') as f3:
#                 writer = csv.writer(f3, delimiter=';')
#                 str1 = ','.join(str(v) for v in vector)
#                 writer.writerow([row[0], row[1], str1, row[2]])     #Ausgangstext, POS-Tags, Vektoren, Cyberbullying (1/0)
#             logging.info('Vector: END')
#
# train_data()

##### Methode kann einen einzelnen Satz zu Testzwecken komplett bearbeiten und schreibt das Ergebnis in eine neue Date
# Input: Siehe Variable ganz oben
# def process_single_tweet(tweet):
#
#     # 1. clean tweet
#     clean_tweet = prepare_POS_text(tweet)
#
#     #2. pos_tag tweet
#
#     test_postags = nltk.pos_tag(clean_tweet)
#
#     #3. tag special words
#     special_tags = ','.join((POS_specials_all(test_postags)))
#     tags_split = special_tags.split(",")
#
#     #4. build vector
#     vector = build_vector(tags_split)
#
#
#     # with open('POS_method/POS_Testdaten_compare.csv', 'a') as c:
#     #     writer2 = csv.writer(c, delimiter=';')
#     #     writer2.writerow([tweet, tags_split, vector])
#     return vector
#
# print(process_single_tweet(text))