# Cleaning the Twitter Hate Speech Classifier Dataset

import csv
import sys
import codecs

with open('twitter-hate-speech-classifier.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    with open('twitter-hate-speech-classifier_cleaned.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for row in reader:
            writer.writerow(row)