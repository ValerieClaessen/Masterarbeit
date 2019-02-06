import nltk
import csv
import pickle
from nltk import word_tokenize
from nltk.corpus import stopwords
#nltk.download()

swearword_tag = "sw"
text = "I hate my fucking ugly friend who is called Lisa Marie Schuster!!!!"
upper_test = "HAfTgggE"


def prepare_POS_text(row):
    tokens = word_tokenize(row)
    stop_words = set(stopwords.words('english'))
    #words = [word for word in tokens if word.isalpha()] #auf alphanumerische Zeichen prüfen
    words = [w for w in tokens if not w in stop_words]   #Stopworte entfernen
    return words



tokens = nltk.word_tokenize(text)   #tokenizing

test_tags= nltk.pos_tag(prepare_POS_text(text)) #POS-tagging

# def check_upper_char(c):
#     if c >= 'A' and c <= 'Z':
#         return True
#     else:
#         return False

def check_upper_word(word):
    char_count = 0
    for char in word:
        if char >= 'A' and char <= 'Z':
            char_count += 1
    return char_count




# def POS_specials_all(pos_tags):
#     pos_tags_man = []
#     pos_tags_new = []
#     upper_check = []
#     for tag in pos_tags:
#         if tag[1] == "NNP" or tag[1] == "NNS" or tag[1] == "NN" or tag[1] == "NNPS":
#             new_pos = list(tag)
#             new_pos[1] = "N"
#             new_tag = tuple(new_pos)
#             pos_tags_new.append(new_tag[1])
#         elif tag[1] == "VBG" or tag[1] == "VBP" or tag[1] == "VB" or tag[1] == "VBN" or tag[1] == "VBZ" or tag[1] == "VBD":
#             new_pos = list(tag)
#             new_pos[1] = "V"
#             new_tag = tuple(new_pos)
#             pos_tags_new.append(new_tag[1])
#         elif tag[1] == "JJ" or tag[1] == "JJR" or tag[1] == "JJS":
#             new_pos = list(tag)
#             new_pos[1] = "J"
#             new_tag = tuple(new_pos)
#             pos_tags_new.append(new_tag[1])
#         elif tag[1] == "PDT" or tag[1] == "POS" or tag[1] == "PRP" or tag[1] == "PRP$":
#             new_pos = list(tag)
#             new_pos[1] = "P"
#             new_tag = tuple(new_pos)
#             pos_tags_new.append(new_tag[1])
#         elif tag[1] == "RB" or tag[1] == "RBR" or tag[1] == "RBS" or tag[1] == "RP":
#             new_pos = list(tag)
#             new_pos[1] = "R"
#             new_tag = tuple(new_pos)
#             pos_tags_new.append(new_tag[1])
#         elif tag[0] == "!" :
#             new_pos = list(tag)
#             new_pos[1] = "EXCL"
#             new_tag = tuple(new_pos)
#             pos_tags_new.append(new_tag[1])
#         elif tag[0] == "?" :
#             new_pos = list(tag)
#             new_pos[1] = "QUE"
#             new_tag = tuple(new_pos)
#             pos_tags_new.append(new_tag[1])
#         else:
#             pos_tags_new.append(tag[1])
#
#
#     #for tag in pos_tags:
#         if check_upper_word(tag[0]) >= 2:
#             upper = list(tag)
#             upper[1] = upper[1] + "<CL>"
#             tag1 = tuple(upper)
#             upper_check.append(tag1[1])
#         else:
#             upper_check.append(tag[1])
#
#
#     #for tag in pos_tags:
#         written = False
#         f = open('POS_method/list.txt', 'r')
#         for line in f:
#             if tag[0].lower() == line.lower().strip():
#                 to_list = list(tag)
#                 to_list[1] = to_list[1] + "<sw>"
#                 tag1 = tuple(to_list)
#                 pos_tags_man.append(tag1[1])
#                 written = True
#         f1 = open('POS_method/first-names.txt', 'r')
#         for line in f1:
#             if tag[0].lower() == line.lower().strip():
#                 to_list = list(tag)
#                 to_list[1] = to_list[1] + "<fn>"
#                 tag2 = tuple(to_list)
#                 pos_tags_man.append(tag2[1])
#                 written = True
#
#         f2 = open('POS_method/names.txt', 'r')
#         for line in f2:
#             if tag[0].lower() == line.lower().strip() and written == False: #wichtig: Vornamen werden Nachnamen bevorzugt
#                 to_list = list(tag)
#                 to_list[1] = to_list[1] + "<n>"
#                 tag3 = tuple(to_list)
#                 pos_tags_man.append(tag3[1])
#                 written = True
#
#         f3 = open('POS_method/middle-names.txt', 'r')
#         for line in f3:
#             if tag[0].lower() == line.lower().strip() and written == False:  # wichtig: Vornamen werden Nachnamen bevorzugt
#                 to_list = list(tag)
#                 to_list[1] = to_list[1] + "<mn>"
#                 tag4 = tuple(to_list)
#                 pos_tags_man.append(tag4[1])
#                 written = True
#
#         f4 = open('POS_method/negative-words.txt', 'r')
#         for line in f4:
#             if tag[0].lower() == line.lower().strip() and written == False:  # wichtig: Vornamen werden Nachnamen bevorzugt
#                 to_list = list(tag)
#                 to_list[1] = to_list[1] + "<nw>"
#                 tag5 = tuple(to_list)
#                 pos_tags_man.append(tag5[1])
#                 written = True
#
#         if written == False:
#             pos_tags_man.append(tag[1])
#
#     return pos_tags_man

