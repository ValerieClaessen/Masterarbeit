import nltk
import csv
import pickle
from nltk import word_tokenize
from nltk.corpus import stopwords
#nltk.download()

swearword_tag = "sw"
text = "I hate my fucking ugly friend who is called Lisa Marie Schuster!!!!"


def prepare_POS_text(row):
    tokens = word_tokenize(row)
    stop_words = set(stopwords.words('english'))
    words = [word for word in tokens if word.isalpha()] #auf alphanumerische Zeichen prüfen
    words = [w for w in words if not w in stop_words]   #Stopworte entfernen
    return words



tokens = nltk.word_tokenize(text)   #tokenizing

test_tags= nltk.pos_tag(prepare_POS_text(text)) #POS-tagging




def POS_specials_all(pos_tags):
    pos_tags_man = []

    for tag in pos_tags:
        written = False
        f = open('POS_method/list.txt', 'r')
        for line in f:
            if tag[0].lower() == line.lower().strip():
                to_list = list(tag)
                to_list[1] = to_list[1] + "<sw>"
                tag1 = tuple(to_list)
                pos_tags_man.append(tag1[1])
                written = True
        f1 = open('POS_method/first-names.txt', 'r')
        for line in f1:
            if tag[0].lower() == line.lower().strip():
                to_list = list(tag)
                to_list[1] = to_list[1] + "<fn>"
                tag2 = tuple(to_list)
                pos_tags_man.append(tag2[1])
                written = True

        f2 = open('POS_method/names.txt', 'r')
        for line in f2:
            if tag[0].lower() == line.lower().strip() and written == False: #wichtig: Vornamen werden Nachnamen bevorzugt
                to_list = list(tag)
                to_list[1] = to_list[1] + "<n>"
                tag3 = tuple(to_list)
                pos_tags_man.append(tag3[1])
                written = True

        f3 = open('POS_method/middle-names.txt', 'r')
        for line in f3:
            if tag[0].lower() == line.lower().strip() and written == False:  # wichtig: Vornamen werden Nachnamen bevorzugt
                to_list = list(tag)
                to_list[1] = to_list[1] + "<mn>"
                tag4 = tuple(to_list)
                pos_tags_man.append(tag4[1])
                written = True

        f4 = open('POS_method/negative-words.txt', 'r')
        for line in f4:
            if tag[0].lower() == line.lower().strip() and written == False:  # wichtig: Vornamen werden Nachnamen bevorzugt
                to_list = list(tag)
                to_list[1] = to_list[1] + "<nw>"
                tag5 = tuple(to_list)
                pos_tags_man.append(tag5[1])
                written = True

        if written == False:
            pos_tags_man.append(tag[1])
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
            writer = csv.writer(f3, delimiter=',')
            str1 = ','.join(POS_specials_all(test_tags2))
            writer.writerow([str1])
            print(str1)







#print(POS_specials_all(test_tags))


#nltk.help.upenn_tagset('NNP')
#print(tokens)
#print(prepare_POS_text(text))