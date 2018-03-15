from os import environ
from flask import Flask,render_template,request,redirect,url_for,Markup
import battle_simulator
from battle_simulator import simulate
from battle_simulator import settings
from battle_simulator import print_functions

app=Flask(__name__)
@app.route('/')

def index():
    filename = ""
    html = ""
    
    #init_combatants = []
    
    #for combatant in init_combatants:
    #    print_details_html(combatant,html) 

    if hasattr(settings,'output'):
        if settings.output != None:
            if len(settings.output) > 0:
                for i in settings.output:
                    if '<div' in i:
                        html += Markup(i + '</div>')
                    else:
                        html += Markup('<div>' + i + '</div>')           

    data = {
        "title": 'Dungeons & Dragons 5E - Battle Simulator',
        "msg":'Select and customise your combatants, the hit Simulate to see how they compete!',
        "process_form": process_form(),
        "filename": filename,
        "content": html
        }

    return render_template('index.html',data=data)

@app.route('/', methods=['GET', 'POST'])
def process_form():
    if request.method == 'POST':        
        # do stuff when the 'run battle' button is pushed
        if request.form['button'] == 'Simulate':
            simulate.simulate_battle() 
            return redirect(url_for('index'))
        elif request.form['button'] == 'Reset':
            simulate.reset_simulation()
            return redirect(url_for('index'))
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else

def print_details_html(combatant,html):
    html += Markup('<div class=combatant>')
    html += Markup('<div> Name: '  + combatant.fullname + '</div>')
    html += Markup('<div> Race: '  + combatant.race.name + '</div>')
    html += Markup('<div> Class: '  + combatant.creature_class.name + '</div>')
    html += Markup('<div> Sub-class: '  + combatant.creature_subclass.name + '</div>')
    html += Markup('<div> Max Hit Points: '  + repr(combatant.max_health) + '</div>')
    html += Markup('<div> --------------------------------' + '</div>')
    html += Markup('<div> Stats: ' + '</div>')
    html += Markup('<div> Strength: ' + repr(combatant.stats.str) + '</div>')
    html += Markup('<div> Dexterity: ' + repr(combatant.stats.dex) + '</div>')
    html += Markup('<div> Constitution: ' + repr(combatant.stats.con) + '</div>')
    html += Markup('<div> Intelligence: ' + repr(combatant.stats.intel) + '</div>')
    html += Markup('<div> Wisdom: ' + repr(combatant.stats.wis) + '</div>')
    html += Markup('<div> Charisma: ' + repr(combatant.stats.cha) + '</div>')
    html += Markup('<div>' + '</div>')
    html += Markup('<div> Weapon Proficiencies: ' + '</div>')
    for item in combatant.weapon_proficiency():
        html += Markup('<div> Weapon Proficiency: ' + item.name + '</div>')
    html += Markup('<div>' + '</div>')
    html += Markup('<div>' + '</div>')
    html += Markup('<div> Equipped Weapon: ' + combatant.current_weapon.name + '</div>')
    html += Markup('<div> Other Weapons: ' + '</div>')
    for item in combatant.weapon_inventory():
        html += Markup('<div> Weapon: ' + item.name + '</div>')
    html += Markup('<div>' + '</div>')
    html += Markup('<div> Other Equipment: ' + '</div>')
    for item in combatant.equipment_inventory():
        html += Markup('<div> Item: ' + item.name + '</div>')
    html += Markup('<div>' + '</div>')
    html += Markup('<div>---------------------------------' + '</div>')
    html += Markup('</div>')

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT,debug=True)