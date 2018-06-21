#Explicit imports
from battle_simulator import combatants

#Implicit imports
from battle_simulator.classes import *
from battle_simulator.print_functions import *

def inflict_condition(combatant,source,condition,duration=0,grants_advantage=False,grants_disadvantage=False):
    condition_inflicted = False
    for combatant_condition in combatant.creature_conditions():
        if combatant_condition.condition == condition:
            if combatant_condition.source != source:
                if combatant_condition.limited_duration and combatant_condition.duration < duration:
                    #Overwrite the current condition with the new condition and duration
                    combatant_condition.source = source
                    combatant_condition.duration = duration
                    
                    print_output(indent() + combatant.name + ' is affected by a new instance of the ' + combatant_condition.condition.name + ' condition! It\'s duration has been refreshed!')
                    condition_inflicted = True
                elif combatant_condition.limited_duration and not combatant_condition.duration < duration:
                    # The new condition has a shorter duration than the one being suffered; output a message
                    print_output(indent() + combatant.name + ' is already ' + combatant_condition.condition.name + '!')
                    condition_inflicted = True
                else:
                    #The condition has already been inflicted on the target, do not output a message
                    condition_inflicted = True
                    
    if not condition_inflicted:
        combatant_condition = creature_condition()
        combatant_condition.source = source
        combatant_condition.condition = condition
        if duration != 0:
            combatant_condition.limited_duration = True
        else:
            combatant_condition.limited_duration = False
        combatant_condition.duration = duration    
        combatant_condition.grants_advantage = grants_advantage
        combatant_condition.grants_disadvantage = grants_disadvantage
        combatant.creature_conditions().append(combatant_condition)   
        print_output(indent() + combatant.name + ' is now ' + combatant_condition.condition.name + '!')

def remove_condition(combatant,condition_to_remove):
    # Mutate the condition list against the creature to exclude the condition/conditions to remove
    # On the off chance multiple instances of the same condition are recorded against the target this will remove all instances of them 
    if check_condition(combatant,condition_to_remove):
        combatant.creature_conditions()[:] = [combatant_condition for combatant_condition in combatant.creature_conditions() if not combatant_condition.condition == condition_to_remove]    
        print_output(indent() + combatant.name + ' is no longer ' + condition_to_remove.name + '!')

def update_conditions(combatant):
    # Update the duration on all limited-duration conditions
    for combatant_condition in combatant.creature_conditions():
        # Conditions that are inflicted with a duration of 0 are 
        if combatant_condition.limited_duration and combatant_condition.duration > 0:
            combatant_condition.duration -= 1 
            if combatant_condition.duration <= 0:
                print_output(indent() + 'The ' + combatant_condition.condition.name + ' condition affecting ' + combatant.name + ' wears off.')        

    # Mutate the list to remove conditions that have expired
    combatant.creature_conditions()[:] = [combatant_condition for combatant_condition in combatant.creature_conditions() if combatant_condition.limited_duration and not combatant_condition.duration <= 0]

#Return true/false if the condition affects the combatant
def check_condition(combatant,condition):
    for combatant_condition in combatant.creature_conditions():
        if combatant_condition.condition == condition:
            return True
    return False
