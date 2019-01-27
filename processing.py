import csv
import re
import codecs

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
        next(reader, None)  # skip header

        for row in reader:
            cyberbullying1.append(row[7])
            strength1.append(row[8])
            topic1.append(row[9])

    with codecs.open(file2, 'r', encoding="ascii", errors='ignore') as csvfile2:
        reader2 = csv.reader(csvfile2, delimiter=';')
        next(reader2, None)  # skip header

        for row in reader2:
            cyberbullying2.append(row[7])
            strength2.append(row[8])
            topic2.append(row[9])

        with open(file3, 'a') as csvfile3:
            writer = csv.writer(csvfile3, delimiter=';')

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
            for el in topic1:
                if el == 0:
                    topic3.append(0)
                else:
                    top1 = el
                    top1 = top1.replace(",", "")
                    top2 = topic2[x]
                    top2 = top2.replace(",", "")
                    topic3.append(top1 + " " + top2)
                x += 1

            #delete identical topics
            x = 0
            while x <= 4999:
                top = topic3[x]
                topic3[x] = ' '.join(unique_list(top.split()))
                x += 1

            print(topic3)

        x = 0
        for row in reader2:
            writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], cyberbullying3[x], strength3[x], topic3[x]])
            x += 1

#create_final_twitter_bullying("twitter_bullying_sabrina.csv", "twitter_bullying_valerie.csv", "twitter_bullying_annotated")

username = r'@\S*'                                                  # matches usernames starting with '@'
image = r'https\S*'                                                 # matches images and links (starting with 'https')
link = r'http\S*'                                                   # matches images and links (starting with 'http')
hashtag = r'#\S*'                                                   # matches hashtags (starting with '#'

