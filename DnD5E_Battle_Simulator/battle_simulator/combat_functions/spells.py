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
    initkey = operator.attrgetter("min_spellslot_level")
    spells_by_min_spellslot_level = sorted(combatant.spell_list(), key=initkey,reverse=True)    

    for spell in spells_by_min_spellslot_level:
        if spell.casting_time == casttime:
            #If we already used our bonus action this turn to cast a spell, we can only cast 1 action speed cantrips on our action
            if combatant.bonus_action_spell_casted and not spell.cantrip:
                break

            #Check that components (V,S,M) are available for spell?
            #Evaluate if spell is targetted or self (i.e. buff?)?
            # Only select spells we have a spellslot for
            spellslot = get_highest_spellslot(combatant,spell)
            #See if a spellslot was returned by the function
            if spell.cantrip or spell.min_spellslot_level == 0 or spellslot:    
                # Check Concentrating
                if not spell.concentration or (spell.concentration and not check_condition(combatant,condition.Concentrating)):
                    # Run through the list at least once to find a spell
                    # Then, only consider the spell if it is of a higher minimum level than the previous spell
                    if best_spell == None or (best_spell != None and spell.min_spellslot_level >= best_spell.min_spellslot_level):                        
                        # Consider each spell in the list, considering the least-preferable spells first, and the most preferable last
                        # Healing > Buffs > AoE Debuffs > Debuffs > AoE Damage > Single target Damage (save) > Single target damage (spell attack)
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

                        # Damage spells (only if we have no healing/buff/debuffs)
                        # AoE Damage
                        if spell.category == spell_category.AoE_Damage:                                        
                            # Check targets, if we can find a target, choose this spell
                            affected_targets = []                                                
                            affected_targets = calculate_area_effect(combatant,combatant.xpos,combatant.ypos,combatant.target.xpos,combatant.target.ypos,spell.shape,spell.shape_width,spell.shape_length)   
                            if len(affected_targets) >= 1:
                                best_spell = spell

                        # Single target debuffs, i.e. Hold Person
                        if spell.category == spell_category.Debuff:                                        
                            # Don't consider this spell if the condition is already on the target
                            if not check_condition(combatant.target,spell.condition):
                                # Prioritise debuff spells based on condition? Sometimes we may want to do damage instead if a condition effects the target
                                if spell.condition == condition.Restrained:
                                    best_spell = spell
                                else:                                    
                                    best_spell = spell

                        # AoE Debuffs, i.e. Slow
                        if spell.category == spell_category.AoE_Debuff:                                        
                            # Check targets, if more than 2 in AoE this is best spell
                            affected_targets = []                                                
                            affected_targets = calculate_area_effect(combatant,combatant.xpos,combatant.ypos,combatant.target.xpos,combatant.target.ypos,spell.shape,spell.shape_width,spell.shape_length)                               
                            if len(affected_targets) >= 2:
                                best_spell = spell
                        
                        # Buff spells are very powerful, and include Reaction buffs like Shield
                        if spell.category == spell_category.Buff:                                                                    
                            if find_buff_target(combatant,spell.condition,spell.range) != None:                                    
                                best_spell = spell

                        #Healing spells are the most important to consider; if we find a target who needs healing we                         
                        if spell.category == spell_category.Healing:            
                            if best_spell == None or ((spell.instance*(spell.healing_die_count*spell.healing_die)) >= (best_spell.instance*(best_spell.healing_die_count*best_spell.healing_die))):
                                heal_target = find_heal_target(combatant,spell.range)
                                if heal_target != None:                                                      
                                    best_spell = spell
    return best_spell

