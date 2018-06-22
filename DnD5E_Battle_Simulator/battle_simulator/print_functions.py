import os
from os import path    
import time
import datetime
from datetime import timedelta 

import math
from flask import Markup
from battle_simulator import settings
from battle_simulator import combatants

def set_output_file():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H%M%S')    
    if not os.path.exists("combatlog/"):
        os.makedirs("combatlog/")
    settings.filename = "combatlog/combat_" + st + ".html"

def open_file():
    if settings.filename != "":
        if not settings.file_open:            
            settings.file = open(settings.filename,'a')
            settings.file_open = True
            print("File located at " + settings.file.name)
            print_time_stamp(True,'Starting Time: ')

def close_file():
    print_time_stamp(False,'Ending Time: ')    
    if settings.filename != "":
        settings.file.close()
        settings.file_open = False

def delete_file():
    if (settings.filename != "") and (settings.file_open == False):
        os.remove(settings.filename)      

def print_output(string): 
    if not settings.suppress_output:
        if settings.filename != "":
            if not settings.file_open:
                open_file()      
            print(string,file=settings.file)
            settings.output.append(string)
        else:
            print(string)
            settings.output.append(string)

def begin_div(string):
    print_output('<div class="' + string + '">')

def end_div():
    print_output('</div>')

def print_error(string):
    print_output('<div class="error"' + string + '</div>')

def print_time_stamp(start,string):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S') 
    if start:
        settings.start_time = ts
    else:
        settings.end_time = ts
    string = string + st
    print(string,file=settings.file)
    settings.output.append(string)
    if not start:        
        elapsed = settings.end_time - settings.start_time
        string = 'Total run time: ' + repr(elapsed) + ' seconds.'
        print(string,file=settings.file)
        settings.output.append(string)
    
def print_combatant_table(combatant):
    all_ticked = False
    string = ""
    string += Markup('<div class=combatant>')    
    string += Markup('<tr>')
    string += Markup('<td>')
    if all_ticked:
        string += Markup('<input type=checkbox checked=True name="combatant_' + combatant.name + '" value="'+ combatant.fullname+ '">')
    else:
        string += Markup('<input type=checkbox name="combatant_' + combatant.name + '" value="'+ combatant.fullname+ '">')
    string += Markup('</td>')
    string += Markup('<td>')
    string += Markup(combatant.fullname)
    string += Markup('</td>')
    string += Markup('<td>')    
    if len(combatant.player_classes()) == 1:
        string += Markup('<input type=text onkeypress="return isNumberKey(event)"  name="character_level_' + combatant.name + '" value="' + repr(characterlevel(combatant)) + '">')            
    else:
        string += Markup(characterlevel(combatant))    
    string += Markup('</td>')
    string += Markup('<td>')
    string += Markup('<input type=text onkeypress="return isNumberKey(event)"  name="max_health_' + combatant.name + '" value="' + repr(combatant.max_health) + '">')            
    string += Markup('</td>')
    string += Markup('<td>')
    string += Markup('<input type=text onkeypress="return isNumberKey(event)"  name="armour_class_' + combatant.name + '" value="' + repr(combatant.armour_class) + '">')            
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

def begin_combatant_details():
    string = ""
    string += '<table class=combatant_details>'
    string += '<tr>'
    print_output(string)

def end_combatant_details():    
    string = ""    
    string += '</tr>'
    string += '</table>'
    print_output(string)

def print_combatant_details(combatant,position):
    print_output('<td valign=top>')
    print_output('Initiative Order: ' + repr(position)) 
    print_output('Name: '  + combatant.fullname)
    print_output('Team: '  + combatant.team.name)
    print_output('Race: '  + combatant.race.name)
    print_output('Character Level ' + repr(characterlevel(combatant)))
    print_output('Class Breakdown: ')
    for class_instance in combatant.player_classes():
        print_indent( 'Class: '  + class_instance.player_class.name)
        if class_instance.player_subclass:
            print_double_indent( 'Sub-class: '  + class_instance.player_subclass.name)
        print_double_indent( 'Level: '  + repr(class_instance.player_class_level))
    print_output('Max Hit Points: '  + repr(combatant.max_health))
    print_output(' --------------------------------' )
    print_output('Stats: ')
    print_output('Strength: ' + repr(combatant.stats.str))
    print_output('Dexterity: ' + repr(combatant.stats.dex))
    print_output('Constitution: ' + repr(combatant.stats.con))
    print_output('Intelligence: ' + repr(combatant.stats.intel))
    print_output('Wisdom: ' + repr(combatant.stats.wis))
    print_output('Charisma: ' + repr(combatant.stats.cha))
    print_output(' --------------------------------' )
    print_output('Weapon Proficiencies: ')
    for item in combatant.weapon_proficiency():
        print_indent( item.name)
    print_output('Weapons: ')
    for weapon in combatant.weapon_inventory():
        print_indent( weapon.name)
    print_output('Other Equipment: ')
    for item in combatant.equipment_inventory():                
        print_indent( item.name)
    print_output('---------------------------------')       
    print_output('Feats')
    for feat in combatant.creature_feats():
        print_indent( feat.name)
    #print_output('Rage Beyond Death: ' + repr(combatant.rage_beyond_death))
    #print_output('---------------------------------')
    print_output('Spells Known')    
    for spell in combatant.spell_list():                                       
        print_indent( spell.name) 
    print_output('Spellslots')    
    for spellslot in combatant.spellslots():                               
        if spellslot.level != 0:
            print_indent( numbered_list(spellslot.level) + ' Level Spellslots: ' + repr(spellslot.current))        
    print_output('</td>')

