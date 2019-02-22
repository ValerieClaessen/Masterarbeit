import csv

c1 = open("./Datasets/relational_strategies_1_cleaned.csv", "w")
c1.truncate()
c1.close()

c2 = open("./Datasets/relational_strategies_2_cleaned.csv", "w")
c2.truncate()
c2.close()




with open('./Datasets/relational_strategies_1.csv', 'r') as f2:
    reader = csv.reader(f2, delimiter = ",")

    with open('./Datasets/relational_strategies_1_cleaned.csv', 'w') as csvfile2:
        writer1 = csv.writer(csvfile2, delimiter=';')
        next(reader, None)  #hierdurch wird die erste Zeile des originaldokuments übersprungen (beim einlesen)
        writer1.writerow(['User ID', 'Text'])

        for row in reader:
            writer1.writerow((row[4], row[5]))

with open('./Datasets/relational_strategies_2.csv', 'r') as f2:
    reader2 = csv.reader(f2, delimiter = ",")

    with open('./Datasets/relational_strategies_2_cleaned.csv', 'w') as csvfile2:
        writer2 = csv.writer(csvfile2, delimiter=';')
        next(reader2, None)  #hierdurch wird die erste Zeile des originaldokuments übersprungen (beim einlesen)
        writer2.writerow(['User ID', 'Text'])

        for row in reader2:
            writer2.writerow((row[4], row[5]))