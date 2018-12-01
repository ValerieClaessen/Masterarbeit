# Cleaning our own twitter bullying data
import csv
import sys

def append_data():
    with open('twitter_bullying_archive.csv', 'r') as f:
        reader = csv.reader(f, delimiter = ";")
        next(reader, None)    #skip header

        with open('twitter_bullying_archive2.csv', 'r') as f3:
            reader2 = csv.reader(f3, delimiter=";")
            next(reader2, None)  # skip header

            with open('twitter_bullying_archive3.csv', 'r') as f4:
                reader3 = csv.reader(f4, delimiter=";")
                next(reader, None)  # skip header

                with open('twitter_bullying_archive4.csv', 'r') as f5:
                    reader4 = csv.reader(f5, delimiter=";")
                    next(reader, None)  # skip header

                    with open('twitter_bullying_archive5.csv', 'r') as f6:
                        reader5 = csv.reader(f6, delimiter=";")
                        next(reader, None)  # skip header

                        with open('twitter_bullying_archive6.csv', 'r') as f7:
                            reader6 = csv.reader(f7, delimiter=";")
                            next(reader, None)  # skip header

                            with open('twitter_bullying_archive7.csv', 'r') as f8:
                                reader7 = csv.reader(f8, delimiter=";")
                                next(reader, None)  # skip header

                                with open('twitter_bullying.csv', 'a') as f2:          #merge files
                                    writer = csv.writer(f2, delimiter=';')
                                    writer.writerow(['Tweet', 'Created at', 'User', 'ID', 'Reply to', 'Retweet', 'Text', 'Hashtags'])  # header

                                    count = 1
                                    for row in reader:
                                        row[0] = count
                                        writer.writerow(row)
                                        count += 1

                                    for row in reader2:
                                        row[0] = count
                                        writer.writerow(row)
                                        count += 1

                                    for row in reader3:
                                        row[0] = count
                                        writer.writerow(row)
                                        count += 1

                                    for row in reader4:
                                        row[0] = count
                                        writer.writerow(row)
                                        count += 1

                                    for row in reader5:
                                        row[0] = count
                                        writer.writerow(row)
                                        count += 1

                                    for row in reader6:
                                        row[0] = count
                                        writer.writerow(row)
                                        count += 1

                                    for row in reader7:
                                        row[0] = count
                                        writer.writerow(row)
                                        count += 1

#delete same tweets
def delete_same_tweets():
    with open('twitter_bullying.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)  # skip header

        with open('twitter_bullying_cleaned.csv', 'w') as f2:
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
    with open('twitter_bullying_cleaned.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";")
        next(reader, None)  # skip header

        with open('twitter_bullying_cleaned2.csv', 'w') as f2:
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

#TODO: Daten nach Datum ordnen

append_data()
delete_same_tweets()
get_hashtags()
