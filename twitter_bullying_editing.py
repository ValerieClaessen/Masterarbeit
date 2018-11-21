# Cleaning our own twitter bullying data
import csv
import sys

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
with open('twitter_bullying_archive2.csv', 'r') as f3:
    reader2 = csv.reader(f3, delimiter=";")
    next(reader2, None)  # skip header

    with open('twitter_bullying_archive2_cleaned.csv', 'w') as f4:
        writer2 = csv.writer(f4, delimiter=';')
        lines = []
        count = 1

        for row in reader2:
            same = False
            for line in lines:
                if line == row[6]:
                    same = True

            if same == False:
                print("new")
                lines.append(row[6])
                row[0] = count
                writer2.writerow(row)
                count += 1
            else:
                print("same")


