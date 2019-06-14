from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO

from flask_bootstrap import Bootstrap

import machine_learning
from test_save_chat import write_to_file

import ml_processing

import svm

import csv

import pickle

training_list = ml_processing.process_data("train_set.csv")

matrix_pos = svm.do_matrix(training_list, "lexicon_pos.txt")
matrix_neut = svm.do_matrix(training_list, "lexicon_neut.txt")
matrix_neg = svm.do_matrix(training_list, "lexicon_neg.txt")

curses = ml_processing.make_list_of_curse_words("curses.txt")

with open('prestem_no_dup.csv', 'r') as csvfile:
    dict_words = {}
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        dict_words[row[0]] = row[1]

    pickle.dump(dict_words, open("complete_dict.p", "wb"))

pickle.dump(training_list, open("training_list.p", "wb"))
pickle.dump(matrix_pos, open("matrix_pos.p", "wb"))
pickle.dump(matrix_neut, open("matrix_neut.p", "wb"))
pickle.dump(matrix_neg, open("matrix_neg.p", "wb"))
pickle.dump(curses, open("curses.p", "wb"))

count = 0

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/', methods=['POST', 'GET'])
def sessions():
    return render_template('index.html')
    #return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('connect')
def connect():
    global count
    count += 1
    #print(count)

    stat = {'count': count}
    jsonify(stat)

    socketio.emit('status', stat, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    global count
    count -= 1
    #print(count)

    stat = {'count': count}
    jsonify(stat)

    socketio.emit('status', stat, broadcast=True)

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    currentSocketId = request.sid   #gibt die individuelle ID des aktuellen User an
    print('current socketID: ' + currentSocketId)
    print('received my event: ' + str(json))

    if (json.get("user_name") is not None):
        print(json.get("message"))
        write_to_file(json.get("message"),json.get("user_name"), currentSocketId, str(json["cyberbullying"]), str(json["hatespeech"]), json.get("evaluation"))

    socketio.emit('my response', json, callback=messageReceived)

@app.route('/machine_learning', methods=['GET', 'POST'])
def do_machine_learning():
    message = request.form['sentence']
    c_b = request.form['cb']
    h_s = request.form['hs']

    if (message is not None):
        class_cb = machine_learning.use_svm(message)
        print("Cyberbullying: ", class_cb[0])
        print("Hate Speech: ", class_cb[1])
        c_b = class_cb[0]
        h_s = class_cb[1]

    dict = {'sentence': message, 'cb': c_b, 'hs': h_s}

    return jsonify(dict)

if __name__ == '__main__':
    socketio.run(app, debug=True)