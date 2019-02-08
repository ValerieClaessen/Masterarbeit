import csv

# function to save movie_lines.txt and movie_conversations.txt in a csv file
def text_to_csv():
    with open("movie_lines.txt", "r", errors="ignore") as file:
        filedata = file.read()

    # replace old seperator (+++$+++) with ";"
    filedata = filedata.replace("+++$+++", ";")

    # save as csv
    with open('movie_lines.csv', 'w', errors="ignore") as f:
        f.write(filedata)


    with open("movie_conversations.txt", "r", errors="ignore") as file2:
        filedata2 = file2.read()

    # replace old seperator (+++$+++) with ";"
    filedata2 = filedata2.replace("+++$+++", ";")

    # save as csv
    with open('movie_conversations.csv', 'w', errors="ignore") as f2:
        f2.write(filedata2)


    with open('movie_conversations.csv', 'r') as f5:
        reader3 = csv.reader(f5, delimiter=";")

        with open('movie_conversations_new.csv', 'w') as f4:
            writer2 = csv.writer(f4, delimiter=";")

            # label each conversation with a respective id and save data in a new file with a new column containing the id
            count = 1
            for row in reader3:
                writer2.writerow([count, row[0], row[1], row[2], row[3]])
                count += 1

# function to match movie lines with their respective conversation
def match_lines_conversations():
    # create a new file movie.csv that will have an additional column containing the id of the conversation the utterance is a part of
    with open('movie.csv', 'w') as f3:
        writer = csv.writer(f3, delimiter=';')

        # header
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

                        # remove useless symbols
                        movie_lines = movie_lines.replace("[", "")
                        movie_lines = movie_lines.replace("]", "")
                        movie_lines = movie_lines.replace("'", "")
                        movie_lines = movie_lines.replace(" ", "")

                        # create a list containing all line ids from a conversation
                        movie_lines = movie_lines.split(",")

                        # if the id of a line in movie_lines matches an id from a conversation in movie_conversations_new,
                        # save the id of the conversation
                        for element in movie_lines:
                            if movie_line == element:
                                conversation_id = line[0]

                    # save all data from movie_lines in a new file containing an additional columns for the respective conversation_id
                    writer.writerow([conversation_id, row[0], row[1], row[4]])

#text_to_csv()
#match_lines_conversations()
