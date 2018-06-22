from battle_simulator import combatants
from battle_simulator.classes import * 
from battle_simulator.print_functions import * 
from battle_simulator.combat_functions.damage import * 
from battle_simulator.combat_functions.generics import *
from battle_simulator.combat_functions.position import *
from battle_simulator.combat_functions.target import *
import operator
from operator import attrgetter

def select_spell(combatant,casttime):
    best_spell = None
    #Check that the target is in a condition to warrant casting the spell on?
    if not check_condition(combatant.target,condition.Unconscious):    
        for spell in combatant.spell_list():
            if spell.casting_time == casttime:
                #If we already used our bonus action this turn to cast a spell, we can only cast 1 action speed cantrips on our action
                if combatant.bonus_action_spell_casted and not spell.cantrip:
                    break

                #Check that components (V,S,M) are available for spell?
                #Evaluate if spell is targetted or self (i.e. buff?)?
                # Only select spells we have a spellslot for
                spellslot = get_highest_spellslot(combatant,spell)
                #See if a spellslot was returned by the function
                if spell.cantrip or spellslot:    
                    # Check Concentrating
                    if not spell.concentration or (spell.concentration and not check_condition(combatant,condition.Concentrating)):
                        #Always choose higher level spells first
                        if best_spell == None or (best_spell != None and spell.min_spellslot_level >= best_spell.min_spellslot_level):
                            #Healing spells first:
                            # Healing spell                            
                            if spell.healing_die != 0:
                                if best_spell == None or ((spell.instance*(spell.healing_die_count*spell.healing_die)) >= (best_spell.instance*(best_spell.healing_die_count*best_spell.healing_die))):
                                    heal_target = find_heal_target(combatant,spell.range)
                                    if heal_target != None:
                                        print_output(combatant.name + ' thinks that ' + heal_target.name + ' needs healing!')                     
                                        best_spell = spell

                            # Buff spells                            
                            if spell.condition != 0 and spell.saving_throw_attribute == 0:                                                                                    
                                if find_buff_target(combatant,condition,spell.range) != None:                                    
                                    best_spell = spell

                            # Debuff/saving throw spells                            
                            if spell.condition != 0:
                                best_spell = spell

                            # Direct damage/save forcing spells:
                            if best_spell == None:
                                if spell.damage_die != 0 and spell.saving_throw_attribute != 0 and not spell.spell_attack:
                                    best_spell = spell

                                if spell.spell_attack:
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
    if spell.cantrip or spellslot:               
        # Deduct one usage from the spellslot (not cantrips)
        if spell.cantrip:
            print_indent( spell.description + " " + combatant.target.name)
        else:
            #Consume the spell slot from player's available slots
            print_indent( combatant.name + ' is burning a ' + numbered_list(spellslot.level) + ' level spellslot to cast ' + spell.name)                            
            spellslot.current -= 1
        
        spell_ID = new_spell_ID()
        savetype = saving_throw.Strength
        if spell.saving_throw_attribute != 0:
            savetype = saving_throw(spell.saving_throw_attribute)

        if spell.concentration:
            # Assign an identifier to the spell, so we can later cancel its effect across conditions            
            inflict_condition(combatant,spell_ID,condition.Concentrating,spell.maximum_duration)

        if spell.healing_die != 0:
            heal_target = find_heal_target(combatant,spell.range)

            if heal_target != None:
                i = 1
                while i <= spell.instance:
                    for x in range(0,spell.healing_die_count):
                        resolve_spell_healing(combatant,heal_target,spell,spellslot)                                    
                    i += 1                     
            else:
                print_output('The spell fizzles as there is no target any more!')

        # Buff/debuff
        elif spell.condition != 0:
            #Apply the buff
            if spell.saving_throw_attribute == 0:
                buff_target = find_buff_target(combatant,spell.condition,spell.range)
                if buff_target != None:                
                    print_output(combatant.name + ' casts the ' + spell.name + ' spell on ' + buff_target.name)
                    inflict_condition(buff_target,spell_ID,spell.condition,spell.condition_duration)
                else:
                    print_output('The spell fizzles as there is no target any more!')
            #Attempt to apply the debuff
            else:
                print_output(combatant.name + ' casts the ' + spell.name + ' spell on ' + combatant.target.name)
                if savingthrow(combatant.target,savetype,spell_save_DC(combatant,spell)):            
                    print_output(combatant.target.name + ' resists the effect of the ' + spell.name + ' spell!')
                else:
                    inflict_condition(combatant.target,spell_ID,spell.condition,spell.condition_duration)
        # Direct damage spell (just binary save)
        elif spell.saving_throw_attribute != 0 and not spell.spell_attack:            
            print_output(combatant.name + ' casts the ' + spell.name + ' spell on ' + combatant.target.name)
            if savingthrow(combatant.target,savetype,spell_save_DC(combatant,spell)):            
                print_output(combatant.target.name + ' resists the effect of the ' + spell.name + ' spell!')
            else:
                resolve_spell_damage(combatant,combatant.target,spell,spellslot,False)                
        # Make spell attack (if spell is an attack)
        elif spell.spell_attack:            
            # Make one attack per instance
            i = 1
            while i <= spell.instance:
                spell_attack(combatant,combatant.target,spell,spellslot)
                i += 1                     
        else:
            # Automatically resolve spell damage on spells that have no healing, are not spell attacks, do not inflict conditions, and have no save
            # i.e. Divine Smite
            resolve_spell_damage(combatant,combatant.target,spell,spellslot,crit)
        #Resolve saving throw
        #if spell.saving_throw:
            #Resolve saving throw to see if damage/condition is applied                                                                                   

        #Resolve spell damage and fatalities after attacks landed/saving throws failed and all instances are accounted for
        resolve_damage(combatant.target)
        resolve_fatality(combatant.target)

        #Check if we have spellslots left (except cantrips)
        if spellslot != None:
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

    to_hit_modifier += spellcasting_ability_modifier(combatant,spell)    

    to_hit_modifier += combatant.proficiency
    return (to_hit_modifier)

def get_highest_spellslot(combatant,spell):    
    # Sort spells by level (use highest slots first)
    initkey = operator.attrgetter("level")
    sorted_spells = sorted(combatant.spellslots(), key=initkey,reverse=True)    

    for spellslot in sorted_spells:
        if spellslot.level >= spell.min_spellslot_level:
            # 0 level spellslots are cantrips, and always returned. Otherwise we must have enough spells remaining
            if spellslot.current > 0:
                return spellslot             

def new_spell_ID():
    ID = settings.last_spell_ID + 1
    settings.last_spell_ID = ID
    return ID