#Cast a spell  - if Crit is forced use it
def cast_spell(combatant,spell,crit = None):    
    if not find_target(combatant):
        print_output('No targets remain!')
        return
    #Find the best spellslot to use on this spell
    spellslot = get_best_spellslot(combatant,spell)
    #See if a spellslot was returned by the function - cantrips and spells with a zero spellslot level are exempt
    if spell.cantrip or spell.min_spellslot_level == 0 or spellslot:               
        # Deduct one usage from the spellslot (not cantrips)
        if spellslot:
            #Consume the spell slot from player's available slots
            print_indent( combatant.name + ' is burning a ' + numbered_list(spellslot.level) + ' level spellslot to cast ' + spell.name)                                    
            spellslot.current -= 1
                
        if spell.description != "":
            print_indent( spell.description + " " + combatant.target.name)        
        
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
                    print_indent(combatant.target.name + ' resists the effect of the ' + spell.name + ' spell!')                    
                    if spell.damage_die != 0:
                        calculate_spell_damage(combatant,combatant.target,spell,spellslot,False,spell.saving_throw_damage_multiplier)    
                else:
                    inflict_condition(combatant.target,spell_ID,spell.condition,spell.condition_duration,spell.repeat_save_action,spell.repeat_save_end_of_turn,spell.saving_throw_attribute,spell_save_DC(combatant,spell))                    
                    if spell.damage_die != 0:
                        calculate_spell_damage(combatant,combatant.target,spell,spellslot,False)    
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
            #Pre-roll spell damage
            aoe_spell_damage = roll_spell_damage(combatant,spell,spellslot,False)           

            for affected_target in affected_targets:    
                print_output(affected_target.name + ' is in the affected area (located at (' + repr(affected_target.xpos) + ',' + repr(affected_target.ypos) + ')')   
                # Check if a saving throw is defined
                if spell.saving_throw_attribute != 0:
                    print_output(combatant.name + ' casts the ' + spell.name + ' spell on ' + combatant.target.name)
                    if savingthrow(combatant.target,savetype,spell_save_DC(combatant,spell)):            
                        print_indent(combatant.target.name + ' resists the effect of the ' + spell.name + ' spell!')
                    else:
                        inflict_condition(combatant.target,spell_ID,spell.condition,spell.condition_duration,spell.repeat_save_action,spell.repeat_save_end_of_turn,spell.saving_throw_attribute,spell_save_DC(combatant,spell))
                        #Debuff spells may also have a damage component
                        if spell.damage_die != 0:
                            calculate_spell_damage(combatant,affected_target,spell,spellslot,False,1,aoe_spell_damage)                             
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
                xorigin = combatant.xpos
                yorigin = combatant.ypos

            affected_targets = calculate_area_effect(combatant,xorigin,yorigin,combatant.target.xpos,combatant.target.ypos,spell.shape,spell.shape_width,spell.shape_length,True)   
            #Pre-roll spell damage
            aoe_spell_damage = roll_spell_damage(combatant,spell,spellslot,False)     

            # Apply damage to targets
            for affected_target in affected_targets:    
                print_output(affected_target.name + ' is in the affected area (located at (' + repr(affected_target.xpos) + ',' + repr(affected_target.ypos) + ')')                              
                if spell.saving_throw_attribute != 0:
                    if savingthrow(affected_target,spell.saving_throw_attribute,spell_save_DC(combatant,spell)):
                        #If target has evasion and saves, nothing happens
                        if (spell.saving_throw_attribute == saving_throw.Dexterity and affected_target.evasion) or (spell.saving_throw_damage_multiplier == 0):
                            print_indent(affected_target.name + ' resists all damage from the spell!') 
                        else:                
                            print_indent(affected_target.name + ' resists some damage from the spell!') 
                            calculate_spell_damage(combatant,affected_target,spell,spellslot,False,spell.saving_throw_damage_multiplier,aoe_spell_damage)                
                    else:
                        if spell.saving_throw_attribute == saving_throw.Dexterity and affected_target.evasion:
                            print_indent(affected_target.name + ' avoids half the damage thanks to Evasion!')
                            calculate_spell_damage(combatant,affected_target,spell,spellslot,False,0.5,aoe_spell_damage)              
                        else:
                            # Full damage
                            calculate_spell_damage(combatant,affected_target,spell,spellslot,False,1,aoe_spell_damage) 
                else:
                    # Damage automatically applies
                    calculate_spell_damage(combatant,affected_target,spell,spellslot,False,1,aoe_spell_damage)                    
        # Direct damage spell
        elif spell.category == spell_category.Damage:
            if spell.spell_attack:
                i = 0
                while i < total_instances:
                    #Repeat find_target call to see if we should firebolt someone else (i.e. because our current target drops)
                    if not find_target(combatant):
                        print_output('No targets remain!')
                        return
                    spell_attack(combatant,combatant.target,spell,spellslot)
                    i += 1                
            else:
                i = 0
                while i < total_instances:
                    # Check if a saving throw is defined
                    #Repeat find_target call to see if we should firebolt someone else (i.e. because our current target drops)
                    if not find_target(combatant):
                        print_output('No targets remain!')
                        return
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
                        calculate_spell_damage(combatant,combatant.target,spell,spellslot,crit)            
                    i += 1
           
        #Silently update concentration; if all targets saved aagainst the effect we need to immediately stop concentrating
        update_concentration(combatant)            

        #Check if we have spellslots left (except cantrips)
        if spellslot != None:
            if spellslot.level != 0 and spellslot.current == 0:
                print_output(combatant.name + ' has no ' + numbered_list(spellslot.level) + ' level spellslots remaining!')
    else:
        print_indent(combatant.name + ' wants to cast ' + spell.name + ', but has no appropriate spellslots remaining!')

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
    if spell.cantrip:
        return None
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
    if spell.cantrip or spell.min_spellslot_level == 0:
        return None
    
    initkey = operator.attrgetter("level")
    sorted_spells = sorted(combatant.spellslots(), key=initkey,reverse=True)    

    best_spellslot = None
    for spellslot in sorted_spells:        
        if spellslot.level >= spell.min_spellslot_level:
            if spellslot.current > 0:
                # Prefer to use the spell underneath the maximum spellslot level (i.e. casting Slow at level 5 offers no benefit over casting it at level 3)
                if spellslot.level <= spell.max_spellslot_level:                                       
                    best_spellslot = spellslot            
                # If we have to over-cast, make sure we use the lowest available spellslot
                elif best_spellslot == None or (spellslot.level >= spell.max_spellslot_level and spellslot.level < best_spellslot.level):
                    best_spellslot = spellslot                

    return best_spellslot

def new_spell_ID():
    ID = settings.last_spell_ID + 1
    settings.last_spell_ID = ID
    return ID