def POS_specials_all(pos_tags):
    pos_tags_man = []
    pos_tags_new = []
    upper_check = []
    for tag in pos_tags:
        if tag[1] == "NNP" or tag[1] == "NNS" or tag[1] == "NN" or tag[1] == "NNPS":
            new_pos = list(tag)
            new_pos[1] = "N"

        elif tag[1] == "VBG" or tag[1] == "VBP" or tag[1] == "VB" or tag[1] == "VBN" or tag[1] == "VBZ" or tag[1] == "VBD":
            new_pos = list(tag)
            new_pos[1] = "V"

        elif tag[1] == "JJ" or tag[1] == "JJR" or tag[1] == "JJS":
            new_pos = list(tag)
            new_pos[1] = "J"

        elif tag[1] == "PDT" or tag[1] == "POS" or tag[1] == "PRP" or tag[1] == "PRP$":
            new_pos = list(tag)
            new_pos[1] = "P"

        elif tag[1] == "RB" or tag[1] == "RBR" or tag[1] == "RBS" or tag[1] == "RP":
            new_pos = list(tag)
            new_pos[1] = "R"

        elif tag[0] == "!" :
            new_pos = list(tag)
            new_pos[1] = "EXCL"

        elif tag[0] == "?" :
            new_pos = list(tag)
            new_pos[1] = "QUE"

        else:
            new_pos = list(tag)
            new_pos[1] = tag[1]


    #for tag in pos_tags:
        if check_upper_word(tag[0]) >= 2:
            #new_pos = list(tag)
            new_pos[1] = new_pos[1] + "<CL>"
        else:
            #new_pos = list(tag)
            new_pos[1] = new_pos[1]


    #for tag in pos_tags:
        written = False
        f = open('POS_method/list.txt', 'r')
        for line in f:
            if tag[0].lower() == line.lower().strip():
                #new_pos = list(tag)
                new_pos[1] = new_pos[1] + "<sw>"

                written = True
                break
        f1 = open('POS_method/first-names.txt', 'r')
        for line in f1:
            if tag[0].lower() == line.lower().strip():
                #new_pos = list(tag)
                new_pos[1] = new_pos[1] + "<fn>"

                written = True
                break
        f2 = open('POS_method/names.txt', 'r')
        for line in f2:
            if tag[0].lower() == line.lower().strip() and written == False: #wichtig: Vornamen werden Nachnamen bevorzugt
                #new_pos = list(tag)
                new_pos[1] = new_pos[1] + "<n>"

                written = True
                break
        f3 = open('POS_method/middle-names.txt', 'r')
        for line in f3:
            if tag[0].lower() == line.lower().strip() and written == False:  # wichtig: Vornamen werden Nachnamen bevorzugt
                #new_pos = list(tag)
                new_pos[1] = new_pos[1] + "<mn>"

                written = True
                break
        f4 = open('POS_method/negative-words.txt', 'r')
        for line in f4:
            if tag[0].lower() == line.lower().strip() and written == False:  # wichtig: Vornamen werden Nachnamen bevorzugt
                #new_pos = list(tag)
                new_pos[1] = new_pos[1] + "<nw>"

                written = True
                break
        #if written == False:
        #    #new_pos = list(tag)
        #    new_pos[1] = new_pos[1]

        new_tag = tuple(new_pos)
        pos_tags_man.append(new_tag[1])


    return pos_tags_man


with open('POS_method/POS_Testdaten.csv', 'r') as f2:
    reader = csv.reader(f2, delimiter = ";")
    for row in reader:
        #print(row[0])
        text2 = ""
        cleaned = prepare_POS_text(row[0])
        #text2 = nltk.word_tokenize(row[0])
        test_tags2 = []
        test_tags2 = nltk.pos_tag(cleaned)

        #with open('POS_tagged_data.csv', 'w') as w:
        #    w.write(POS_specials_all(test_tags2))


        #print(str1)
        with open('POS_method/POS_Testdaten_test.csv', 'a') as f3:
            writer = csv.writer(f3, delimiter=';')
            str1 = ','.join(POS_specials_all(test_tags2))
            writer.writerow([row[0], str1])
            print(str1)







#print(POS_specials_all(test_tags))


#nltk.help.upenn_tagset('NNP')
#print(tokens)
#print(prepare_POS_text(text))