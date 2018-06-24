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
                    
                    print_indent( combatant.name + ' is affected by a new instance of the ' + combatant_condition.condition.name + ' condition! It\'s duration has been refreshed!')
                    condition_inflicted = True
                elif combatant_condition.limited_duration and not combatant_condition.duration < duration:
                    # The new condition has a shorter duration than the one being suffered; output a message
                    print_indent( combatant.name + ' is already ' + combatant_condition.condition.name + '!')
                    condition_inflicted = True
                else:
                    #The condition has already been inflicted on the target, do not output a message
                    condition_inflicted = True
                    
    # Set condition properties here?
    if condition == condition.Restrained:
        grants_disadvantage = True

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
        
        #Special property of Haste
        if condition == condition.Hasted:
            combatant_condition.grants_action = True
            combatant_condition.granted_action_used = False
        combatant.creature_conditions().append(combatant_condition)   
        print_indent( combatant.name + ' is now ' + combatant_condition.condition.name + '!')

def remove_condition(combatant,condition_to_remove):
    #Concentration is inflicted by the spell; look across all other targets for instances of that spell and remove them if required
    if condition_to_remove == condition.Concentrating:
        # Retrieve the concentration object so we can access the source
        concentration_condition = None
        for combatant_condition in combatant.creature_conditions():
           if combatant_condition.condition == condition_to_remove:
                concentration_condition = combatant_condition

        if concentration_condition != None:
            for spell_effect_combatant in combatants.list:
                for spell_effect in spell_effect_combatant.creature_conditions():
                    # Avoid recursion
                    if spell_effect.source == concentration_condition.source and spell_effect.condition != condition_to_remove:
                        remove_condition(spell_effect_combatant,spell_effect.condition)

    # Mutate the condition list against the creature to exclude the condition/conditions to remove
    # On the off chance multiple instances of the same condition are recorded against the target this will remove all instances of them     
    if check_condition(combatant,condition_to_remove):
        combatant.creature_conditions()[:] = [combatant_condition for combatant_condition in combatant.creature_conditions() if not combatant_condition.condition == condition_to_remove]    
        print_indent( combatant.name + ' is no longer ' + condition_to_remove.name + '!')    

        
def update_conditions(combatant):
    # Update the duration on all limited-duration conditions
    for combatant_condition in combatant.creature_conditions():
        # Conditions that are inflicted with a duration of 0 are 
        if combatant_condition.limited_duration and combatant_condition.duration > 0:
            combatant_condition.duration -= 1 
            if combatant_condition.duration <= 0:
                print_indent( 'The ' + combatant_condition.condition.name + ' condition affecting ' + combatant.name + ' wears off.')        

    # Mutate the list to remove conditions that have expired
    combatant.creature_conditions()[:] = [combatant_condition for combatant_condition in combatant.creature_conditions() if combatant_condition.limited_duration and not combatant_condition.duration <= 0]

#Return true/false if the condition affects the combatant
def check_condition(combatant,condition):
    for combatant_condition in combatant.creature_conditions():
        if combatant_condition.condition == condition:
            return True
    return False
