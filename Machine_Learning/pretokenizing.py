from nltk.corpus import words
from nltk.stem import PorterStemmer
from nltk.corpus import brown
import csv
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re


#nltk.download()

ps = PorterStemmer()


with open('prestem.csv', mode='w') as stem_file:
    stem_writer = csv.writer(stem_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


    for word in words.words():
            stem_writer.writerow([word, ps.stem(word)])
            #print(word, ps.stem(word))

with open('prestem.csv', mode='a') as stem_file:
    stem_writer = csv.writer(stem_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


    for word in brown.words():
        pattern = False
        if re.match(r"[0-9]", word):
            print("print", word)
        else:
            stem_writer.writerow([word, ps.stem(word)])



with open('list.txt', newline='') as f:
        curses = []
        for x in f:
            curses.append(x.rstrip())
        print(curses)

with open('prestem.csv', mode='a') as curse_file:
    curse_writer = csv.writer(curse_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


    for word in curses:
            curse_writer.writerow([word, ps.stem(word)])
            print(word, ps.stem(word))


with open('prestem.csv','r') as in_file, open('prestem_no_dup.csv','w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    for line in in_file:
        if line in seen: continue # skip duplicate

        seen.add(line)
        out_file.write(line)

