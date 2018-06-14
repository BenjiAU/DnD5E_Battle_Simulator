#Explicit imports
from battle_simulator import combatants

#Implicit imports
from battle_simulator.classes import *
from battle_simulator.print_functions import *

#Other imports
import random
import math
import operator
from operator import itemgetter, attrgetter
from copy import copy

def resolve_bonus_damage(combatant,bonus_target,type,die,count,flat,crit,source):
    bonus_damage = 0
    crit_damage = 0
    if (bonus_target == 0) or (bonus_target == combatant.target.race):
        #if bonus_target == 0:
            #print_output(indent() + 'Rolling bonus damage: ')

        #else:
            #print_output(indent() + 'Rolling bonus damage against ' + combatant.target.race.name + ': ')  
            #                  
        for x in range(0,count):
            die_damage = roll_die(die)
            print_output(doubleindent() + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(die) + ' (' + source + ' Bonus Damage)')
            if greatweaponfighting(combatant) and die_damage <= 2 and source == combatant.main_hand_weapon.name:
                print_output(doubleindent() + combatant.name + ' rerolled a weapon die due to Great Weapon Fighting!')
                die_damage = roll_die(die)
                print_output(doubleindent() + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(die) + ' (' + source + ' Bonus Damage)')
            bonus_damage += die_damage
        if crit:
            crit_damage = bonus_damage * 2           
                        
    if crit:
        print_output(indent() + combatant.name + ' dealt an additional ' + crit_damage_text(repr(crit_damage+flat)) + ' (roll = ' + repr(bonus_damage) + ') points of ' + type.name + ' damage with ' + source)
        deal_damage(combatant,combatant.target,crit_damage+flat,type,combatant.main_hand_weapon.magic)
    else:
        print_output(indent() + combatant.name + ' dealt an additional ' + damage_text(repr(bonus_damage+flat)) + ' points of ' + type.name + ' damage with ' + source)
        deal_damage(combatant,combatant.target,bonus_damage+flat,type,combatant.main_hand_weapon.magic)

def resolve_hemo_damage(combatant):        
    #Gunslinger - Hemorrhaging Shot; damage and type is stored against the target and resolved after the target takes its turn (treated as nonmagical always?)
    if combatant.hemo_damage > 0:
        print_output(combatant.name + ' bleeds profusely from an earlier gunshot wound, suffering ' + damage_text(repr(combatant.hemo_damage)) + ' points of damage from Hemorrhaging Critical!')
        #hack
        #combatant.hemo_damage_type = combatant.target.main_hand_weapon.weapon_damage_type
        #deal damage to yourself
        deal_damage(combatant,combatant,combatant.hemo_damage,combatant.hemo_damage_type,False)
        combatant.hemo_damage = 0
        combatant.hemo_damage_type = 0     
        resolve_fatality(combatant)

def deal_damage(combatant,target,damage,dealt_damage_type,magical):    
    #Reduce bludgeoning/piercing/slashing if raging (and not wearing Heavy armour)
    if target.raging and not target.armour_type == armour_type.Heavy:            
        if dealt_damage_type in (damage_type.Piercing,damage_type.Bludgeoning,damage_type.Slashing):
            damage = int(damage/2)              
            print_output(doubleindent() + target.name + ' shrugs off ' + dmgred_text(repr(damage)) + ' points of damage in their rage!')
    if target.enlarged:
        if dealt_damage_type in (damage_type.Fire,damage_type.Cold,damage_type.Lightning):
            damage = int(damage/2)              
            print_output(doubleindent() + target.name + ' shrugs off ' + dmgred_text(repr(damage)) + ' points of damage due to the effects of Enlarge!')

    #Reduce bludgeoning/piercing/slashing if dealt by non-magical dealt_
    if target.monster_type == monster_type.Ancient_Black_Dragon:            
        if dealt_damage_type in (damage_type.Piercing,damage_type.Bludgeoning,damage_type.Slashing) and not magical:
            damage = int(damage/2)              
            print_output(doubleindent() + target.name + ' shrugs off ' + dmgred_text(repr(damage)) + ' points of damage from the non-magical attack!')

    if damage > 0:
        #Check if creature already has a type of this damage pending to be deducted from hit points
        for x in target.pending_damage():
            if x.pending_damage_type == dealt_damage_type:
                x.damage += damage
                damage = 0
        #If there is still damage, create a new pending damage object against the creature
        if damage > 0:
            pd = pending_damage()
            pd.pending_damage_type = dealt_damage_type
            pd.damage = damage
            target.pending_damage().append(pd)
            # Update statistics for combatant
            combatant.total_damage_dealt += damage

def heal_damage(combatant,healing):        
    #Can't heal the dead
    if combatant.alive:
    # Bring combatant back from unconsciousness, reset death saving throws if any
        if combatant.current_health == 0:
            combatant.conscious = True
            combatant.death_saving_throw_failure = 0
            combatant.death_saving_throw_success = 0

        combatant.current_health = combatant.current_health + healing
    
