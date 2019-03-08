from flask import Flask, url_for, request, render_template

from Flask.test_save_chat import write_to_file

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/chat", methods=['POST', 'GET'])
def chat():
    name = ""
    if request.method == 'POST':
        name = request.form['name']
        write_to_file(name, 23)
    else:
        name = request.args.get('name')
    return "Hello " + name + "!"

if __name__ == '__main__':
    app.run(port=1337, debug=True)  #Debug muss auf einem echten Server auf False gestellt werden!