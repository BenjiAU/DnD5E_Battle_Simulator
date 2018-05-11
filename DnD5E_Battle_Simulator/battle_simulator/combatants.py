#This module keeps the current list of combatant information for other modules to access

from battle_simulator import fighters

#Generic combat initialisation functions
from battle_simulator import initialise_combat

# Combat functions
from battle_simulator import combat_functions

#System imports
import operator
from operator import itemgetter, attrgetter, methodcaller

combatants = []

def default_simulation():
    fighters.initialise_combatants(combatants)
    fighters.initialise_team(combatants)
    # Hard-coded initialisation functions for combatants
    initialise_position()

def reset_combatants():
    initialise_combat.reset_combatants(combatants)

def initialise_position():
    fighters.initialise_position(combatants)

def get_combatants():
    return(combatants)

def set_initiative_order():
    unsorted_combatants = combatants
    #Roll initiative for each combatant
    for combatant in unsorted_combatants:     
        combat_functions.roll_initiative(combatant)            
                            
    initkey = operator.attrgetter("initiative_roll")
    combatants = sorted(unsorted_combatants, key=initkey,reverse=True)