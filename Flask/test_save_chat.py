
def write_to_file(text, chatID):

    f = open('file.txt', 'a')
    f.write("user = " + str(chatID) + " chattext = " + str(text) + '\n')


#write_to_file("test", 23)