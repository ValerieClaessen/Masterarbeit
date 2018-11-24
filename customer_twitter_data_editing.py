import csv

c1 = open("./Datasets/customer_twitter_cleaned.csv", "w")
c1.truncate()
c1.close()




with open('./Datasets/customer_twitter.csv', 'r') as f2:
    reader = csv.reader(f2, delimiter = ",")

    with open('./Datasets/customer_twitter_cleaned.csv', 'w') as csvfile2:
        writer1 = csv.writer(csvfile2, delimiter=';')

        for row in reader:
            writer1.writerow(row)