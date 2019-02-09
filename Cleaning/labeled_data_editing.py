import csv

c1 = open("./Datasets/labeled_data_cleaned.csv", "w")
c1.truncate()
c1.close()

c2 = open("./Datasets/labeled_data_delim_cleaned.csv", "w")
c2.truncate()
c2.close()

with open("./Datasets/labeled_data.csv", 'r') as f:                      #ursprüngliches Datenset lesen

    reader = csv.reader(f, delimiter=',')
    lines = [line for line in f.readlines() if line.strip()]    #mit line.strip() werden die leeren Zeilen nicht mitgelesen

with open("./Datasets/labeled_data_cleaned.csv", "a") as f1:    #in neues Datenset schreiben
    writer = csv.writer(f1, delimiter=';')
    #
    f1.writelines(lines)

linesnew = open("./Datasets/labeled_data_cleaned.csv", "r").read().split("\n")  #Variable die nur Strings bis zum ersten Zeilenumbruch enthält

#TODO: Herausfinden was genau enumerate macht
repeat = 0  #Variable zur gesamtwiederholung aller Säuberungsmechanismen
while repeat < 8:   #8 mal durchlaufen
    for i, line in enumerate(linesnew):
        left_text = line.partition(",")[0]
        if not line.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
            linesnew[i - 1] = linesnew[i - 1].strip() + " " + line
            linesnew.pop(i)
        elif "." in left_text :
            linesnew[i - 1] = linesnew[i - 1].strip() + " " + line
            linesnew.pop(i)
        elif "," not in line[:7]:
             linesnew[i - 1] = linesnew[i - 1].strip() + " " + line
             linesnew.pop(i)
    repeat = repeat +1
# Zeilen neu aneinander hängen
open("./Datasets/labeled_data_cleaned.csv", "w").write("\n".join(linesnew) + "\n") #TODO: Herausfinden was join() hier genau macht

#Datei neu mit dem richtigen Delimiter (zunächst lesen) schreiben
with open('./Datasets/labeled_data_cleaned.csv', encoding="utf-8", errors='ignore') as f:    #save with ; as delimiter
    reader1 = csv.reader(f, delimiter = ',')

    with open('./Datasets/labeled_data_delim_cleaned.csv', 'w') as csvfile:
        writer1 = csv.writer(csvfile, delimiter=';')
        writer1.writerow(['ID', 'Count', 'Hate Speech', 'Offensive Language', 'Neither', 'Class', 'Tweet'])  # header
        #neue richtige Zeilenzahlen einfügen
        count = 0
        for row in reader1:
            row[0] = count
            writer1.writerow(row) #Zeile schreiben
            count += 1
