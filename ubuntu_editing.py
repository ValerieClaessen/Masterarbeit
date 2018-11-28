import csv
import sys

def save_with_semicolon(file, filename):
    with open(file, encoding="utf-8", errors='ignore') as f:        #save with ; as delimiter
        reader = csv.reader(f, delimiter = ',')

        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            for row in reader:
                try:
                    writer.writerow(row)
                except csv.Error as e:
                    sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

save_with_semicolon("dialogueText.csv", "dialogueText_cleaned.csv")
print("ok")
save_with_semicolon("dialogueText_196.csv", "dialogueText_196_cleaned.csv")
print("ok2")
save_with_semicolon("dialogueText_301.csv", "dialogueText_301_cleaned.csv")
print("ok3")

def write_to_new_file(file, filename):
    with open(file, 'r') as f2:
        reader = csv.reader(f2, delimiter = ";")
        next(reader, None)    #skip header

        with open(filename, 'w') as csvfile2:
            writer2 = csv.writer(csvfile2, delimiter=';')
            writer2.writerow(["Conversation ID", "Date", "From", "To", "Text"])

            for row in reader:
                writer2.writerow([row[1], row[2], row[3], row[4], row[5]])

write_to_new_file("dialogueText_cleaned.csv", "dialogueText_cleaned2.csv")
print("ok4")
write_to_new_file("dialogueText_196_cleaned.csv", "dialogueText_196_cleaned2.csv")
print("ok5")
write_to_new_file("dialogueText_301_cleaned.csv", "dialogueText_301_cleaned2.csv")
print("ok6")

