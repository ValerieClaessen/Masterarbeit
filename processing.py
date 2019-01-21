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

processing("twitter_bullying_test.csv", "twitter_bullying_test_processed.csv")

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

remove_duplicate_smileys("smileys.txt")

def processing_smileys(file1, file2, file3):
    with codecs.open(file1, 'r', encoding="ascii", errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        smiley_list = []
        smileys = open(file2, 'r')
        for smiley in smileys:
            smiley_list.append(smiley.strip())

        for row in reader:
            for el in smiley_list:
                row[5] = row[5].replace(el, "+" + el + "+")                         # mark smileys with "+smiley+"

            with open(file3, 'a') as csvfile:  # saving processed tweets to new file
                writer = csv.writer(csvfile, delimiter=';')
                writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])

processing_smileys("twitter_bullying_test_processed.csv", "smileys2.txt", "twitter_bullying_test_processed2.csv")

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

processing_abbreviations("twitter_bullying_test_processed2.csv", "abbreviations.csv", "twitter_bullying_test_processed3.csv")

