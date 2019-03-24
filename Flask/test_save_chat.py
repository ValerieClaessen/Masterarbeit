
def write_to_file(text, username, userID):

    f = open('file.txt', 'a')
    f.write("user = " + str(username) + " chattext = " + str(text) + " ID = " + str(userID) + '\n')


#write_to_file("test", 23)