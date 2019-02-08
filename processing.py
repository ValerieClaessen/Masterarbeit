import csv
import re
import codecs
from spellchecker_autocorrect import correctSentence

# method to remove duplicates in a string
def unique_list(l):
    """
    This method is used in create_final_twitter_bullying() to delete identical topics assigned to a tweet, which is the case
    whenever both annotators assigned the same topic.
    """

    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

# function to make the final version of the annotated tweets of our dataset
def create_final_twitter_bullying(file1, file2, file3):
    """
    The final version will be annotated as follows:
    - only those tweets contain cyberbullying, which were marked "1" by both annotators
    - if different strengths were selected, choose the weaker one
    - all topics selected by the annotators will be topics in the final file
    """

    cyberbullying1 = []             # list of cyberbullying values assigned by the 1st annotator
    strength1 = []                  # list of cyberbullying strength / type values assigned by the 1st annotator
    topic1 = []                     # list of topics assigned by the 1st annotator
    cyberbullying2 = []             # list of cyberbullying values assigned by the 2nd annotator
    strength2 = []                  # list of cyberbullying strength / type values assigned by the 2nd annotator
    topic2 = []                     # list of topics assigned by the 2nd annotator
    cyberbullying3 = []             # list of final cyberbullying values
    strength3 = []                  # list of final cyberbullying strength / type values
    topic3 = []                     # list of merged topics

    # analyse annotated dataset of 1st annotator
    with codecs.open(file1, 'r', encoding="ascii", errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)  # skip header

        # append assigned cyberbullying, strengths and topics of each tweet to the lists
        for row in reader:
            cyberbullying1.append(row[7])
            strength1.append(row[8])
            topic1.append(row[9])

    # analyse annotated dataset of 2nd annotator
    with codecs.open(file2, 'r', encoding="ascii", errors='ignore') as csvfile2:
        reader2 = csv.reader(csvfile2, delimiter=';')
        next(reader2, None)  # skip header

        # append assigned cyberbullying, strengths and topics of each tweet to the lists
        for row in reader2:
            cyberbullying2.append(row[7])
            strength2.append(row[8])
            topic2.append(row[9])

    #print(cyberbullying1)
    #print(cyberbullying2)
    #print(strength1)
    #print(strength2)
    #print(topic1)
    #print(topic2)

    # estimate final values based on the values assigned by both annotators
    with codecs.open(file2, 'r', encoding="ascii", errors='ignore') as csvfile4:
        reader3 = csv.reader(csvfile4, delimiter=';')
        next(reader3, None)  # skip header

        with open(file3, 'a') as csvfile3:
            writer = csv.writer(csvfile3, delimiter=';')

            # only if both annotators labeled the tweet as cyberbullying (1) will the final value be 1
            x = 0
            for el in cyberbullying1:
                if el == 1 and cyberbullying2[x] == 1:
                    cyberbullying3.append("1")
                elif el == "1" and cyberbullying2[x] == "1":
                    cyberbullying3.append("1")
                else:
                    cyberbullying3.append("0")
                x += 1

            #print(cyberbullying3)

            # the weakest strength assigned by one of the annotators will be the final strength value
            # if one of the annotators labeled the tweet as no cyberbullying, the strength value will automatically be 0
            x = 0
            for el in strength1:
                if el <= strength2[x]:
                    strength3.append(el)
                else:
                    strength3.append(strength2[x])
                x += 1

            #print(strength3)

            # all topics assinged by both annotators will be topics in the final annotation
            x = 0
            for el in topic1:
                top1 = el
                top1 = top1.replace(",", "")        # delete comma between topics
                top2 = topic2[x]
                top2 = top2.replace(",", "")

                # if one of the annotators labeled the tweet as no cyerbullying, all topics assigned by the other annotator will be ignored
                if top1 == 0 or top1 == "0":
                    topic3.append("0")
                elif top2 == 0 or top2 == "0":
                    topic3.append("0")
                else:
                    topic3.append(top1 + " " + top2)    # append topics assigned by 1st and 2nd annotator
                x += 1

            # delete identical topics
            x = 0
            while x <= 4999:
                top = topic3[x]
                topic3[x] = ' '.join(unique_list(top.split()))
                x += 1

            #print(topic3)

            # write new values in a final file
            writer.writerow(['Tweet', 'Created at', 'User', 'ID', 'Reply to', 'Text', 'Hashtags', 'Cyberbullying', 'Strength', 'Topic'])
            x = 0
            for row in reader3:
                writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], cyberbullying3[x], strength3[x], topic3[x]])
                x += 1

