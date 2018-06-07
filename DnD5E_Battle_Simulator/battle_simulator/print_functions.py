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
    if settings.filename != "":
        if not settings.file_open:
            open_file()      
        print(string,file=settings.file)
        settings.output.append(string)
    else:
        print(string)
        settings.output.append(string)

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
    string = ""
    string += Markup('<div class=combatant>')    
    string += Markup('<tr>')
    string += Markup('<td>')
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

def print_combatant_details(combatant,position):
    print_output('**************************')
    print_output('Position: ' + repr(position)) 
    print_output(' Name: '  + combatant.fullname)
    print_output(' Team: '  + combatant.team.name)
    print_output(' Race: '  + combatant.race.name)
    print_output(' Character Level ' + repr(characterlevel(combatant)))
    print_output(' Class Breakdown: ')
    for class_instance in combatant.player_classes():
        print_output(indent() + ' Class: '  + class_instance.player_class.name)
        if class_instance.player_subclass:
            print_output(doubleindent() + ' Sub-class: '  + class_instance.player_subclass.name)
        print_output(doubleindent() + ' Level: '  + repr(class_instance.player_class_level))
        print_output('')
    print_output(' Max Hit Points: '  + repr(combatant.max_health))
    print_output(' --------------------------------' )
    print_output(' Stats: ')
    print_output(' Strength: ' + repr(combatant.stats.str))
    print_output(' Dexterity: ' + repr(combatant.stats.dex))
    print_output(' Constitution: ' + repr(combatant.stats.con))
    print_output(' Intelligence: ' + repr(combatant.stats.intel))
    print_output(' Wisdom: ' + repr(combatant.stats.wis))
    print_output(' Charisma: ' + repr(combatant.stats.cha))
    print_output(' --------------------------------' )
    print_output('')            
    print_output(' Weapon Proficiencies: ')
    for item in combatant.weapon_proficiency():
        print_output(indent() + item.name)
    print_output('')
    print_output('')    
    print_output(' Weapons: ')
    for weapon in combatant.weapon_inventory():
        print_output(indent() + weapon.name)
    print_output('')
    print_output(' Other Equipment: ')
    for item in combatant.equipment_inventory():                
        print_output(indent() + item.name)
    print_output('')
    print_output('---------------------------------')       
    print_output('Feats')
    for feat in combatant.creature_feats():
        print_output(indent() + feat.name)
    #print_output('Rage Beyond Death: ' + repr(combatant.rage_beyond_death))
    #print_output('---------------------------------')
    print_output('Spellslots')    
    for spellslot in combatant.spellslots():                               
        print_output(indent() + numbered_list(spellslot.level) + ' Level Spellslots: ' + repr(spellslot.current))        
    print_output('**************************')

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
    print_output(' Average Damage per Round: '  + repr(math.floor(combatant.total_damage_dealt/combatant.rounds_fought)))    
    print_output(' Average Damage per Attempt: '  + repr(math.floor(combatant.total_damage_dealt/settings.max_attempts)))    
    print_output(' Total Damage Dealt: '  + repr(combatant.total_damage_dealt))

def print_grid(xorigin,yorigin,highlight_grids,targets):   
    target_grids = []
    for target in targets:
        target_grids.append((target.xpos,target.ypos))
    #print_output(' Affected Grids ' + repr(highlight_grids))
    #Drawing grid from top left corner
    x = xorigin - 40
    y = yorigin + 40    
    #Initial line of grid showing starting co-ordinates
    grid_line = '<div class=grid>AoE Grid (centered on origin point: ' + repr(xorigin) + ',' + repr(yorigin) + ')'
    print_output(grid_line)
    grid_line = '<div class=grid>Legend: O = Origin, X = Affected Target, A = Affected Area, T = Unaffected Target, . = Empty'
    print_output(grid_line)    
    grid_line = '<div class=grid>'
    while y > yorigin - 41:
        x = xorigin - 40        
        while x < xorigin + 41:
            if x == xorigin and y == yorigin:
                grid_line += ' O '
            elif (x,y) in highlight_grids and (x,y) in target_grids:
                grid_line += ' X '        
            elif (x,y) in target_grids:
                grid_line += ' T '         
            elif (x,y) in highlight_grids:
                grid_line += ' A '                               
            else:
                grid_line += ' . '        
            #grid_line += '(' + repr(x) + ',' + repr(y) + ')'        
            x += 5        
        print_output(grid_line)            
        grid_line = '<div class=grid>'
        y -= 5

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
def indent():
    return '<div class="indent">'

def doubleindent():
    return '<div class="doubleindent">'

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

def hp_text(currenthp,maxhp):
    if currenthp/maxhp >= 0.75:
        return '<span class="hpnormal">Current HP: ' + repr(currenthp) + '/' + repr(maxhp)+ '</span>'
    elif currenthp/maxhp >= 0.5 and currenthp/maxhp < 0.75:
        return '<span class="hpmidrange">Current HP: ' + repr(currenthp) + '/' + repr(maxhp)+ '</span>'
    elif currenthp >= 1 and currenthp/maxhp < 0.5:
        return '<span class="hplow">Current HP: ' + repr(currenthp) + '/' + repr(maxhp)+ '</span>'
    elif currenthp <= 0:
        return '<span class="hpdead">Current HP: ' + repr(currenthp) + '/' + repr(maxhp)+ '</span>'

def victory_text(text):
    return '<span class=victory_text>' + text + '</span>'

def killing_blow_text(text):
    return '<span class=hdywtdt>' + text + '</span>'