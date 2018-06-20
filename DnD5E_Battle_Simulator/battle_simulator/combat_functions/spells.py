from battle_simulator import combatants
from battle_simulator.classes import * 
from battle_simulator.print_functions import * 
from battle_simulator.combat_functions.damage import * 
from battle_simulator.combat_functions.generics import *
from battle_simulator.combat_functions.position import *
import operator
from operator import attrgetter

def select_spell(combatant,casttime):
    best_spell = None
    #Check that the target is in a condition to warrant casting the spell on?
    if not check_condition(combatant.target,condition.Unconscious):    
        for spell in combatant.spell_list():
            if spell.casting_time == casttime:
                #Check that components (V,S,M) are available for spell?
                #Evaluate if spell is targetted or self (i.e. buff?)?
                # Only select spells we have a spellslot for
                spellslot = get_highest_spellslot(combatant,spell)
                #See if a spellslot was returned by the function
                if spellslot:    
                    #Check that target is in range of spell (spells with range 0 always satisfy this condition - i.e. Divine Smite is tied to attack)
                    if (spell.range == 0) or calc_distance(combatant,combatant.target) <= spell.range:                           
                        # Choose the first spell we find, or check the total potential damage of the spell to decide which one to use
                        if best_spell == None or (spell.instance*(spell.damage_die_count*spell.damage_die)) >= (best_spell.instance*(best_spell.damage_die_count*best_spell.damage_die)):
                            best_spell = spell
                    # It may be that the spell is currently out of range, but it could still be beneficial to close the gap and use that spell
                    # Apply a penalty to out-of-range spells to make us choose between a weaker, closer spell and a stronger one that forces us to close the gap
                    elif calc_distance(combatant,combatant.target) > spell.range:                    
                        range_penalty = 0.75
                        if best_spell == None or ((spell.instance*(spell.damage_die_count*spell.damage_die))*range_penalty) >= (best_spell.instance*(best_spell.damage_die_count*best_spell.damage_die)):
                            best_spell = spell
    return best_spell

#Cast a spell  - if Crit is forced use it
def cast_spell(combatant,spell,crit = None):
    #Check if a spell slot is available to be used
    #Always use highest level spellslot to cast spell (for now...)
    spellslot = get_highest_spellslot(combatant,spell)
    #See if a spellslot was returned by the function
    if spellslot:               
        # Deduct one usage from the spellslot (not cantrips)
        if spellslot.level == 0:
            print_output(indent() + spell.description + " " + combatant.target.name)
        else:
            #Consume the spell slot from player's available slots
            print_output(indent() + combatant.name + ' is burning a ' + numbered_list(spellslot.level) + ' level spellslot to cast ' + spell.name)                            
            spellslot.current -= 1

        # Make spell attack (if spell is an attack)
        if spell.spell_attack:            
            # Make one attack per instance
            i = 1
            while i <= spell.instance:
                spell_attack(combatant,combatant.target,spell,spellslot)
                i += 1                     
        else:
            # Automatically resolve spell damage on spells i.e. Divine Smite
            resolve_spell_damage(combatant,combatant.target,spell,spellslot,crit)
        #Resolve saving throw
        #if spell.saving_throw:
            #Resolve saving throw to see if damage/condition is applied                                                                                   

        #Resolve spell damage after attacks landed/saving throws failed and all instances are accounted for
        resolve_damage(combatant.target)

        #Check if we have spellslots left (except cantrips)
        if spellslot.level != 0 and spellslot.current == 0:
            print_output(combatant.name + ' has no ' + numbered_list(spellslot.level) + ' level spellslots remaining!')

def spell_attack(combatant,target,spell,spellslot):
    advantage = False
    disadvantage = False    
    crit = False

    advantage,disadvantage = determine_advantage(combatant,spell.range > 0)
    spell_hit_modifier = calc_spell_hit_modifier(combatant,spell)
    atkroll = attack_roll(combatant,advantage,disadvantage,spell_hit_modifier)    
    if atkroll == 20:
        crit = True
        print_output('************************')
        print_output('It\'s a CRITICAL ROLE!!!')
        print_output('************************')
    
    totalatk = atkroll + spell_hit_modifier;
    totalAC = calc_total_AC(target)
    if totalatk >= calc_total_AC(target):
        print_output(combatant.name + '\'s spell attack (' + repr(totalatk) + ') against '+ combatant.target.name + ' (AC ' + repr(totalAC) + ') with ' + spell.name + ' HIT!!!')
        resolve_spell_damage(combatant,combatant.target,spell,spellslot,crit)
        combatant.attacks_hit += 1
    else:        
        print_output(combatant.name + '\'s spell attack (' + repr(totalatk) + ') against ' + combatant.target.name +  ' (AC ' + repr(totalAC) + ') with ' + spell.name + ' MISSED!')        
        #Update statistics
        combatant.attacks_missed += 1


def calc_spell_hit_modifier(combatant,spell):
    to_hit_modifier = 0

    for spell_player_class in spell.player_classes():
        for player_class_block in combatant.player_classes():            
            if spell_player_class == player_class_block.player_class:
                player_spellcasting_attribute = player_class_block.spellcasting_attribute
    if player_spellcasting_attribute == attribute.Intelligence:
        to_hit_modifier = intmod(combatant)
    elif player_spellcasting_attribute == attribute.Wisdom:
        to_hit_modifier = wismod(combatant)
    elif player_spellcasting_attribute == attribute.Charisma:
        to_hit_modifier = chamod(combatant)

    to_hit_modifier += combatant.proficiency
    return (to_hit_modifier)

def get_highest_spellslot(combatant,spell):    
    # Sort spells by level (use highest slots first)
    initkey = operator.attrgetter("level")
    sorted_spells = sorted(combatant.spellslots(), key=initkey,reverse=True)    

    for spellslot in sorted_spells:
        if spellslot.level >= spell.min_spellslot_level:
            # 0 level spellslots are cantrips, and always returned. Otherwise we must have enough spells remaining
            if spellslot.level == 0 or spellslot.current > 0:
                return spellslot             