def processing(file1, file2):
    with codecs.open(file1, 'r', encoding="ascii", errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            # twitter_bullying
            #usernames = re.findall(username, row[5])                # find all usernames
            #images = re.findall(image, row[5])                      # find all images / links
            #hashtags = re.findall(hashtag, row[5])
            #links = re.findall(link, row[5])

            # bullying_traces
            usernames = re.findall(username, row[2])
            images = re.findall(image, row[2])
            hashtags = re.findall(hashtag, row[2])
            links = re.findall(link, row[2])

            # customer_twitter
            # dialogText_196
            # dialogueText_301
            # dialogueText
            # supreme_conversation
            #usernames = re.findall(username, row[4])
            #images = re.findall(image, row[4])
            #hashtags = re.findall(hashtag, row[4])
            #links = re.findall(link, row[4])

            # labeled_data
            #usernames = re.findall(username, row[6])
            #images = re.findall(image, row[6])
            #hashtags = re.findall(hashtag, row[6])
            #links = re.findall(link, row[6])

            # twitter_hate_speech_classifier
            #usernames = re.findall(username, row[1])
            #images = re.findall(image, row[1])
            #hashtags = re.findall(hashtag, row[1])
            #links = re.findall(link, row[1])

            # movie_lines
            #usernames = re.findall(username, row[3])
            #images = re.findall(image, row[3])
            #hashtags = re.findall(hashtag, row[3])
            #links = re.findall(link, row[3])

            # twitter_bullying
            #row[5] = row[5].replace('RT', '')                       # delete 'RT'

            # bullying_traces
            row[2] = row[2].replace('RT', '')

            # customer_twitter
            # dialogText_196
            # dialogueText_301
            # dialogueText
            # supreme_conversation
            #row[4] = row[4].replace('RT', '')

            # labeled_data
            #row[6] = row[6].replace('RT', '')

            # twitter_hate_speech_classifier
            #row[1] = row[1].replace('RT', '')

            # movie_lines
            #row[3] = row[3].replace('RT', '')

            for name in usernames:
                # twitter_bullying
                #row[5] = row[5].replace(name, '')                   # delete usernames

                # bullying_traces
                row[2] = row[2].replace(name, '')

                # customer_twitter
                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                #row[4] = row[4].replace(name, '')

                # labeled_data
                #row[6] = row[6].replace(name, '')

                # twitter_hate_speech_classifier
                #row[1] = row[1].replace(name, '')

                # movie_lines
                #row[3] = row[3].replace(name, '')

            for pic in images:
                # twitter_bullying
                #row[5] = row[5].replace(pic, '')                    # delete images and links

                # bullying_traces
                row[2] = row[2].replace(pic, '')

                # customer_twitter
                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                #row[4] = row[4].replace(pic, '')

                # labeled_data
                #row[6] = row[6].replace(pic, '')

                # twitter_hate_speech_classifier
                #row[1] = row[1].replace(pic, '')

                # movie_lines
                #row[3] = row[3].replace(pic, '')

            for li in links:
                # twitter_bullying
                # row[5] = row[5].replace(li, '')                    # delete images and links

                # bullying_traces
                row[2] = row[2].replace(li, '')

                # customer_twitter
                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                # row[4] = row[4].replace(li, '')

                # labeled_data
                # row[6] = row[6].replace(li, '')

                # twitter_hate_speech_classifier
                # row[1] = row[1].replace(li, '')

                # movie_lines
                # row[3] = row[3].replace(li, '')


            for tag in hashtags:
                # twitter_bullying
                #row[5] = re.sub(r"(\w)([A-Z][a-z])+", r"\1 \2", row[5])     # insert space before capital letter (but avoid for allcaps words)

                # bullying_traces
                row[2] = re.sub(r"(\w)([A-Z][a-z])+", r"\1 \2", row[2])

                # customer_twitter
                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                #row[4] = re.sub(r"(\w)([A-Z][a-z])+", r"\1 \2", row[4])

                # labeled_data
                #row[6] = re.sub(r"(\w)([A-Z][a-z])+", r"\1 \2", row[6])

                # twitter_hate_speech_classifier
                #row[1] = re.sub(r"(\w)([A-Z][a-z])+", r"\1 \2", row[1])

                # movie_lines
                #row[3] = re.sub(r"(\w)([A-Z][a-z])+", r"\1 \2", row[3])

            # twitter_bullying
            #row[5] = row[5].replace('#', '')                        # delete hashtag sign (so hashtags themselves count as words with sentiment)

            # bullying_traces
            row[2] = row[2].replace('#', '')

            # customer_twitter
            # dialogText_196
            # dialogueText_301
            # dialogueText
            # supreme_conversation
            #row[4] = row[4].replace('#', '')

            # labeled_data
            #row[6] = row[6].replace('#', '')

            # twitter_hate_speech_classifier
            #row[1] = row[1].replace('#', '')

            # movie_lines
            #row[3] = row[3].replace('#', '')

            with open(file2, 'a') as csvfile:  # saving processed tweets to new file
                writer = csv.writer(csvfile, delimiter=';')

                # twitter_bullying
                #writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])

                # bullying_traces
                # customer_twitter
                # labeled_data
                writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

                # twitter_hate_speech_classifier
                # movie_lines
                #writer.writerow([row[0], row[1], row[2], row[3]])

                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                #writer.writerow([row[0], row[1], row[2], row[3], row[4]])

#twitter_bullying
#processing("twitter_bullying_annotated.csv", "twitter_bullying_processed.csv")

#bullying_traces
processing("bullying_traces_cleaned2.csv", "bullying_traces_processed.csv")

# customer_twitter
#processing("customer_twitter_cleaned.csv", "customer_twitter_processed.csv")

# labeled_data
#processing("labeled_data_delim_cleaned.csv", "labeled_data_processed.csv")

# twitter_hate_speech_classifier
#processing("twitter-hate-speech-classifier_cleaned2.csv", "twitter_hate_speech_classifier_processed.csv")

# dialogText_196
#processing("dialogueText_196_clean.csv", "dialogueText_196_processed.csv")

# dialogueText_301
#processing("dialogueText_301_clean.csv", "dialogueText_301_processed.csv")

# dialogueText
#processing("dialogueText_clean.csv", "dialogueText_processed.csv")

# movie_lines
#processing("movie_lines_clean.csv", "movie_lines_processed.csv")

# supreme_conversation
#processing("supreme_conversation_data_header_clean.csv", "supreme_conversation_processed.csv")

print("done")

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
                    # twitter_bullying
                    #if em in row[5]:
                    #    found_smiley = True

                    # bullying_traces
                    if em in row[2]:
                        found_smiley = True

                    # customer_twitter
                    # dialogText_196
                    # dialogueText_301
                    # dialogueText
                    # supreme_conversation
                    #if em in row[4]:
                    #    found_smiley = True

                    # labeled_data
                    #if em in row[6]:
                    #    found_smiley = True

                    # twitter_hate_speech_classifier
                    #if em in row[1]:
                    #    found_smiley = True

                    # movie_lines
                    #if em in row[3]:
                    #    found_smiley = True

                if found_smiley == False:
                    # twitter_bullying
                    #row[5] = row[5].replace(el, "<" + el + ">")                         # mark smileys with "<smiley>"

                    # bullying_traces
                    row[2] = row[2].replace(el, "<" + el + ">")

                    # customer_twitter
                    # dialogText_196
                    # dialogueText_301
                    # dialogueText
                    # supreme_conversation
                    #row[4] = row[4].replace(el, "<" + el + ">")

                    # labeled_data
                    #row[6] = row[6].replace(el, "<" + el + ">")

                    # twitter_hate_speech_classifier
                    #row[1] = row[1].replace(el, "<" + el + ">")

                    # movie_lines
                    #row[3] = row[3].replace(el, "<" + el + ">")

            with open(file3, 'a') as csvfile:  # saving processed tweets to new file
                writer = csv.writer(csvfile, delimiter=';')

                # twitter_bullying
                #writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])

                # bullying_traces
                # customer_twitter
                # labeled_data
                writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

                # twitter_hate_speech_classifier
                # movie_lines
                #writer.writerow([row[0], row[1], row[2], row[3]])

                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                # writer.writerow([row[0], row[1], row[2], row[3], row[4]])

# twitter_bullying
#processing_smileys("twitter_bullying_processed.csv", "smileys2.txt", "twitter_bullying_processed2.csv")

#bullying_traces
processing_smileys("bullying_traces_processed.csv", "smileys2.txt", "bullying_traces_processed2.csv")

# customer_twitter
#processing_smileys("customer_twitter_processed.csv", "smileys2.txt", "customer_twitter_processed2.csv")

# labeled_data
#processing_smileys("labeled_data_processed.csv", "smileys2.txt", "labeled_data_processed2.csv")

# twitter_hate_speech_classifier
#processing_smileys("twitter_hate_speech_classifier_processed.csv", "smileys2.txt", "twitter_hate_speech_classifier_processed2.csv")

# dialogueText_196
#processing_smileys("dialogueText_196_processed.csv", "smileys2.txt", "dialogueText_196_processed2.csv")

# dialogueText_301
#processing_smileys("dialogueText_301_processed.csv", "smileys2.txt", "dialogueText_301_processed2.csv")

# dialogueText
#processing_smileys("dialogueText_processed.csv", "smileys2.txt", "dialogueText_processed2.csv")

# movie_lines
#processing_smileys("movie_lines_processed.csv", "smileys2.txt", "movie_lines_processed2.csv")

# supreme_conversation
#processing_smileys("supreme_conversation_processed.csv", "smileys2.txt", "supreme_conversation_processed2.csv")

print("done2")

def processing_abbreviations(file1, file2, file3):
    with open(file2) as f:
        reader2 = csv.reader(f, delimiter=";")
        abbreviations = {rows[0]: rows[1] for rows in reader2}

    with codecs.open(file1, 'r', encoding="ascii", errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        for row in reader:
            for key, value in abbreviations.items():
                # twitter_bullying
                #row[5] = row[5].replace(key, value)

                # bullying_traces
                row[2] = row[2].replace(key, value)

                # customer_twitter
                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                #row[4] = row[4].replace(key, value)

                # labeled_data
                #row[6] = row[6].replace(key, value)

                # twitter_hate_speech_classifier
                #row[1] = row[1].replace(key, value)

                # movie_lines
                #row[3] = row[3].replace(key, value)

            with open(file3, 'a') as csvfile:  # saving processed tweets to new file
                writer = csv.writer(csvfile, delimiter=';')

                # twitter_bullying
                #writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])

                # bullying_traces
                # customer_twitter
                # labeled_data
                writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

                # twitter_hate_speech_classifier
                # movie_lines
                #writer.writerow([row[0], row[1], row[2], row[3]])

                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                # writer.writerow([row[0], row[1], row[2], row[3], row[4]])

# twitter_bullying
#processing_abbreviations("twitter_bullying_processed2.csv", "abbreviations.csv", "twitter_bullying_final.csv")

#bullying_traces
processing_abbreviations("bullying_traces_processed2.csv", "abbreviations.csv", "bullying_traces_final.csv")

# customer_twitter
#processing_abbreviations("customer_twitter_processed2.csv", "abbreviations.csv", "customer_twitter_final.csv")

# labeled_data
#processing_abbreviations("labeled_data_processed2.csv", "abbreviations.csv", "labeled_data_final.csv")

# twitter_hate_speech_classifier
#processing_abbreviations("twitter_hate_speech_classifier_processed2.csv", "abbreviations.csv", "twitter_hate_speech_classifier_final.csv")

# dialogueText_196
#processing_abbreviations("dialogueText_196_processed2.csv", "abbreviations.csv", "dialogueText_196_final.csv")

# dialogueText_301
#processing_abbreviations("dialogueText_301_processed2.csv", "abbreviations.csv", "dialogueText_301_final.csv")

# dialogueText
#processing_abbreviations("dialogueText_processed2.csv", "abbreviations.csv", "dialogueText_final.csv")

# movie_lines
#processing_abbreviations("movie_lines_processed2.csv", "abbreviations.csv", "movie_lines_final.csv")

# supreme_conversation
#processing_abbreviations("supreme_conversation_processed2.csv", "abbreviations.csv", "supreme_conversation_final.csv")

print("done3")