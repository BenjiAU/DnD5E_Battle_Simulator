import os
from os import path    
import time
import datetime
import math

from battle_simulator import settings

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

def close_file():
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

def print_details(combatant,position):
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
    print_output(' Hit Percentage: '  + repr(math.floor(combatant.attacks_hit/(combatant.attacks_hit + combatant.attacks_missed)*100)) + '%')    
    print_output(' Total Rounds Fought: '  + repr(combatant.rounds_fought))
    print_output(' Average Damage per Round: '  + repr(math.floor(combatant.total_damage_dealt/combatant.rounds_fought)))    
    print_output(' Average Damage per Attempt: '  + repr(math.floor(combatant.total_damage_dealt/settings.max_attempts)))    
    print_output(' Total Damage Dealt: '  + repr(combatant.total_damage_dealt))

def indent():
    return '<div class="indent">'

def doubleindent():
    return '<div class="doubleindent">'

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