import csv

c1 = open("./Datasets/customer_twitter_cleaned.csv", "w")
c1.truncate()
c1.close()




with open('./Datasets/customer_twitter.csv', 'r') as f2:
    reader = csv.reader(f2, delimiter = ",")

    with open('./Datasets/customer_twitter_cleaned.csv', 'w') as csvfile2:
        writer1 = csv.writer(csvfile2, delimiter=';')
        next(reader, None)  #hierdurch wird die erste Zeile des originaldokuments übersprungen (beim einlesen)
        writer1.writerow(['Conversation ID','Tweet ID', 'Author ID', 'Created at', 'Text', 'Response Tweet', 'In Response to Tweet'])

        for row in reader:
            writer1.writerow(row)
