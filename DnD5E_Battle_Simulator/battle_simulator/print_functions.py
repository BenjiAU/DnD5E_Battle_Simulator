import os
from os import path    
import time
import datetime

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
    print_output('Position: ' + repr(position)) 
    print_output(' Name: '  + combatant.fullname)
    print_output(' Race: '  + combatant.race.name)
    print_output(' Class: '  + combatant.creature_class.name)
    print_output(' Sub-class: '  + combatant.creature_subclass.name)
    print_output(' Max Hit Points: '  + repr(combatant.max_health))
    print_output(' --------------------------------' )
    print_output(' Stats: ')
    print_output(' Strength: ' + repr(combatant.stats.str))
    print_output(' Dexterity: ' + repr(combatant.stats.dex))
    print_output(' Constitution: ' + repr(combatant.stats.con))
    print_output(' Intelligence: ' + repr(combatant.stats.intel))
    print_output(' Wisdom: ' + repr(combatant.stats.wis))
    print_output(' Charisma: ' + repr(combatant.stats.cha))
    print_output('')            
    print_output(' Weapon Proficiencies: ')
    for item in combatant.weapon_proficiency():
        print_output(' Weapon Proficiency: ' + item.name)
    print_output('')
    print_output('')
    print_output(' Equipped Weapon: ' + combatant.current_weapon.name)
    print_output(' Other Weapons: ')
    for item in combatant.weapon_inventory():
        print_output(' Weapon: ' + item.name)
    print_output('')
    print_output(' Other Equipment: ')
    for item in combatant.equipment_inventory():                
        print_output(' Item: ' + item.name)
    print_output('')
    print_output('---------------------------------')       
    print_output('Feats')
    print_output('Rage Beyond Death: ' + repr(combatant.rage_beyond_death))