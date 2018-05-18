
from os import environ
from flask import Flask,render_template,request,redirect,url_for,Markup
import battle_simulator
from battle_simulator import simulate
from battle_simulator import settings
from battle_simulator import print_functions
from battle_simulator import combatants

app=Flask(__name__)
@app.route('/')

def index():
    filename = ""
    html = Markup('<div>----Output----</div>')   
    html_combatants = ""
    
    simulate.load_combatants()
    for combatant in combatants.list:
        html_combatants += print_details_html(combatant)                 

    if hasattr(settings,'output'):
        if settings.output != None:
            if len(settings.output) > 0:
                for i in settings.output:
                    if '<div' in i:
                        html += Markup(i + '</div>')
                    else:
                        html += Markup('<div>' + i + '</div>')           

    data = {
        "title": 'Critical Role Battle Simulator V1.0',
        "msg":'Warning - content on this website may contain spoilers for one or both campaigns of Critical Role.',
        "process_form": process_form(), 
        "filename": filename,
        "combatants": html_combatants,
        "content": html
        }

    return render_template('index.html',data=data)

@app.route('/', methods=['GET', 'POST'])
def process_form():
    if request.method == 'POST':        
        # do stuff when the 'run battle' button is pushed
        if request.form['simulate'] == 'Simulate':            
            combatants.list = [combatant for combatant in combatants.list if request.form.get('combatant_' + combatant.name)]
            for combatant in combatants.list:
                selected_team = request.form.get('team_' + combatant.name)
                for team in combatants.teams:
                    if selected_team == team.name and selected_team != combatant.team.name:
                        combatant.team = team
                selected_xpos = int(request.form.get('xpos_' + combatant.name))
                if selected_xpos != combatant.starting_xpos and selected_ypos != 0:
                    combatant.starting_xpos = selected_xpos
                selected_ypos = int(request.form.get('ypos_' + combatant.name))
                if selected_ypos != combatant.starting_ypos and selected_ypos != 0:
                    combatant.starting_ypos = selected_ypos
            #selected_combatants = request.form.getlist("combatant")
            #selected_teams = request.form.getlist('team_select')
            #simulate.set_combatants(selected_combatants,selected_teams)            
            simulate.simulate_battle()
            return redirect(url_for('index'))
        elif request.form['simulate'] == 'Reset':
            simulate.reset_simulation()
            return redirect(url_for('index'))
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else

def print_details_html(combatant):
    string = ""
    string += Markup('<div class=combatant>')    
    string += Markup('<tr>')
    string += Markup('<td>')
    string += Markup('<input type=checkbox name="combatant_' + combatant.name + '" value="'+ combatant.fullname+ '">')
    string += Markup('</td>')
    string += Markup('<td>')
    string += Markup(print_functions.characterlevel(combatant))
    string += Markup('</td>')
    string += Markup('<td>')
    string += Markup(combatant.fullname)
    string += Markup('</td>')
    string += Markup('<td>')
    string += Markup(combatant.notes)
    string += Markup('</td>')
    string += Markup('<td>')    
    string += Markup('<input type=text onkeypress="return isNumberKey(event)"  name="xpos_' + combatant.name + '" value="' + repr(combatant.starting_xpos) + '">')
    string += Markup('</td>')
    string += Markup('<td>')
    string += Markup('<input type=text onkeypress="return isNumberKey(event)" name="ypos_' + combatant.name + '" value="' + repr(combatant.starting_ypos) + '">')
    string += Markup('</td>')
    string += Markup('<td>')    
    string += Markup('<select name="team_' + combatant.name + '" class="selectpicker form-control">')
    for team in combatants.teams:
        if team.name == combatant.team.name:
            string += Markup('<option selected="selected" value="' + team.name + '">' + team.name + '</option>')
        else:
            string += Markup('<option value="' + team.name + '">' + team.name + '</option>')
    string += Markup('</select>')
    string += Markup('</td>')
    string += Markup('</tr>')
    string += Markup('</div>')
    return(string)

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT,debug=True)