def print_summary(combatant):
    print_output('**************************')
    print_output(' Name: '  + combatant.fullname)
    print_output(' Team: '  + combatant.team.name)
    print_output(' Attacks Made: '  + repr(combatant.attacks_hit + combatant.attacks_missed))
    print_output(' Attacks Hit: '  + repr(combatant.attacks_hit))
    print_output(' Attacks Missed: '  + repr(combatant.attacks_missed))
    if combatant.attacks_hit > 0:
        print_output(' Hit Percentage: '  + repr(math.floor(combatant.attacks_hit/(combatant.attacks_hit + combatant.attacks_missed)*100)) + '%')    
    print_output(' Total Rounds Fought: '  + repr(combatant.rounds_fought))
    if combatant.rounds_fought > 0:
        print_output(' Average Damage per Round: '  + repr(math.floor(combatant.total_damage_dealt/combatant.rounds_fought)))    
    print_output(' Average Damage per Attempt: '  + repr(math.floor(combatant.total_damage_dealt/settings.max_attempts)))    
    print_output(' Total Damage Dealt: '  + repr(combatant.total_damage_dealt))

def print_grid(xorigin,yorigin,highlight_grids,targets):   
    target_grids = []
    target_ids = []
    for target in targets:
        name = target.name
        target_grids.append((target.xpos,target.ypos))        
        target_ids.append(hp_text(target.alive,target.current_health,target.max_health,target.name[0]))        
    #print_output(' Affected Grids ' + repr(highlight_grids))
    #Drawing grid from top left corner
    x = xorigin - 50
    y = yorigin + 50    
    #Initial line of grid showing starting co-ordinates    
    begin_div('grid_column')
    begin_div('grid')    
    print_output('Battlefield (origin point: ' + repr(xorigin) + ',' + repr(yorigin) + ')')
    while y > yorigin - 51:
        x = xorigin - 50        
        grid_line = ""
        while x < xorigin + 51: 
            if x == xorigin and y == yorigin:
                grid_line += ' O '
            elif (x,y) in highlight_grids and (x,y) in target_grids:
                list_index = target_grids.index((x,y))
                grid_line += target_ids[list_index]
            elif (x,y) in target_grids:
                list_index = target_grids.index((x,y))
                grid_line += target_ids[list_index]
            elif (x,y) in highlight_grids:
                grid_line += ' * '                               
            else:
                grid_line += ' . '        
            #grid_line += '(' + repr(x) + ',' + repr(y) + ')'        
            x += 5                
        print_output(grid_line)                    
        y -= 5        
    # End the Grid div
    end_div()
    # End the Grid Column div
    end_div()

def numbered_list(counter):
    suffix = ""
    if counter == 1:
        suffix = 'st'
    elif counter == 2:
        suffix = 'nd'
    elif counter == 3:
        suffix = 'rd'
    elif counter >= 4 and counter <= 9:
        suffix = 'th'
    return repr(counter) + suffix


def characterlevel(combatant):
    player_level = 0
    for class_instance in combatant.player_classes():
        player_level += class_instance.player_class_level
    return player_level

#Style functions
def print_indent(text):
    print_output('<span class="indent">' + text + '</span>')
def print_double_indent(text):
    print_output('<span class="double-indent">' + text + '</span>')

def movement_text(text):
    return '<span class="movement">' + text + '</span>'

def damage_text(text):
    return '<span class="damage">' + text + '</span>'

def crit_damage_text(text):
    return '<span class="crit_damage">' + text + '</span>'

def healing_text(text):
    return '<span class="healing">' + text + '</span>'

def dmgred_text(text):
    return '<span class="damage_reduction">' + text + '</span>'

def hp_text(alive,currenthp,maxhp,string=""):
    hp_string = ""
    if alive:
        if currenthp/maxhp >= 0.75:
            hp_string ='<span class="hpnormal">'
        elif currenthp/maxhp >= 0.5 and currenthp/maxhp < 0.75:
            hp_string ='<span class="hpmidrange">'
        elif currenthp >= 1 and currenthp/maxhp < 0.5:
            hp_string ='<span class="hplow">'
        elif currenthp <= 0:
            hp_string = '<span class="hpzero">'
    else:
        hp_string = '<span class="hpdead">'

    if string == "":
        hp_string += 'Current HP: ' + repr(currenthp) + '/' + repr(maxhp)+ '</span>'
    else:
        hp_string += string + '</span>'
    return hp_string

def position_text(xpos,ypos):
    return movement_text('Current Position: (' + repr(xpos) + ',' + repr(ypos) + ')')

def victory_text(text):
    return '<span class=victory_text>' + text + '</span>'

def killing_blow_text(text):
    return '<span class=hdywtdt>' + text + '</span>'

def print_horizontal_line():
    print_output(Markup('<hr>'))