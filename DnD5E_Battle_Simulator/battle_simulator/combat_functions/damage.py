#Explicit imports
from battle_simulator import combatants

#Implicit imports
from battle_simulator.classes import *
from battle_simulator.print_functions import *
from battle_simulator.combat_functions.generics import * 
from battle_simulator.combat_functions.events import * 

#Other imports
import random
import math

def resolve_bonus_damage(combatant,bonus_target,type,die,count,flat,crit,source,magic):
    bonus_damage = 0
    crit_damage = 0
    if (bonus_target == 0) or (bonus_target == combatant.target.race):
        for x in range(0,count):
            die_damage = roll_die(die)
            print_double_indent( combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(die) + ' (' + source + ' Bonus Damage)')
            if greatweaponfighting(combatant) and die_damage <= 2 and source == combatant.main_hand_weapon.name:
                print_double_indent( combatant.name + ' rerolled a weapon die due to Great Weapon Fighting!')
                die_damage = roll_die(die)
                print_double_indent( combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(die) + ' (' + source + ' Bonus Damage)')
            bonus_damage += die_damage
        if crit:
            crit_damage = bonus_damage * 2           
                        
    if crit:
        print_indent( combatant.name + ' dealt an additional ' + crit_damage_text(repr(crit_damage+flat)) + ' points of ' + type.name + ' damage with ' + source)
        deal_damage(combatant,combatant.target,crit_damage+flat,type,magic,crit)
    else:
        print_indent( combatant.name + ' dealt an additional ' + damage_text(repr(bonus_damage+flat)) + ' points of ' + type.name + ' damage with ' + source)
        deal_damage(combatant,combatant.target,bonus_damage+flat,type,magic,crit)

def resolve_hemo_damage(combatant):        
    #Gunslinger - Hemorrhaging Shot; damage and type is stored against the target and resolved after the target takes its turn (treated as nonmagical always?)
    if combatant.hemo_damage > 0:
        print_output(combatant.name + ' bleeds profusely from an earlier gunshot wound, suffering ' + damage_text(repr(combatant.hemo_damage)) + ' points of damage from Hemorrhaging Critical!')
        #hack
        #combatant.hemo_damage_type = combatant.target.main_hand_weapon.weapon_damage_type
        #deal damage to yourself
        deal_damage(combatant,combatant,combatant.hemo_damage,combatant.hemo_damage_type,False,False)
        combatant.hemo_damage = 0
        combatant.hemo_damage_type = 0     
        resolve_damage(combatant)
        resolve_fatality(combatant)

def calculate_spell_damage(combatant,target,spell,spellslot,crit,multiplier=1):
    print_indent( 'Rolling spell damage:')                        
    spell_damage = 0
    if spell.damage_die > 0:
        # Start with base damage of spell
        for x in range(0,spell.damage_die_count):
            die_damage = roll_die(spell.damage_die)
            print_double_indent( combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(spell.damage_die) + ' (Spell Damage)')
            spell_damage += die_damage

        #Add additional damage for levels of expended spell slot
        if spellslot != None:
            if spellslot.level > spell.min_spellslot_level:
                # If the spell gains no benefit for spells higher than the maximum, we still burn the higher slot, but only get benefit from the maximum against the spell                
                if spell.max_spellslot_level < spellslot.level:
                    spellslot_bonus = spell.max_spellslot_level
                else:
                    spellslot_bonus = spellslot.level                
                
                for x in range(spell.min_spellslot_level,spellslot_bonus):
                    for y in range(0,spell.damage_die_count_per_spell_slot):
                        die_damage = roll_die(spell.damage_die_per_spell_slot)
                        print_double_indent( combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(spell.damage_die_per_spell_slot) + ' (Additional Spell Damage from Spell Slot)')
                        spell_damage += die_damage

        #Add bonus damage
        if combatant.target.race == spell.bonus_damage_target:
            for x in range(0,spell.bonus_damage_die_count):
                die_damage = roll_die(spell.bonus_damage_die)
                spell_damage += die_damage

    # Add flat damage
    spell_damage += spell.flat_damage

    #Double dice if crit
    if crit:
        spell_damage = spell_damage * 2
        
    # Apply multiplier 
    spell_damage = int(spell_damage * multiplier)

    print_indent( spell.name + ' dealt ' + damage_text(repr(spell_damage)) + ' points of ' + spell.damage_type.name + ' damage!')                    
    
    if spell.spell_attack:
        spell_damage = calculate_reduction_after_attack(combatant.target,spell_damage)

    deal_damage(combatant,target,spell_damage,spell.damage_type,True,crit)   

    # The spell effect is self-contained with all damage computed in this function; resolve it immediately and check fatality
    resolve_damage(target)

    # Resolve fatality immediately for spell effects
    resolve_fatality(combatant.target)

