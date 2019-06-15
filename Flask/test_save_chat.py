import datetime
import csv


def write_to_file(text, username, userID, cb, hs, eval):

    x = datetime.datetime.now()
    date = str(x.date())
    print(date)

    if date == "2019-03-31":
        with open('save_csv.csv', mode='a') as save:

            save_writer = csv.writer(save, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            try:
                save_writer.writerow([str(username), str(text), str(userID), str(cb), str(hs), str(eval)])
            except csv.Error:
                return "Error"
            finally:
                print("not possible to write!")
    else:
        with open('save_csv.csv', mode='a') as save:

            save_writer = csv.writer(save, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            try:
                save_writer.writerow([str(username), str(text), str(userID), str(cb), str(hs), str(eval)])
            except csv.Error:
                return "Error"
            finally:
                print("not possible to write!")
#write_to_file("test", 23)