import csv

def text_to_csv():
    with open("movie_lines.txt", "r", errors="ignore") as file:
        filedata = file.read()

    filedata = filedata.replace("+++$+++", ";")

    with open('movie_lines.csv', 'w', errors="ignore") as f:
        f.write(filedata)

    with open("movie_conversations.txt", "r", errors="ignore") as file2:
        filedata2 = file2.read()

    filedata2 = filedata2.replace("+++$+++", ";")

    with open('movie_conversations.csv', 'w', errors="ignore") as f2:
        f2.write(filedata2)

    with open('movie_conversations.csv', 'r') as f5:
        reader3 = csv.reader(f5, delimiter=";")

        with open('movie_conversations_new.csv', 'w') as f4:
            writer2 = csv.writer(f4, delimiter=";")

            count = 1
            for row in reader3:
                writer2.writerow([count, row[0], row[1], row[2], row[3]])
                count += 1

def match_lines_conversations():
    with open('movie.csv', 'w') as f3:
        writer = csv.writer(f3, delimiter=';')
        writer.writerow(['Conversation ID', 'Line ID', 'Character ID', 'Utterance'])

        with open("movie_lines.csv", "r") as file3:
            reader = csv.reader(file3, delimiter=";")

            with open("movie_conversations_new.csv", "r") as file4:
                reader2 = list(csv.reader(file4, delimiter=";"))

                for row in reader:
                    conversation_id = ""
                    movie_line = row[0]
                    movie_line = movie_line.replace(" ", "")

                    for line in reader2:
                        movie_lines = line[4]
                        movie_lines = movie_lines.replace("[", "")
                        movie_lines = movie_lines.replace("]", "")
                        movie_lines = movie_lines.replace("'", "")
                        movie_lines = movie_lines.replace(" ", "")
                        movie_lines = movie_lines.split(",")
                        for element in movie_lines:
                            if movie_line == element:
                                conversation_id = line[0]

                    writer.writerow([conversation_id, row[0], row[1], row[4]])

text_to_csv()
match_lines_conversations()
