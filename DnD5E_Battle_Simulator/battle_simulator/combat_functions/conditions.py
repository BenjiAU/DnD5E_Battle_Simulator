#Explicit imports
from battle_simulator import combatants

#Implicit imports
from battle_simulator.classes import *
from battle_simulator.print_functions import *

def inflict_condition(combatant,source,condition,duration):
    combatant_condition = creature_condition()
    combatant_condition.source = source
    combatant_condition.condition = condition
    combatant_condition.duration = duration
    combatant.creature_conditions().append(combatant_condition)   
    print_output(indent() + combatant.name + ' is now affected by the ' + combatant_condition.condition.name + ' condition!')

def update_conditions(combatant):
    # Update the duration on all conditions
    for combatant_condition in combatant.creature_conditions():
        combatant_condition.duration -= 1 
        if combatant_condition.duration <= 0:
            print_output(indent() + 'The ' + combatant_condition.condition.name + ' condition affecting ' + combatant.name + ' wears off.')        

    # Mutate the list to remove conditions that have expired
    combatant.creature_conditions()[:] = [combatant_condition for combatant_condition in combatant.creature_conditions() if not combatant_condition.duration <= 0]

def check_condition(combatant,condition):
    for combatant_condition in combatant.creature_conditions():
        if combatant_condition.condition == condition:
            return True
    return False