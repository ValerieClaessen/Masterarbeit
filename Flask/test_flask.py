from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO

from flask_bootstrap import Bootstrap

import machine_learning
from test_save_chat import write_to_file

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

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    currentSocketId = request.sid   #gibt die individuelle ID des aktuellen User an
    print('current socketID: ' + currentSocketId)
    print('received my event: ' + str(json))

    if (json.get("user_name") is not None):
        print(json.get("message"))
        #write_to_file(json.get("message"),json.get("user_name"), currentSocketId, str(json["cb"]), str(json["hs"]), json.get("evaluation"))
        write_to_file(json.get("message"),json.get("user_name"), currentSocketId, json.get("evaluation"))

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