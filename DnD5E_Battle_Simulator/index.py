from os import environ
from flask import Flask,render_template,request,redirect,url_for,Markup
import battle_simulator
from battle_simulator import main 
from battle_simulator import settings

app=Flask(__name__)
@app.route('/')

def index():
    filename = ""
    html = ""
    if hasattr(settings,'output'):
        if settings.output != None:
            if len(settings.output) > 0:
                for i in settings.output:
                    if '<div' in i:
                        html += Markup(i + '</div>')
                    else:
                        html += Markup('<div>' + i + '</div>')

        #if hasattr(settings,'filename'):        
         #   filename = "Opening file: " + settings.filename
          #  with open(settings.filename) as f:
           #     content = f.readlines()

    data = {
        "title": 'Home Page',
        "msg":'Battle Simulator for DND 5E',
        "me": environ.get('USERNAME'),
        "process_form": process_form(),
        "filename": filename,
        "content": html }

    return render_template('index.html',data=data)

@app.route('/', methods=['GET', 'POST'])
def process_form():
    if request.method == 'POST':        
        # do stuff when the 'run battle' button is pushed
        if request.form['button'] == 'Simulate':
            main.simulate_battle()        
            return redirect(url_for('index'))
        elif request.form['button'] == 'Reset':
            main.reset_simulation()
            return redirect(url_for('index'))
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT,debug=True)