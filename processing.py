import csv
import re
import codecs

username = r'@\S*'                                                  # matches usernames starting with '@'
image = r'https\S*'                                                 # matches images and links (starting with 'https')
hashtag = r'#\S*'                                                   # matches hashtags (starting with '#'

def processing(file1, file2):
    with codecs.open(file1, 'r', encoding="ascii", errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            usernames = re.findall(username, row[5])                # find all usernames
            images = re.findall(image, row[5])                      # find all images / links
            hashtags = re.findall(hashtag, row[5])

            row[5] = row[5].replace('RT', '')                       # delete 'RT'

            for name in usernames:
                row[5] = row[5].replace(name, '')                   # delete usernames

            for pic in images:
                row[5] = row[5].replace(pic, '')                    # delete images and links

            for tag in hashtags:
                row[5] = re.sub(r"(\w)([A-Z][a-z])+", r"\1 \2", row[5])     # insert space before capital letter (but avoid for allcaps words)

            row[5] = row[5].replace('#', '')                        # delete hashtag sign (so hashtags themselves count as words with sentiment)


            with open(file2, 'a') as csvfile:  # saving processed tweets to new file
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])

#processing("twitter_bullying_test.csv", "twitter_bullying_test_processed.csv")

def remove_duplicate_smileys(file):
    smileys = open(file, "r")
    smiley_list = []

    file2 = open('smileys2.txt', 'w')
    for line in smileys:
        smiley_in_list = False
        for el in smiley_list:
            if line == el:
                smiley_in_list = True
        if smiley_in_list == False:
            file2.write(line)
        smiley_list.append(line)

#remove_duplicate_smileys("smileys.txt")

def processing_smileys(file1, file2, file3):
    with codecs.open(file1, 'r', encoding="ascii", errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        smiley_list = []
        smileys = open(file2, 'r')
        for smiley in smileys:
            smiley_list.append(smiley.strip())
        smiley_list.sort(key=len, reverse=True)                                     # sort smileys (longest first)

        found_smiley_list = []
        for el in smiley_list:
            found_smiley_list.append("<" + el + ">")

        for row in reader:                                                          # check if smiley would be part of an already marked smiley
            for el in smiley_list:
                found_smiley = False
                for em in found_smiley_list:
                    if em in row[5]:
                        found_smiley = True

                if found_smiley == False:
                    row[5] = row[5].replace(el, "<" + el + ">")                         # mark smileys with "<smiley>"

            with open(file3, 'a') as csvfile:  # saving processed tweets to new file
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])

#processing_smileys("twitter_bullying_test_processed.csv", "smileys2.txt", "twitter_bullying_test_processed2.csv")

def processing_abbreviations(file1, file2, file3):
    with open(file2) as f:
        reader2 = csv.reader(f, delimiter=";")
        abbreviations = {rows[0]: rows[1] for rows in reader2}

    with codecs.open(file1, 'r', encoding="ascii", errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        for row in reader:
            for key, value in abbreviations.items():
                row[5] = row[5].replace(key, value)

            with open(file3, 'a') as csvfile:  # saving processed tweets to new file
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])

#processing_abbreviations("twitter_bullying_test_processed2.csv", "abbreviations.csv", "twitter_bullying_test_processed3.csv")

# method to remove duplicates in a string
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

# Making the final version of the annotated tweets
# Only those tweets contain cyberbullying, which were marked "1" by both annotators
# If different strengths were selected, choose the weaker one
# All topics selected by the annotators will be topics in the final file
def create_final_twitter_bullying(file1, file2, file3):
    cyberbullying1 = []
    strength1 = []
    topic1 = []
    cyberbullying2 = []
    strength2 = []
    topic2 = []
    cyberbullying3 = []
    strength3 = []
    topic3 = []

    with codecs.open(file1, 'r', encoding="ascii", errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        for row in reader:
            cyberbullying1.append(row[7])
            strength1.append(row[8])
            topic1.append(row[9])

    with codecs.open(file2, 'r', encoding="ascii", errors='ignore') as csvfile:
        reader2 = csv.reader(csvfile, delimiter=';')

        for row in reader2:
            cyberbullying2.append(row[7])
            strength2.append(row[8])
            topic2.append(row[9])

        with open(file3, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            x = 0
            for el in cyberbullying1:
                if el == 1 and cyberbullying2[x] == 1:
                    print("1")
                    cyberbullying3.append(1)
                else:
                    cyberbullying3.append(0)
                x += 1

            x = 0
            for el in strength1:
                if el <= strength2[x]:
                    strength3.append(el)
                else:
                    strength3.append(strength2[x])
                x += 1

            x = 0
            for el in topic3:
                top1 = el
                top1 = top1.replace(",", "")
                top2 = topic2[x]
                top2 = top2.replace(",", "")
                topic3.append(top1 + " " + top2)
                x += 1

            #delete identical topics
            while x <= 4999:
                top = topic3[x]
                topic3[x] = ' '.join(unique_list(top.split()))

#create_final_twitter_bullying("twitter_bullying_sabrina.csv", "twitter_bullying_valerie.csv", "twitter_bullying_final")