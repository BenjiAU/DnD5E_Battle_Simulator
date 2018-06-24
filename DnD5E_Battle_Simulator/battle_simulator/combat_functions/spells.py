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
                        if spell.category == spell_category.Healing:            
                            if best_spell == None or ((spell.instance*(spell.healing_die_count*spell.healing_die)) >= (best_spell.instance*(best_spell.healing_die_count*best_spell.healing_die))):
                                heal_target = find_heal_target(combatant,spell.range)
                                if heal_target != None:
                                    print_output(combatant.name + ' thinks that ' + heal_target.name + ' needs healing!')                     
                                    best_spell = spell

                        if spell.category == spell_category.Buff:                                        
                            if find_buff_target(combatant,condition,spell.range) != None:                                    
                                best_spell = spell

                        # AoE Debuffs                            
                        if spell.category == spell_category.AoE_Debuff:                                        
                            # Check targets, if more than 2 in AoE this is best spell
                            affected_targets = []                                                
                            affected_targets = calculate_area_effect(combatant,combatant.xpos,combatant.ypos,combatant.target.xpos,combatant.target.ypos,spell.shape,spell.shape_width,spell.shape_length)   
                            if len(affected_targets) >= 2:
                                best_spell = spell

                        # Single target debuffs
                        if spell.category == spell_category.Debuff:                                        
                            best_spell = spell

                        # Damage spells (only if we have no healing/buff/debuffs)
                        # AoE Damage
                        if spell.category == spell_category.AoE_Damage:                                        
                            # Check targets, if more than 2 in AoE this is best spell
                            affected_targets = []                                                
                            affected_targets = calculate_area_effect(combatant,combatant.xpos,combatant.ypos,combatant.target.xpos,combatant.target.ypos,spell.shape,spell.shape_width,spell.shape_length)   
                            if len(affected_targets) >= 2:
                                best_spell = spell
                            
                        # Single target damage
                        if spell.category == spell_category.Damage:                                                                                                        
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
                            else:
                                # Prefer non-spell attacks that have no save (i.e. magic missile)
                                if spell.saving_throw_attribute == 0:
                                    best_spell = spell
                                else:
                                    if best_spell == None or (spell.instance*(spell.damage_die_count*spell.damage_die)) >= (best_spell.instance*(best_spell.damage_die_count*best_spell.damage_die)):
                                        best_spell = spell
    return best_spell