def resolve_spell_healing(combatant,target,spell,spellslot):
    print_indent( 'Rolling spell healing:')                        
    spell_healing = 0
    if spell.healing_die > 0:
        # Start with base healing of spell
        for x in range(0,spell.healing_die_count):
            die_healing = roll_die(spell.healing_die)
            print_double_indent( combatant.name + ' rolled a ' + repr(die_healing) + ' on a d' + repr(spell.healing_die) + ' (Spell Healing)')
            spell_healing += die_healing

        #Add additional healing for levels of expended spell slot
        if spellslot.level > spell.min_spellslot_level:
            # If the spell gains no benefit for spells higher than the maximum, we still burn the higher slot, but only get benefit from the maximum against the spell                
            if spell.max_spellslot_level < spellslot.level:
                spellslot_bonus = spell.max_spellslot_level
            else:
                spellslot_bonus = spellslot.level                
                
            for x in range(spell.min_spellslot_level,spellslot_bonus):
                for y in range(0,spell.healing_die_count_per_spell_slot):
                    die_healing = roll_die(spell.healing_die_per_spell_slot)
                    print_double_indent( combatant.name + ' rolled a ' + repr(die_healing) + ' on a d' + repr(spell.healing_die_per_spell_slot) + ' (Additional Spell Healing from Spell Slot)')
                    spell_healing += die_healing
        
    spell_healing += spellcasting_ability_modifier(combatant,spell)
    print_indent( spell.name + ' delivered ' + healing_text(repr(spell_healing)) + ' points of healing!')                    
    heal_damage(target,spell_healing) 

def deal_damage(combatant,target,damage,dealt_damage_type,magical,crit):    
    #Reduce bludgeoning/piercing/slashing if raging (and not wearing Heavy armour)
    if check_condition(target,condition.Raging) and not target.armour_type == armour_type.Heavy:            
        if dealt_damage_type in (damage_type.Piercing,damage_type.Bludgeoning,damage_type.Slashing):
            damage = int(damage/2)              
            print_double_indent( target.name + ' shrugs off ' + dmgred_text(repr(damage)) + ' points of damage in their rage!')
    if check_condition(target,condition.Enlarged):
        if dealt_damage_type in (damage_type.Fire,damage_type.Cold,damage_type.Lightning):
            damage = int(damage/2)              
            print_double_indent( target.name + ' shrugs off ' + dmgred_text(repr(damage)) + ' points of damage due to the effects of Enlarge!')

    #Reduce bludgeoning/piercing/slashing if dealt by non-magical weapon
    if target.monster_type == monster_type.Ancient_Black_Dragon:            
        if dealt_damage_type in (damage_type.Piercing,damage_type.Bludgeoning,damage_type.Slashing) and not magical:
            damage = int(damage/2)              
            print_double_indent( target.name + ' shrugs off ' + dmgred_text(repr(damage)) + ' points of damage from the non-magical attack!')

    if damage > 0:
        #Check if creature already has a type of this damage pending to be deducted from hit points
        for x in target.pending_damage():
            if x.pending_damage_type == dealt_damage_type:
                x.damage += damage
                x.crit = crit
                damage = 0
        #If there is still damage, create a new pending damage object against the creature
        if damage > 0:
            pd = pending_damage()
            pd.pending_damage_type = dealt_damage_type
            pd.damage = damage
            pd.crit = crit
            target.pending_damage().append(pd)
            # Update statistics for combatant
            combatant.total_damage_dealt += damage

def heal_damage(combatant,healing):        
    #Can't heal the dead
    if combatant.alive:
    # Bring combatant back from unconsciousness if healing restores you to over 0 hp, reset death saving throws if any
        if check_condition(combatant,condition.Unconscious) and combatant.current_health + healing > 0:
            remove_condition(combatant,condition.Unconscious)
            combatant.death_saving_throw_failure = 0
            combatant.death_saving_throw_success = 0

        if combatant.current_health + healing > combatant.max_health:
            combatant.current_health = combatant.max_health
        else:
            combatant.current_health = combatant.current_health + healing

        print_indent( combatant.name + ' recovers ' + healing_text(repr(healing)) + ' points of health. ' + hp_text(combatant.alive,combatant.current_health,combatant.max_health))