def resolve_damage(combatant):
    total_damage = 0
    damage_string = indent()
    #Calculate total damage
    #Track the damage dealt for output purposes and set the damage for that type back to zero    
    for x in combatant.pending_damage():        
        if x.damage > 0:
            total_damage += x.damage
            damage_string += repr(int(x.damage)) + ' points of ' + x.pending_damage_type.name + " damage"
            damage_string += "</br>"
    
    #Empty the list of pending damage
    combatant.pending_damage().clear()
    if total_damage > 0:
        
        if combatant.current_health >= 0 and combatant.conscious:
            #Use Reaction if it can do anything
            if not combatant.reaction_used:
                # Stone's Endurance
                if combatant.stones_endurance:
                    if not combatant.stones_endurance_used:
                        #Don't waste stones endurance on small hits (i.e. assume you can roll a 12)
                        if total_damage > conmod(combatant)+12:
                            reduction = conmod(combatant) + roll_die(12)
                            total_damage = int(total_damage - reduction)
                            print_output(combatant.name + ' uses their reaction, and uses Stones Endurance to reduce the damage by ' + repr(reduction) + '! ')
                            damage_string += 'reduced by ' + repr(int(reduction)) + ' (Stones Endurance)'
                            combatant.stones_endurance_used = True
                            combatant.reaction_used = True

                # Uncanny Dodge (can only occur after being victim of an Attack you can see - reduce all the attack damage by half)
                if combatant.uncanny_dodge:
                    # Don't waste dodge on small hits
                    if total_damage > 20:
                        reduction = int(total_damage/2)                        
                        print_output(combatant.name + ' uses their reaction, and uses Uncanny Dodge to reduce the damage of the attack by ' + dmgred_text(repr(reduction)) + '! ')                                    
                        total_damage = int(total_damage - reduction)
                        damage_string += 'reduced by ' + repr(int(reduction)) + ' (Uncanny Dodge)'
                        combatant.reaction_used = True
                        
            combatant.current_health = max(combatant.current_health - total_damage,0)
                        
            print_output('Damage Summary: ' + damage_string)        
            print_output(combatant.name + ' suffers a total of ' + damage_text(repr(int(total_damage))) + ' points of damage. ' + hp_text(combatant.current_health,combatant.max_health))        

def resolve_fatality(combatant):
    if combatant.alive and combatant.conscious and combatant.current_health <= 0:
        # Default proposition - combatant goes unconscious
        combatant.conscious = False   
        print_output(combatant.name + ' is knocked unconscious by the force of the blow!')

        #Relentless rage
        if combatant.relentless_rage and combatant.raging:
            if savingthrow(combatant,saving_throw.Constitution,combatant.saves.con,False,combatant.relentless_rage_DC):
                print_output(combatant.name + ' was dropped below 0 hit points, but recovers to 1 hit point due to their Relentless Rage!')
                combatant.alive = True
                combatant.conscious = True
                combatant.current_health = 1
                combatant.relentless_rage_DC += 5
            else:                
                print_output('The fury within ' + combatant.name + '\'s eyes fades, and they slump to the ground, unable to sustain their Relentless Rage!')
                combatant.conscious = False      
                combatant.relentless_rage = False  

        # rage beyond death (if we need to)
        if not combatant.conscious and combatant.rage_beyond_death and combatant.raging:
            # Combatant is not unconscious if they have Rage Beyond Death
            print_output(combatant.name + ' picks themselves up and continues fighting in their divine rage!')
            combatant.conscious = True
            if combatant.death_saving_throw_failure <= 3:
                # Roll a death saving throw; only track failures, when we hit 3 they are dead at the end of rage
                death_saving_throw(combatant)
                if combatant.death_saving_throw_failure >= 3:
                    print_output(combatant.name + ' fails their third death saving throw, but remains standing in their zealous rage beyond death!')       
                    combatant.conscious = True
                    combatant.alive = True
        elif combatant.rage_beyond_death and not combatant.raging:
            if combatant.death_saving_throw_failure >= 3:
                print_output(combatant.name + ' falls to their knees, the white-hot rage leaving their eyes as their jaw goes slack, and they perish on the ground.')                    
                combatant.conscious = False
                combatant.alive = False  
            else:
                print_output(combatant.name + ' collapses unconscious on the ground, exhausted by their divine rage, but still breathing')
                combatant.conscious = False
                combatant.alive = True

    #Resolve death saving throws (thrown at other parts, i.e. when damage suffered or when unconscious on your turn)
    elif combatant.alive and not combatant.conscious and combatant.current_health <= 0:
        if combatant.death_saving_throw_failure >= 3:
            print_output('~~~~' + combatant.name + '\'s chest stops moving, as the cold embrace of death welcomes them.' + '~~~~')
            combatant.alive = False
        elif combatant.death_saving_throw_success >= 3:
            print_output(combatant.name + '\'s breathing steadies, and they appear to no longer be in imminent risk of death, stabilised and unconscious')
            combatant.stabilised = True                
    
    # Knock target prone, set movement to 0, and turn off rage and if combatant unconscious after evaluating Rage features
    if not combatant.conscious:
        combatant.raging = False
        combatant.prone = True
        combatant.movement = 0

    #Resolve death
    if not combatant.alive and not combatant.conscious and combatant.current_health <=0:
        print_output(killing_blow_text('HOW DO YOU WANT TO DO THIS??'))        

def death_saving_throw(combatant):
    i = roll_die(20)
    print_output(' *** ' + combatant.name + ' makes a Death Saving Throw: they rolled a ' + repr(i) + ' *** ')
    if i <= 1:
        combatant.death_saving_throw_failure += 2
    elif i <= 9:
        combatant.death_saving_throw_failure += 1
    elif i <= 19:
        combatant.death_saving_throw_success += 1
    elif i >= 20:
        # On a natural 20 or higher (due to Bless spell etc.) automatically succeed all death saving throws and recover 1HP. Still prone
        print_output(combatant.name + ' recovers 1 HP, and is back in the fight!')
        heal_damage(combatant,1)        
        return
    print_output(indent() + 'Death Saving Throw Successes: ' + repr(combatant.death_saving_throw_success) + ' Failures: ' + repr(combatant.death_saving_throw_failure))