#Cast a spell  - if Crit is forced use it
def cast_spell(combatant,spell,crit = None):    
    #Find the best spellslot to use on this spell
    spellslot = get_best_spellslot(combatant,spell)
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
        
        spellslot_bonus = 0
        if spellslot != None:
            if spellslot.level > spell.min_spellslot_level:
                # If the spell gains no benefit for spells higher than the maximum, we still burn the higher slot, but only get benefit from the maximum against the spell                
                if spell.max_spellslot_level < spellslot.level:
                    spellslot_bonus = spell.max_spellslot_level-spell.min_spellslot_level
                else:
                    spellslot_bonus = spellslot.level-spell.min_spellslot_level
                
        if spellslot_bonus > 0:
            total_instances = spell.instance + (spell.instance_per_spell_slot * spellslot_bonus)
        else:
            total_instances = spell.instance

        if spell.concentration:
            # Assign an identifier to the spell, so we can later cancel its effect across conditions            
            inflict_condition(combatant,spell_ID,condition.Concentrating,spell.maximum_duration)
        
        # Healing spells
        if spell.category == spell_category.Healing:            
            heal_target = find_heal_target(combatant,spell.range)
            print_output(combatant.name + ' casts the ' + spell.name + ' spell on ' + heal_target.name)

            if heal_target != None:
                i = 0
                while i < total_instances:
                    for x in range(0,spell.healing_die_count):
                        resolve_spell_healing(combatant,heal_target,spell,spellslot)                                                        
                    i += 1
            else:
                print_output('The spell fizzles as there is no target any more!')

        # Buff
        elif spell.category == spell_category.Buff:            
            #Apply the buff            
            buff_target = find_buff_target(combatant,spell.condition,spell.range)
            if buff_target != None:                
                print_output(combatant.name + ' casts the ' + spell.name + ' spell on ' + buff_target.name)
                inflict_condition(buff_target,spell_ID,spell.condition,spell.condition_duration)
            else:
                print_output('The spell fizzles as there is no target any more!')

        #Debuff
        elif spell.category == spell_category.Debuff:            
            # Check if a saving throw is defined
            if spell.saving_throw_attribute != 0:
                print_output(combatant.name + ' casts the ' + spell.name + ' spell on ' + combatant.target.name)
                if savingthrow(combatant.target,savetype,spell_save_DC(combatant,spell)):            
                    print_output(combatant.target.name + ' resists the effect of the ' + spell.name + ' spell!')
                else:
                    inflict_condition(combatant.target,spell_ID,spell.condition,spell.condition_duration,spell.repeat_save_action,spell.repeat_save_end_of_turn,spell.saving_throw_attribute,spell_save_DC(combatant,spell))
                    #Debuff spells may also have a damage component
                    if spell.damage_die != 0:
                        calculate_spell_damage(combatant,combatant.target,spell,spellslot,False)        
                        resolve_damage(combatant.target)
                        resolve_fatality(combatant.target)
            else:
                # No saving throw defined, automatic success
                inflict_condition(combatant.target,spell_ID,spell.condition,spell.condition_duration,spell.repeat_save_action,spell.repeat_save_end_of_turn,spell.saving_throw_attribute,spell_save_DC(combatant,spell))

        # AoE Debuff spell
        elif spell.category == spell_category.AoE_Debuff:
            affected_targets = []
            xorigin = 0
            yorigin = 0
            # Determine point of origin
            # Determine target point
            # Determine AoE
            # Find affected targets
            if spell.origin == origin_point.Self:
                xorigin = comabtant.xpos
                yorigin = combatant.ypos

            affected_targets = calculate_area_effect(combatant,xorigin,yorigin,combatant.target.xpos,combatant.target.ypos,spell.shape,spell.shape_width,spell.shape_length,True)   
                
            for affected_target in affected_targets:    
                print_output(affected_target.name + ' is in the affected area (located at (' + repr(affected_target.xpos) + ',' + repr(affected_target.ypos) + ')')   
                # Check if a saving throw is defined
                if spell.saving_throw_attribute != 0:
                    print_output(combatant.name + ' casts the ' + spell.name + ' spell on ' + combatant.target.name)
                    if savingthrow(combatant.target,savetype,spell_save_DC(combatant,spell)):            
                        print_output(combatant.target.name + ' resists the effect of the ' + spell.name + ' spell!')
                    else:
                        inflict_condition(combatant.target,spell_ID,spell.condition,spell.condition_duration,spell.repeat_save_action,spell.repeat_save_end_of_turn,spell.saving_throw_attribute,spell_save_DC(combatant,spell))
                        #Debuff spells may also have a damage component
                        if spell.damage_die != 0:
                            calculate_spell_damage(combatant,affected_target,spell,spellslot,False)        
                            resolve_spell_damage(affected_target)                            
                else:
                    # No saving throw defined, automatic success
                    inflict_condition(combatant.target,spell_ID,spell.condition,spell.condition_duration,spell.repeat_save_action,spell.repeat_save_end_of_turn,spell.saving_throw_attribute,spell_save_DC(combatant,spell))
        # AoE Damage spell
        elif spell.category == spell_category.AoE_Damage:
            affected_targets = []
            xorigin = 0
            yorigin = 0
            # Determine point of origin
            # Determine target point
            # Determine AoE
            # Find affected targets
            if spell.origin == origin_point.Self:
                xorigin = comabtant.xpos
                yorigin = combatant.ypos

            affected_targets = calculate_area_effect(combatant,xorigin,yorigin,combatant.target.xpos,combatant.target.ypos,spell.shape,spell.shape_width,spell.shape_length,True)   

            # Apply damage to targets
            for affected_target in affected_targets:    
                print_output(affected_target.name + ' is in the affected area (located at (' + repr(affected_target.xpos) + ',' + repr(affected_target.ypos) + ')')   
                if spell.saving_throw_attribute != 0:
                    if savingthrow(affected_target,spell.saving_throw_attribute,spell_save_DC(combatant,spell)):
                        #If target has evasion and saves, nothing happens
                        if (spell.saving_throw_attribute == saving_throw.Dexterity and affected_target.evasion) or (spell.saving_throw_damage_multiplier == 0):
                            print_output(affected_target.name + ' resists all damage from the spell!') 
                        else:                
                            print_output(affected_target.name + ' resists some damage from the spell!') 
                            calculate_spell_damage(combatant,affected_target,spell,spellslot,False,spell.saving_throw_damage_multiplier)                
                    else:
                        if spell.saving_throw_attribute == saving_throw.Dexterity and affected_target.evasion:
                            print_output(affected_target.name + ' avoids half the damage thanks to Evasion!')
                            calculate_spell_damage(combatant,affected_target,spell,spellslot,False,0.5)              
                        else:
                            # Full damage
                            calculate_spell_damage(combatant,affected_target,spell,spellslot,False) 
                else:
                    # Damage automatically applies
                    calculate_spell_damage(combatant,affected_target,spell,spellslot,False,spell.saving_throw_damage_multiplier)         

                # Resolve damage against the target
                resolve_damage(affected_target)
                resolve_fatality(affected_target)
        # Direct damage spell
        elif spell.category == spell_category.Damage:
            if spell.spell_attack:
                i = 0
                while i < total_instances:
                    spell_attack(combatant,combatant.target,spell,spellslot)
                    i += 1
            else:
                i = 0
                while i < total_instances:
                    # Check if a saving throw is defined
                    if spell.saving_throw_attribute != 0:                    
                        if savingthrow(combatant.target,savetype,spell_save_DC(combatant,spell)):            
                            # If save successful, check the damage multiplier; multiplier of 0 means no damage
                            if spell.saving_throw_damage_multiplier == 0:                
                                print_output(combatant.target.name + ' resists all damage from the spell!') 
                            else:
                                calculate_spell_damage(combatant,combatant.target,spell,spellslot,False,spell.saving_throw_damage_multiplier)                
                        else:
                            # Failed save
                            calculate_spell_damage(combatant,combatant.target,spell,spellslot,False)                
                    # No saving throw defined - damage applies automatically (i.e. Divine Smite)
                    else:
                        calculate_spell_damage(combatant,combatant.target,spell,spellslot,False)            
                    i += 1

                # Resolve damage against the target
                resolve_damage(combatant.target)
                resolve_fatality(combatant.target)

            # Resolve damage against the target
            resolve_damage(combatant.target)
            resolve_fatality(combatant.target)
            
        #Silently update concentration; if all targets saved aagainst the effect we need to immediately stop concentrating
        update_concentration(combatant)

        #Resolve spell damage and fatalities after attacks landed/saving throws failed and all instances are accounted for
        if spell.category == spell_category.Damage or spell.category == spell_category.AoE_Damage:
            resolve_damage(combatant.target)
            

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
        calculate_spell_damage(combatant,combatant.target,spell,spellslot,crit)
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


def get_best_spellslot(combatant,spell):    
    # Sort spells by level then selects the one that fits within min/max bounds (so you dont burn higher level spellslots for no reason)
    initkey = operator.attrgetter("level")
    sorted_spells = sorted(combatant.spellslots(), key=initkey,reverse=True)    

    best_spellslot = None
    for spellslot in sorted_spells:
        if spellslot.level >= spell.min_spellslot_level and spellslot.level <= spell.max_spellslot_level:
            # 0 level spellslots are cantrips, and always returned. Otherwise we must have enough spells remaining
            if spellslot.current > 0:
                if best_spellslot == None or spellslot.level > best_spellslot.level:
                    best_spellslot = spellslot

    return best_spellslot

def new_spell_ID():
    ID = settings.last_spell_ID + 1
    settings.last_spell_ID = ID
    return ID