#create_final_twitter_bullying("twitter_bullying_sabrina.csv", "twitter_bullying_valerie.csv", "twitter_bullying_annotated.csv")
#print("merged")

# regular expressions that will be used in processing()
username = r'@\S*'                                                  # matches usernames starting with '@'
image = r'https\S*'                                                 # matches images and links (starting with 'https')
link = r'http\S*'                                                   # matches images and links (starting with 'http')
hashtag = r'#\S*'                                                   # matches hashtags (starting with '#'

def processing(file1, file2):
    with codecs.open(file1, 'r', encoding="ascii", errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            # the column that is analysed is the one containing the utterance
            # depending on the dataset that will be processed the column that contains the utterance (e.g. row[5]) will be different

            # find all usernames, images, links and hashtags based on the regular expressions phrased above
            # twitter_bullying
            #usernames = re.findall(username, row[5]
            #images = re.findall(image, row[5])
            #hashtags = re.findall(hashtag, row[5])
            #links = re.findall(link, row[5])

            # bullying_traces
            #usernames = re.findall(username, row[2])
            #images = re.findall(image, row[2])
            #hashtags = re.findall(hashtag, row[2])
            #links = re.findall(link, row[2])

            # customer_twitter
            # dialogText_196
            # dialogueText_301
            # dialogueText
            # supreme_conversation
            usernames = re.findall(username, row[4])
            images = re.findall(image, row[4])
            hashtags = re.findall(hashtag, row[4])
            links = re.findall(link, row[4])

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

            # delete every occurence of "RT", indicating that a tweet is a retweet
            # twitter_bullying
            #row[5] = row[5].replace('RT', '')

            # bullying_traces
            #row[2] = row[2].replace('RT', '')

            # customer_twitter
            # dialogText_196
            # dialogueText_301
            # dialogueText
            # supreme_conversation
            row[4] = row[4].replace('RT', '')

            # labeled_data
            #row[6] = row[6].replace('RT', '')

            # twitter_hate_speech_classifier
            #row[1] = row[1].replace('RT', '')

            # movie_lines
            #row[3] = row[3].replace('RT', '')

            # delete all usernames found by the use of the regular expressions
            for name in usernames:
                # twitter_bullying
                #row[5] = row[5].replace(name, '')

                # bullying_traces
                #row[2] = row[2].replace(name, '')

                # customer_twitter
                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                row[4] = row[4].replace(name, '')

                # labeled_data
                #row[6] = row[6].replace(name, '')

                # twitter_hate_speech_classifier
                #row[1] = row[1].replace(name, '')

                # movie_lines
                #row[3] = row[3].replace(name, '')

            # delete all images and links (https) found by the use of the regular expressions
            for pic in images:
                # twitter_bullying
                #row[5] = row[5].replace(pic, '')

                # bullying_traces
                #row[2] = row[2].replace(pic, '')

                # customer_twitter
                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                row[4] = row[4].replace(pic, '')

                # labeled_data
                #row[6] = row[6].replace(pic, '')

                # twitter_hate_speech_classifier
                #row[1] = row[1].replace(pic, '')

                # movie_lines
                #row[3] = row[3].replace(pic, '')

            # delete all images and links (http) found by the use of the regular expressions
            for li in links:
                # twitter_bullying
                #row[5] = row[5].replace(li, '')

                # bullying_traces
                #row[2] = row[2].replace(li, '')

                # customer_twitter
                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                row[4] = row[4].replace(li, '')

                # labeled_data
                #row[6] = row[6].replace(li, '')

                # twitter_hate_speech_classifier
                #row[1] = row[1].replace(li, '')

                # movie_lines
                #row[3] = row[3].replace(li, '')

            # delete "#" before every hashtag found by the use of the regular expressions
            for tag in hashtags:

                # insert space before capital letter (but avoid for allcaps words) to seperate words in a hashtag consisting of multiple words
                # twitter_bullying
                #row[5] = re.sub(r"(\w)([A-Z][a-z])+", r"\1 \2", row[5])

                # bullying_traces
                #row[2] = re.sub(r"(\w)([A-Z][a-z])+", r"\1 \2", row[2])

                # customer_twitter
                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                row[4] = re.sub(r"(\w)([A-Z][a-z])+", r"\1 \2", row[4])

                # labeled_data
                #row[6] = re.sub(r"(\w)([A-Z][a-z])+", r"\1 \2", row[6])

                # twitter_hate_speech_classifier
                #row[1] = re.sub(r"(\w)([A-Z][a-z])+", r"\1 \2", row[1])

                # movie_lines
                #row[3] = re.sub(r"(\w)([A-Z][a-z])+", r"\1 \2", row[3])

            # delete hashtag sign (so hashtags themselves count as used words)
            # twitter_bullying
            #row[5] = row[5].replace('#', '')

            # bullying_traces
            #row[2] = row[2].replace('#', '')

            # customer_twitter
            # dialogText_196
            # dialogueText_301
            # dialogueText
            # supreme_conversation
            row[4] = row[4].replace('#', '')

            # labeled_data
            #row[6] = row[6].replace('#', '')

            # twitter_hate_speech_classifier
            #row[1] = row[1].replace('#', '')

            # movie_lines
            #row[3] = row[3].replace('#', '')

            # saving processed utterance in a new file together with all other columns
            with open(file2, 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')

                # depending on the processed dataset the number of columns will be different
                # twitter_bullying
                #writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])

                # bullying_traces
                # customer_twitter
                # labeled_data
                #writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

                # twitter_hate_speech_classifier
                # movie_lines
                #writer.writerow([row[0], row[1], row[2], row[3]])

                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                writer.writerow([row[0], row[1], row[2], row[3], row[4]])

#twitter_bullying
#processing("twitter_bullying_annotated.csv", "twitter_bullying_processed.csv")

#bullying_traces
#processing("bullying_traces_cleaned2.csv", "bullying_traces_processed.csv")

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

#print("done")

# function to remove duplicate smileys from smiley.txt that was merged from multiple sources
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
        smiley_list.sort(key=len, reverse=True)                         # sort smileys (longest first), so they will be marked first

        # create a list of all smileys with their marks (e.g. "<:)>") to be used in order to ignore already marked smileys
        # e.g. if ">:(" was already marked a "<>:(>", ":)" will no longer be marked, so we will avoid a marking such as "<><:(>>"
        found_smiley_list = []
        for el in smiley_list:
            found_smiley_list.append("<" + el + ">")

        # check if smiley would be part of an already marked smiley (found_smiley_list)
        for row in reader:
            # the column that is analysed is the one containing the utterance
            # depending on the dataset that will be processed the column that contains the utterance (e.g. row[5]) will be different

            for el in smiley_list:
                found_smiley = False
                for em in found_smiley_list:
                    # twitter_bullying
                    #if em in row[5]:
                    #    found_smiley = True

                    # bullying_traces
                    #if em in row[2]:
                    #    found_smiley = True

                    # customer_twitter
                    # dialogText_196
                    # dialogueText_301
                    # dialogueText
                    # supreme_conversation
                    if em in row[4]:
                        found_smiley = True

                    # labeled_data
                    #if em in row[6]:
                    #    found_smiley = True

                    # twitter_hate_speech_classifier
                    #if em in row[1]:
                    #    found_smiley = True

                    # movie_lines
                    #if em in row[3]:
                    #    found_smiley = True

                # mark smileys as "<smiley>"
                if found_smiley == False:
                    # twitter_bullying
                    #row[5] = row[5].replace(el, "<" + el + ">")

                    # bullying_traces
                    #row[2] = row[2].replace(el, "<" + el + ">")

                    # customer_twitter
                    # dialogText_196
                    # dialogueText_301
                    # dialogueText
                    # supreme_conversation
                    row[4] = row[4].replace(el, "<" + el + ">")

                    # labeled_data
                    #row[6] = row[6].replace(el, "<" + el + ">")

                    # twitter_hate_speech_classifier
                    #row[1] = row[1].replace(el, "<" + el + ">")

                    # movie_lines
                    #row[3] = row[3].replace(el, "<" + el + ">")

            # saving utterances with marked smileys in a new file together will all the other columns
            with open(file3, 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')

                # depending on the processed dataset the number of columns will be different
                # twitter_bullying
                #writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])

                # bullying_traces
                # customer_twitter
                # labeled_data
                #writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

                # twitter_hate_speech_classifier
                # movie_lines
                #writer.writerow([row[0], row[1], row[2], row[3]])

                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                writer.writerow([row[0], row[1], row[2], row[3], row[4]])

# twitter_bullying
#processing_smileys("twitter_bullying_processed.csv", "smileys2.txt", "twitter_bullying_processed2.csv")

#bullying_traces
#processing_smileys("bullying_traces_processed.csv", "smileys2.txt", "bullying_traces_processed2.csv")

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

#print("done2")

# function to dissolve all abbreviations used in the utterances
def processing_abbreviations(file1, file2, file3):
    with open(file2) as f:
        reader2 = csv.reader(f, delimiter=";")

        # create a dictionary that contains the abbreviations as the keys (row[0]) and the dissolved expression as the values (row[1])
        # from abbreviations.csv
        abbreviations = {rows[0]: rows[1] for rows in reader2}

    with codecs.open(file1, 'r', encoding="ascii", errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        for row in reader:
            # the column that is analysed is the one containing the utterance
            # depending on the dataset that will be processed the column that contains the utterance (e.g. row[5]) will be different

            # replace the abbreviation (key) with the dissolved expression (value)
            for key, value in abbreviations.items():
                # twitter_bullying
                #row[5] = row[5].replace(key, value)

                # bullying_traces
                #row[2] = row[2].replace(key, value)

                # customer_twitter
                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                row[4] = row[4].replace(key, value)

                # labeled_data
                #row[6] = row[6].replace(key, value)

                # twitter_hate_speech_classifier
                #row[1] = row[1].replace(key, value)

                # movie_lines
                #row[3] = row[3].replace(key, value)

            # saving utterances with dissolved abbreviations in a new file together with all the other columns
            with open(file3, 'a') as csvfile:  # saving processed tweets to new file
                writer = csv.writer(csvfile, delimiter=';')

                # depending on the processed dataset the number of columns will be different
                # twitter_bullying
                #writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])

                # bullying_traces
                # customer_twitter
                # labeled_data
                #writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

                # twitter_hate_speech_classifier
                # movie_lines
                #writer.writerow([row[0], row[1], row[2], row[3]])

                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                writer.writerow([row[0], row[1], row[2], row[3], row[4]])

# twitter_bullying
#processing_abbreviations("twitter_bullying_processed2.csv", "abbreviations.csv", "twitter_bullying_processed3.csv")

#bullying_traces
#processing_abbreviations("bullying_traces_processed2.csv", "abbreviations.csv", "bullying_traces_processed3.csv")

# customer_twitter
#processing_abbreviations("customer_twitter_processed2.csv", "abbreviations.csv", "customer_twitter_processed3.csv")

# labeled_data
#processing_abbreviations("labeled_data_processed2.csv", "abbreviations.csv", "labeled_data_processed3.csv")

# twitter_hate_speech_classifier
#processing_abbreviations("twitter_hate_speech_classifier_processed2.csv", "abbreviations.csv", "twitter_hate_speech_classifier_processed3.csv")

# dialogueText_196
#processing_abbreviations("dialogueText_196_processed2.csv", "abbreviations.csv", "dialogueText_196_processed3.csv")

# dialogueText_301
#processing_abbreviations("dialogueText_301_processed2.csv", "abbreviations.csv", "dialogueText_301_processed3.csv")

# dialogueText
#processing_abbreviations("dialogueText_processed2.csv", "abbreviations.csv", "dialogueText_processed3.csv")

# movie_lines
#processing_abbreviations("movie_lines_processed2.csv", "abbreviations.csv", "movie_lines_processed3.csv")

# supreme_conversation
#processing_abbreviations("supreme_conversation_processed2.csv", "abbreviations.csv", "supreme_conversation_processed3.csv")

#print("done3")

# function to use spellchecker_autocorrect on all utterances to correct the spelling
def autocorrect(file1, file2):
    with open(file1) as f:
        reader = csv.reader(f, delimiter=";")

        for row in reader:
            # the column that is analysed is the one containing the utterance
            # depending on the dataset that will be processed the column that contains the utterance (e.g. row[5]) will be different

            # correct the utterance
            # twitter_bullying
            #row[5] = correctSentence(row[5])

            # bullying_traces
            #row[2] = correctSentence(row[2])

            # customer_twitter
            # dialogText_196
            # dialogueText_301
            # dialogueText
            # supreme_conversation
            #row[4] = correctSentence(row[4])

            # labeled_data
            #row[6] = correctSentence(row[6])

            # twitter_hate_speech_classifier
            #row[1] = correctSentence(row[1])

            # movie_lines
            #row[3] = correctSentence(row[3])

            # saving the autocorrected utterance in a new file together with all the other columns
            with open(file2, 'a') as csvfile:  # saving processed tweets to new file
                writer = csv.writer(csvfile, delimiter=';')

                # depending on the processed dataset the number of columns will be different
                # twitter_bullying
                #writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])

                # bullying_traces
                # customer_twitter
                # labeled_data
                #writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

                # twitter_hate_speech_classifier
                # movie_lines
                #writer.writerow([row[0], row[1], row[2], row[3]])

                # dialogText_196
                # dialogueText_301
                # dialogueText
                # supreme_conversation
                #writer.writerow([row[0], row[1], row[2], row[3], row[4]])

# twitter_bullying
#autocorrect("twitter_bullying_processed3.csv", "twitter_bullying_final.csv")

#bullying_traces
#autocorrect("bullying_traces_processed3.csv", "bullying_traces_final.csv")

# customer_twitter
#autocorrect("customer_twitter_processed3.csv", "customer_twitter_final.csv")

# labeled_data
#autocorrect("labeled_data_processed3.csv", "labeled_data_final.csv")

# twitter_hate_speech_classifier
#autocorrect("twitter_hate_speech_classifier_processed3.csv", "twitter_hate_speech_classifier_final.csv")

# dialogueText_196
#autocorrect("dialogueText_196_processed3.csv", "dialogueText_196_final.csv")

# dialogueText_301
#autocorrect("dialogueText_301_processed3.csv", "dialogueText_301_final.csv")

# dialogueText
#autocorrect("dialogueText_processed3.csv", "dialogueText_final.csv")

# movie_lines
#autocorrect("movie_lines_processed3.csv", "movie_lines_final.csv")

# supreme_conversation
#autocorrect("supreme_conversation_processed3.csv", "supreme_conversation_final.csv")

#print("done4")

#function to insert a hate speech column that is "1" if the tweet was labeled as RAC, REL, GEN, DIS, SO or GI
def insert_hate_speech(file1, file2):
    with open(file1) as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)  # skip header

        with open(file2, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            # header
            writer.writerow(
                ['Tweet', 'Created at', 'User', 'ID', 'Reply to', 'Text', 'Hashtags', 'Cyberbullying', 'Strength',
                 'Hate Speech', 'Topic'])

            # estimate the hate speech value based on the topics assigned by both annotators
            for row in reader:
                hate_speech = ""

                if "RAC" in row[9]:
                    hate_speech = 1
                elif "REL" in row[9]:
                    hate_speech = 1
                elif "GEN" in row[9]:
                    hate_speech = 1
                elif "DIS" in row[9]:
                    hate_speech = 1
                elif "SO" in row[9]:
                    hate_speech = 1
                elif "GI" in row[9]:
                    hate_speech = 1
                else:
                    hate_speech = 0

                #if hate_speech == 1:
                #    print("yes")

                # save the hate speech value in a new file together will all the other columns
                writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], hate_speech, row[9]])

#insert_hate_speech("twitter_bullying_final.csv", "twitter_bullying_final2.csv")






