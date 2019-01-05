
import json
import jsonpickle
from os import environ, urandom
from flask import Flask,render_template,request,redirect,url_for,Markup,session
import battle_simulator
from battle_simulator import simulate
from battle_simulator import settings
from battle_simulator import print_functions
from battle_simulator import combatants

app=Flask(__name__)
app.secret_key = urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
@app.route('/')

def index():
    filename = ""
    html = Markup('<div class="output">----Output----')       
    # Master output column rendered here
    html += Markup('<div class="output_column">')       
    html_combatants = ""
    
    handle_session_combatants()

    for combatant in combatants.list:
        html_combatants += print_functions.print_combatant_table(combatant)                 

    if hasattr(settings,'output'):        
        store_output()

    output = retrieve_output()
    if output:
        if len(output) > 0:
            for i in output:
                #When the code generates a new column, terminate the outer div to close that column first and allow floating
                # When the code starts a random div, terminate it                    
                if '<div' in i or 'table' in i or 'td' in i:
                    html += Markup(i)
                else:
                    html += Markup(i + '<br>')           
    
    # End the Output Column div                        
    html += Markup('</div>')
    # End the Output div
    html += Markup('</div>')
    data = {
        "title": 'Critical Role Battle Simulator V2.0',
        "msg":'Warning - content on this website may contain spoilers for both campaigns of Critical Role, in the form of revealing character names, statistics, and items that may not be revealed in earlier episodes. Please proceed with caution if you are not up to date!',
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
            if len(combatants.list) > 0:
                for combatant in combatants.list:
                    # Team selection
                    selected_team = request.form.get('team_' + combatant.name)
                    for team in combatants.teams:
                        if selected_team == team.name and selected_team != combatant.team.name:
                            combatant.team = team
                    # Position selection
                    selected_xpos = int(request.form.get('xpos_' + combatant.name))
                    if selected_xpos != combatant.starting_xpos:
                        combatant.starting_xpos = selected_xpos
                    selected_ypos = int(request.form.get('ypos_' + combatant.name))
                    if selected_ypos != combatant.starting_ypos:
                        combatant.starting_ypos = selected_ypos
                    # Max HP selection
                    selected_max_hp = int(request.form.get('max_health_' + combatant.name))
                    if selected_max_hp != combatant.max_health:
                        # Error checking
                        if selected_max_hp > 0 and selected_max_hp <= 999:
                            combatant.max_health = selected_max_hp
                    # AC selection
                    selected_armour_class = int(request.form.get('armour_class_' + combatant.name))
                    if selected_armour_class != combatant.armour_class:
                        # Error checking
                        if selected_armour_class > 0 and selected_armour_class <= 30:
                            combatant.armour_class = selected_armour_class
                    # Level selection
                    if len(combatant.player_classes()) == 1:
                        selected_character_level = int(request.form.get('character_level_' + combatant.name))        
                        if selected_character_level != combatant.player_classes()[0].player_class_level:             
                            if selected_character_level > 0 and selected_character_level <= 20:
                                combatant.player_classes()[0].player_class_level = selected_character_level                
                #selected_combatants = request.form.getlist("combatant")
                #selected_teams = request.form.getlist('team_select')
                #simulate.set_combatants(selected_combatants,selected_teams)         

                #Update the combatants stored 
                session['combatants'] = jsonpickle.encode(combatants.list)

            simulate.simulate_battle()
            return redirect(url_for('index'))
        elif request.form['simulate'] == 'Reset':
            session.clear()
            simulate.reset_simulation()
            return redirect(url_for('index'))
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else

def handle_session_combatants():
    #See if combatants have already been set up for this session
    x = session.get('combatants', None)
    if not x:
        #Load combatants new
        simulate.load_combatants()
        print(combatants.list[1])
        session['combatants'] = jsonpickle.encode(combatants.list)        
    else:
        #Retrieve original list of combatants, flag that this is a repeat battle        
        combatants.list = jsonpickle.decode(session['combatants'])              
    return session['combatants']

def store_output():
    x = session.get('output', None)
    if not x:
        #Load combatants new
        session['output'] = jsonpickle.encode(settings.output)                

def retrieve_output():
    x = session.get('output', None)
    if x:
        #Load combatants new
        return(jsonpickle.decode(session['output']))           
    return ""

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT,debug=True)