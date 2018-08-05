#Explicit imports
from battle_simulator import combatants

#Implicit imports
from battle_simulator.classes import *
from battle_simulator.print_functions import *

def inflict_condition(combatant,source,condition,duration=0,save_action=False,save_end_of_turn=False,saving_throw_attribute=0,saving_throw_DC=0):
    condition_inflicted = False
    for combatant_condition in combatant.creature_conditions():
        if combatant_condition.condition == condition:
            if combatant_condition.limited_duration and combatant_condition.duration < duration:
                #Overwrite the current condition with the new condition and duration
                combatant_condition.source = source
                combatant_condition.duration = duration
                    
                print_indent( combatant.name + ' is affected by a new instance of the ' + combatant_condition.condition.name + ' condition! It\'s duration has been refreshed!')
                condition_inflicted = True
            elif combatant_condition.limited_duration and combatant_condition.duration >= duration:
                # The new condition has a shorter duration than the one being suffered; output a message
                print_indent( combatant.name + ' is already ' + combatant_condition.condition.name + '!')
                condition_inflicted = True
            else:
                #The condition has already been inflicted on the target, do not output a message
                condition_inflicted = True

    if not condition_inflicted:                    
    # Set advantage/disadvantage
        grants_advantage = False
        grants_disadvantage = False

        if condition in [condition.Restrained,condition.Headshot]:
            grants_disadvantage = True
        
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

        #Save information for conditions inflicted via spells/abilities
        combatant_condition.save_action = save_action
        combatant_condition.save_end_of_turn = save_end_of_turn
        combatant_condition.saving_throw_attribute = saving_throw_attribute
        combatant_condition.saving_throw_DC = saving_throw_DC
        
        #Special property of Haste
        if condition == condition.Hasted:
            combatant_condition.grants_action = True
            combatant_condition.granted_action_used = False
        combatant.creature_conditions().append(combatant_condition)   
        print_indent( combatant.name + ' is now ' + combatant_condition.condition.name + '!')

def remove_condition(combatant,condition_to_remove):
    if condition_to_remove == condition.Concentrating:
        end_concentration(combatant)        

    # Mutate the condition list against the creature to exclude the condition/conditions to remove
    # On the off chance multiple instances of the same condition are recorded against the target this will remove all instances of them     
    if check_condition(combatant,condition_to_remove):
        combatant.creature_conditions()[:] = [combatant_condition for combatant_condition in combatant.creature_conditions() if not combatant_condition.condition == condition_to_remove]    
        print_indent( combatant.name + ' is no longer ' + condition_to_remove.name + '!')    
        # Special rule of Haste - after expiry, inflict Stun
        if condition_to_remove == condition.Hasted:
            print_indent( 'As Haste wears off, ' + combatant.name + ' is Stunned!')        
            inflict_condition(combatant,combatant,condition.Stunned,1)
            inflict_condition(combatant,combatant,condition.Incapacitated,1)

def get_concentration_condition(combatant):
    concentration_condition = None
    for combatant_condition in combatant.creature_conditions():
        if combatant_condition.condition == condition.Concentrating:
            concentration_condition = combatant_condition
            return concentration_condition
    return None

def end_concentration(combatant):
    concentration_condition = get_concentration_condition(combatant)

    if concentration_condition != None:
        #Concentration is inflicted by the spell; look across all other targets for instances of that spell_id and remove them if required                
        for spell_effect_combatant in combatants.list:
            for spell_effect in spell_effect_combatant.creature_conditions():                    
                if spell_effect.source == concentration_condition.source and spell_effect.condition != condition.Concentrating:
                    remove_condition(spell_effect_combatant,spell_effect.condition)            
    
def update_concentration(combatant):
    # Returns True if we're still concentrating on an active spell effect; returns False and removes the Concentration condition if we are not
    concentration_condition = get_concentration_condition(combatant)

    if concentration_condition != None:    
        for spell_effect_combatant in combatants.list:
            for spell_effect in spell_effect_combatant.creature_conditions():                    
                if spell_effect.source == concentration_condition.source and spell_effect.condition != condition.Concentrating:
                    return True
    
        # There are no current active spell effects relying on our concentration; safe to remove concentration           
        combatant.creature_conditions()[:] = [combatant_condition for combatant_condition in combatant.creature_conditions() if not combatant_condition.condition == concentration_condition.condition]
        print_output('The spell effects maintained by ' + combatant.name + ' have worn off.')
        print_indent(combatant.name + ' is no longer Concentrating!')
        return False

def update_conditions(combatant):
    # Update the duration on all limited-duration conditions
    for combatant_condition in combatant.creature_conditions():
        # Conditions that are inflicted with a duration of 0 are 
        if combatant_condition.limited_duration and combatant_condition.duration > 0:
            combatant_condition.duration -= 1 
            if combatant_condition.duration <= 0:
                print_indent( 'The ' + combatant_condition.condition.name + ' condition affecting ' + combatant.name + ' wears off.')        
            # Special rule of Haste - after expiry, inflict Stun
                if combatant_condition.condition == condition.Hasted:
                    print_indent( 'As Haste wears off, ' + combatant.name + ' is Stunned!')        
                    inflict_condition(combatant,combatant,condition.Stunned,1)
                    inflict_condition(combatant,combatant,condition.Incapacitated,1)

    # Mutate the list to remove conditions that have expired
    combatant.creature_conditions()[:] = [combatant_condition for combatant_condition in combatant.creature_conditions() if combatant_condition.limited_duration and not combatant_condition.duration <= 0]

#Return true/false if the condition affects the combatant
def check_condition(combatant,condition,from_source=None):
    for combatant_condition in combatant.creature_conditions():
        if combatant_condition.condition == condition:
            return True
    return False

def check_inflicted_condition(combatant,target,condition):    
    for combatant_condition in target.creature_conditions():
        if combatant_condition.condition == condition:    
            concentration_condition = get_concentration_condition(combatant)
            if concentration_condition.source == combatant_condition.source:
                return True
    return False

def action_saveable_condition(combatant):
    for combatant_condition in combatant.creature_conditions():    
        if combatant_condition.save_action:
            return combatant_condition
    return None