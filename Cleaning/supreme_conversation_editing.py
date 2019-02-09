import csv

c1 = open("./Datasets/supreme_conversation_data_cleaned.csv", "w")
c1.truncate()
c1.close()

import fileinput
#TODO: Spaltenüberschriften werden im Moment noch nicht angenommen --> herausfinden wieso
# with open("./Datasets/supreme_conversation_data_cleaned.csv", "w") as f1:  # in neues Datenset schreiben
#     writer = csv.writer(f1, delimiter=';')


with open('./Datasets/supreme.conversations.txt', 'r') as file :
    filedata = file.read()

# festlegen der Strings die gefunden und dann ausgetaucht werden sollen
filedata = filedata.replace('+++$+++', ';') #Merke: replace()

# Neuschreiben des so veränderten Dokuments, dieses mal in ein neues csv-Dokument
with open('./Datasets/supreme_conversation_data_cleaned.csv', 'w') as file:
  file.write(filedata)
  #writer1 = csv.writer(file, delimiter=';')
  #writer1.writerow(['Case ID', 'Utterance ID', 'After Previous', 'Speaker', 'Utterance'])  # header


with open('./Datasets/supreme_conversation_data_cleaned.csv', encoding="utf-8", errors='ignore') as f:    #save with ; as delimiter
    reader1 = csv.reader(f, delimiter = ';')

    with open('./Datasets/supreme_conversation_data_header_cleaned.csv', 'w') as csvfile:
        writer1 = csv.writer(csvfile, delimiter=';')
        writer1.writerow(['Case ID', 'Utterance ID', 'After Previous', 'Speaker', 'Utterance'])  # header
        #neue richtige Zeilenzahlen einfügen

        for r in reader1:
            writer1.writerow((r[0], r[1], r[2], r[3], r[7]))





