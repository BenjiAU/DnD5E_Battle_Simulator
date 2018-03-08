from os import environ
from flask import Flask,render_template
app=Flask(__name__)
@app.route('/')
def index():
    data = {
        "title": 'Home Page',
        "msg":'Hello World from Flask for Python !!!',
        "me": environ.get('USERNAME')}
    return render_template('index.html',data=data)
if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT,debug=True)