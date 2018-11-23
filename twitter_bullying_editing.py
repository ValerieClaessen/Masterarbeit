# Cleaning our own twitter bullying data
import csv
import sys

def append_data():
    with open('twitter_bullying_archive.csv', 'r') as f:
        reader = csv.reader(f, delimiter = ";")
        next(reader, None)    #skip header

        with open('twitter_bullying_archive2.csv', 'a') as f2:          #merge files
            writer = csv.writer(f2, delimiter=';')

            count = 13043
            for row in reader:
                row[0] = count
                writer.writerow(row)
                count += 1

#delete same tweets
def delete_same_tweets():
    with open('twitter_bullying_archive2.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)  # skip header

        with open('twitter_bullying_archive2_cleaned.csv', 'w') as f2:
            writer = csv.writer(f2, delimiter=';')
            lines = []
            count = 1

            for row in reader:
                same = False
                for line in lines:
                    if line == row[6]:
                        same = True

                if same == False:
                    print("new")
                    lines.append(row[6])
                    row[0] = count
                    writer.writerow(row)
                    count += 1
                else:
                    print("same")

def get_hashtags():
    with open('twitter_bullying_archive2_cleaned.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)  # skip header

        with open('twitter_bullying_archive2_cleaned2.csv', 'w') as f2:
            writer = csv.writer(f2, delimiter=';')
            writer.writerow(['Tweet', 'Created at', 'User', 'ID', 'Reply to', 'Retweet', 'Text', 'Hashtags'])  # header

            for row in reader:
                hashtags = row[7]
                symbols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "[", "]", "{", "}", "'", '"', "text:", "indices:", " ,", " "]
                for symbol in symbols:
                    hashtags = hashtags.replace(symbol, "")
                hashtags = hashtags.split(",")
                hashtags = ' '.join(hashtags).split()
                hashtag = ""
                for element in hashtags:
                    hashtag = hashtag + element + ", "
                hashtag = hashtag[:-2]
                row[7] = hashtag
                print(hashtag)

                writer.writerow(row)

append_data()
delete_same_tweets()
get_hashtags()
