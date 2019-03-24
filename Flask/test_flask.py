from flask import Flask, request, render_template
from flask_socketio import SocketIO


from flask_bootstrap import Bootstrap

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
    print(currentSocketId)
    print('received my event: ' + str(json))
    if (json.get("user_name") is not None):
        write_to_file(json.get("message"),json.get("user_name"), currentSocketId)
    socketio.emit('my response', json, callback=messageReceived)



if __name__ == '__main__':
    socketio.run(app, debug=True)