import csv

with open("./Datasets/labeled_data.csv", 'r') as f:                      #ursprüngliches Datenset lesen

    reader = csv.reader(f, delimiter=',')
    lines = [line for line in f.readlines()[1:] if line.strip()]    #mit der eckigen Klammer wird die erste Zeile übersprungen, damit der alte header nicht übernommen, mit line.strip() werden die leeren Zeilen nicht mitgelesen

with open("./Datasets/labeled_data_cleaned.csv", "a") as f1:    #in neues Datenset schreiben
    writer = csv.writer(f1, delimiter=';')
    writer.writerow(['Tweet', 'Created at', 'User', 'ID', 'Reply to', 'Retweet', 'Text', 'Hashtags'])  # header
    f1.writelines(lines)

linesnew = open("./Datasets/labeled_data_cleaned.csv", "r").read().split("\n")

counter = 0

repeat = 0
while repeat < 8:
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

open("./Datasets/labeled_data_cleaned.csv", "w").write("\n".join(linesnew) + "\n")

