from flask import Flask, request, render_template
from flask_socketio import SocketIO

from flask_bootstrap import Bootstrap

from Flask import machine_learning
from Flask.test_save_chat import write_to_file

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


    if (json.get("message") is not None):
        class_cb = machine_learning.use_svm(json.get("message"))
        print("Cyberbullying: ", class_cb[0])
        print("Hate Speech: ", class_cb[1])
        json["cb"] = class_cb[0]
        json["hs"] = class_cb[1]

    if (json.get("user_name") is not None):
        class_cb = machine_learning.use_svm(json.get("message"))
        json["cb"] = class_cb[0]
        json["hs"] = class_cb[1]
        print(json.get("message"))
        write_to_file(json.get("message"),json.get("user_name"), currentSocketId, str(json["cb"]), str(json["hs"]), json.get("evaluation"))

    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)