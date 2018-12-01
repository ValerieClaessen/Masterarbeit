# Cleaning the Twitter Hate Speech Classifier Dataset
import csv
import sys

with open('twitter-hate-speech-classifier.csv', encoding="utf-8", errors='ignore') as f:        #save with ; as delimiter
    reader = csv.reader(f, delimiter = ',')

    with open('twitter-hate-speech-classifier_cleaned.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        for row in reader:
            try:
                writer.writerow(row)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % ("twitter-hate-speech-classifier_cleaned.csv", reader.line_num, e))

with open('twitter-hate-speech-classifier_cleaned.csv', 'r') as f2:
    reader2 = csv.reader(f2, delimiter = ";")
    next(reader2, None)    #skip header

    with open('twitter-hate-speech-classifier_cleaned2.csv', 'w') as csvfile2:
        writer2 = csv.writer(csvfile2, delimiter=';')
        writer2.writerow(["Tweet ID", "Text", "Hate Speech", "Confidence"])

        for row in reader2:
            if row[5] == "The tweet contains hate speech":
                row[5] = 2
            elif row[5] == "The tweet uses offensive language but not hate speech":
                row[5] = 1
            else:
                row[5] = 0

            writer2.writerow([row[18], row[19], row[5], row[6]])
