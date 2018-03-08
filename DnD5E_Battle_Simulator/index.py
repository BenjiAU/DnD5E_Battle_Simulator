from os import environ
from flask import Flask,render_template,request,redirect,url_for
import battle_simulator
from battle_simulator import main 
from battle_simulator import settings

app=Flask(__name__)
@app.route('/')

def index():
    filename = ""
    content = "No content yet!"
    if settings:
        if hasattr(settings,'filename'):        
            filename = "Opening file: " + settings.filename
            with open(settings.filename) as f:
                content = f.readlines()

    data = {
        "title": 'Home Page',
        "msg":'Battle Simulator for DND 5E',
        "me": environ.get('USERNAME'),
        "output": output_form(),
        "reset": reset_form(),
        "filename": filename,
        "content": content }

    return render_template('index.html',data=data)

@app.route('/', methods=['GET', 'POST'])
def output_form():
    if request.method == 'POST':
        # do stuff when the form is submitted        
        main.simulate_battle()        
            
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def reset_form():
    if request.method == 'POST':
        # do stuff when the form is submitted          
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return render_template('index.html')

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT,debug=True)