def calculate_reduction_after_attack(target,dealt_damage):
    modified_damage = dealt_damage
    # Use damage thresholds to help decide if reactions/effects should apply
    if can_use_reaction(target):
        if modified_damage > characterlevel(target):
            # Uncanny Dodge (can only occur after being victim of an Attack you can see - reduce all the attack damage by half)
            if target.uncanny_dodge:
                # Don't waste dodge on small hits                
                reduction = int(dealt_damage/2)           
                print_output('<b>Reaction:</b>')
                print_indent(target.name + ' uses their reaction, and uses Uncanny Dodge to reduce the damage of the attack by ' + dmgred_text(repr(reduction)) + '! ')                                    
                modified_damage = int(modified_damage - reduction)            
                target.reaction_used = True

    return modified_damage

def resolve_damage(combatant):
    #Fire the on_damage_taken_event before damage is resolved
    on_damage_taken_event(combatant)

    total_damage = 0
    damage_string = ""    
    #Calculate total damage
    #Track the damage dealt for output purposes and set the damage for that type back to zero    
    crit = False
    for x in combatant.pending_damage():        
        if x.damage > 0:
            total_damage += x.damage
            damage_string += repr(int(x.damage)) + ' points of ' + x.pending_damage_type.name + " damage"
            damage_string += "</br>"
        if x.crit:
            crit = True

    #Empty the list of pending damage
    combatant.pending_damage().clear()
    if total_damage > 0:
        
        if combatant.current_health >= 0 and not check_condition(combatant,condition.Unconscious):
            #Use Reaction if it can do anything
            if can_use_reaction(combatant):            
                # Stone's Endurance
                if combatant.stones_endurance:
                    if not combatant.stones_endurance_used:
                        #Don't waste stones endurance on small hits (i.e. assume you can roll a 12)
                        if total_damage > conmod(combatant)+12:
                            reduction = conmod(combatant) + roll_die(12)
                            total_damage = int(total_damage - reduction)
                            print_output('<b>Reaction:</b>')                
                            print_indent(combatant.name + ' uses their reaction, and uses Stones Endurance to reduce the damage by ' + repr(reduction) + '! ')
                            damage_string += 'reduced by ' + repr(int(reduction)) + ' (Stones Endurance)'
                            combatant.stones_endurance_used = True
                            combatant.reaction_used = True                
                        
            combatant.current_health = max(combatant.current_health - total_damage,0)
            #Check Concentration
            if check_condition(combatant,condition.Concentrating):
                concentration_check_DC = max(10,round(total_damage/2))
                print_output(combatant.name + ' needs to make a Concentrating check to maintain focus!')
                if savingthrow(combatant,saving_throw.Constitution,concentration_check_DC):
                    print_indent( combatant.name + ' maintains focus on the spell!')
                else:
                    remove_condition(combatant,condition.Concentrating)

            if settings.show_damage_summary:
                print_output('Damage Summary: ')
                print_indent(damage_string)        
            print_output(combatant.name + ' suffers a total of ' + damage_text(repr(int(total_damage))) + ' points of damage. ' + hp_text(combatant.alive,combatant.current_health,combatant.max_health))                    
            
        else:
            if total_damage < combatant.max_health:
                if crit:
                    print_output('***' + 'The critical damage strikes the unconscious form of ' + combatant.name + ' and causes them to fail two Death Saving Throws!' + '***')
                    combatant.death_saving_throw_failure += 2
                else:
                    print_output('***' + 'The damage heavily impacts the unconscious form of ' + combatant.name + ' and causes them to fail a Death Saving Throw!' + '***')
                    combatant.death_saving_throw_failure += 1
                            
                print_indent( 'Death Saving Throw Successes: ' + healing_text(repr(combatant.death_saving_throw_success)) + ' Failures: ' + damage_text(repr(combatant.death_saving_throw_failure)))
            else:
                #Instant death as total damage > hit point maximum
                print_output('***' + 'The damage exceeds ' + combatant.name + '\'s hit point maximum, and causes them to immediately perish.' + '***')
                combatant.death_saving_throw_failure = 3
                resolve_fatality(combatant)

