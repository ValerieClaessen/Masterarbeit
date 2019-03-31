import datetime


def write_to_file(text, username, userID, comp_cb, comp_hs, eval):

    x = datetime.datetime.now()
    date = str(x.date())
    print(date)

    if date == "2019-03-31":
        f = open('file_2019-03-31.txt', 'a')
        f.write("user = " + str(username) + " chattext = " + str(text) + " ID = " + str(userID) + " computed CB = " + str(comp_cb) + " computed HS = " + str(comp_hs) + " evaluation = " + str(eval) + '\n')
    else:
        f = open('file.txt', 'a')
        f.write("user = " + str(username) + " chattext = " + str(text) + " ID = " + str(userID) + '\n')


#write_to_file("test", 23)