def resolve_fatality(combatant):
    if combatant.alive and not check_condition(combatant,condition.Unconscious) and combatant.current_health <= 0:
        # Default proposition - combatant goes unconscious
        # If any features or abilities remove the unconsciousness condition, we remain standing
        inflict_condition(combatant,combatant,condition.Unconscious)                

        #Relentless rage
        if combatant.relentless_rage and check_condition(combatant,condition.Raging):
            if savingthrow(combatant,saving_throw.Constitution,combatant.relentless_rage_DC):
                print_output(combatant.name + ' was dropped below 0 hit points, but recovers to 1 hit point due to their Relentless Rage!')
                combatant.alive = True
                remove_condition(combatant,condition.Unconscious)
                combatant.current_health = 1
                combatant.relentless_rage_DC += 5
            else:                
                print_output('The fury within ' + combatant.name + '\'s eyes fades, and they slump to the ground, unable to sustain their Relentless Rage!')
                remove_condition(combatant,condition.Unconscious)
                combatant.relentless_rage = False  

        # rage beyond death (if we need to)
        if check_condition(combatant,condition.Unconscious) and check_condition(combatant,condition.Raging) and combatant.rage_beyond_death:
            # Combatant is not unconscious if they have Rage Beyond Death
            print_output(combatant.name + ' picks themselves up and continues fighting in their divine rage!')
            remove_condition(combatant,condition.Unconscious)
            if combatant.death_saving_throw_failure <= 3:
                # Roll a death saving throw; only track failures, when we hit 3 they are dead at the end of rage
                death_saving_throw(combatant)
                if combatant.death_saving_throw_failure >= 3:
                    print_output(combatant.name + ' fails their third death saving throw, but remains standing in their zealous rage beyond death!')       
                    remove_condition(combatant,condition.Unconscious)
                    combatant.alive = True
        elif not check_condition(combatant,condition.Raging) and combatant.rage_beyond_death:
            if combatant.death_saving_throw_failure >= 3:
                print_output(combatant.name + ' falls to their knees, the white-hot rage leaving their eyes as their jaw goes slack, and they perish on the ground.')                    
                inflict_condition(combatant,combatant,condition.Unconscious)
                combatant.alive = False  
            else:
                print_output(combatant.name + ' collapses unconscious on the ground, exhausted by their divine rage, but still breathing')
                inflict_condition(combatant,combatant,condition.Unconscious)
                combatant.alive = True

    #Resolve death saving throws (thrown at other parts, i.e. when damage suffered or when unconscious on your turn)
    elif combatant.alive and check_condition(combatant,condition.Unconscious) and combatant.current_health <= 0:
        if combatant.death_saving_throw_failure >= 3:
            print_output('~~~~' + combatant.name + '\'s chest stops moving, as the cold embrace of death welcomes them.' + '~~~~')
            combatant.alive = False
        elif combatant.death_saving_throw_success >= 3:
            print_output(combatant.name + '\'s breathing steadies, and they appear to no longer be in imminent risk of death, stabilised and unconscious')
            combatant.stabilised = True                
    
    # Knock target prone, set movement to 0, and turn off rage and if combatant unconscious after evaluating Rage features
    if check_condition(combatant,condition.Unconscious):
        remove_condition(combatant,condition.Raging) 
        # Remove concentration
        remove_condition(combatant,condition.Concentrating)            

        if not check_condition(combatant,condition.Prone):
            inflict_condition(combatant,combatant,condition.Prone)        
        combatant.movement = 0

    #Resolve death
    #if not combatant.alive and check_condition(combatant,condition.Unconscious) and combatant.current_health <=0:
    #    print_output(killing_blow_text('HOW DO YOU WANT TO DO THIS??'))        

def death_saving_throw(combatant):
    roll = roll_die(20)        
    roll_text = ""

    if roll <= 1:
        roll_text = damage_text(repr(roll))
        combatant.death_saving_throw_failure += 2
    elif roll <= 9:
        roll_text = damage_text(repr(roll))
        combatant.death_saving_throw_failure += 1
    elif roll <= 19:
        roll_text = healing_text(repr(roll))
        combatant.death_saving_throw_success += 1
    elif roll >= 20:
        # On a natural 20 or higher (due to Bless spell etc.) automatically succeed all death saving throws and recover 1HP. Still prone
        print_output(' *** ' + combatant.name + ' makes a Death Saving Throw: they rolled a NATURAL 20 *** ')
        print_output(combatant.name + ' recovers 1 HP, and is back in the fight!')
        heal_damage(combatant,1)        
        return
    print_output(' *** ' + combatant.name + ' makes a Death Saving Throw: they rolled a ' + roll_text + ' *** ')
    print_indent( 'Death Saving Throw Successes: ' + healing_text(repr(combatant.death_saving_throw_success)) + ' Failures: ' + damage_text(repr(combatant.death_saving_throw_failure)))