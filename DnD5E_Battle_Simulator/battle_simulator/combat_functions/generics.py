#Explicit importscheck
from battle_simulator import combatants

#Implicit imports
from battle_simulator.classes import *
from battle_simulator.print_functions import *
from battle_simulator.combat_functions.conditions import *

def use_luck(combatant):
    if combatant.luck_uses > 0:        
        random.seed
        luck_die_roll = random.randint(1,20)        
        combatant.luck_uses -= 1
        print_output(indent() + combatant.name + ' used a point of Luck, and rolled a ' + repr(luck_die_roll) + ' on the lucky d20!')
        return(luck_die_roll)        

# save functions #

def savingthrow(combatant,savetype,DC):
    print_output('<i>Saving Throw</i>')
    if savetype == saving_throw.Strength:
        modifier = combatant.saves.str
        adv = combatant.saves.str_adv
    elif savetype == saving_throw.Dexterity:
        modifier = combatant.saves.dex
        adv = combatant.saves.dex_adv
    elif savetype == saving_throw.Constitution:
        modifier = combatant.saves.con
        adv = combatant.saves.con_adv
    elif savetype == saving_throw.Intelligence:
        modifier = combatant.saves.int
        adv = combatant.saves.int_adv
    elif savetype == saving_throw.Wisdom:
        modifier = combatant.saves.wis
        adv = combatant.saves.wis_adv
    elif savetype == saving_throw.Charisma:
        modifier = combatant.saves.cha
        adv = combatant.saves.cha_adv

    roll = roll_die(20)

    savingthrow = roll + modifier    
    print_output(combatant.name + ' rolled a ' + repr(roll) + ' on a d20 for the saving throw with a +' + repr(modifier) + ' modifier')                                                                                                             
    # Check conditions
    if check_condition(combatant,condition.Stunned):
        if savetype == saving_throw.Strength or savetype == saving_throw.Dexterity:
            print_output(indent() + combatant.name + ' automatically fails the ' + repr(DC) + ' ' + savetype.name + ' save as they are currently incapacitated!')
            return False

    #print_output(savetype + ' save: Natural roll: ' + repr(roll) + ', modifier: ' + repr(modifier))
    if savingthrow >= DC:
        print_output(indent() + combatant.name + ' succeeded on a DC' + repr(DC) + ' ' + savetype.name + ' save with a total of ' + repr(savingthrow) + '!')
        return True
    
    if adv:
        #print_output(combatant.name + ' failed the save, but has advantage on ' + savetype + ' saving throws!')
        roll = roll_die(20)
        savingthrow = roll + modifier
        #print_output(savetype + ' save: Natural roll: ' + repr(roll) + ', modifier: ' + repr(modifier))        
        if savingthrow >= DC:
            print_output(indent() + combatant.name + ' succeeded on a DC' + repr(DC) + ' ' + savetype.name + ' save with a total of ' + repr(savingthrow) + '!')
            return True

    #If the savingthrow fails, and we could make it with a decent roll (say higher than 15), and we have luck, spend luck to reroll the d20
    if combatant.luck_uses > 0 and (DC - modifier <= 15):
        luck_roll = use_luck(combatant)
        if luck_roll > roll:
            savingthrow = luck_roll + modifier
            if savingthrow >= DC:
                print_output(indent() + combatant.name + ' used a point of Luck, and has now succeeded on a DC' + repr(DC) + ' ' + savetype.name + ' save with a total of ' + repr(savingthrow) + '!')
                return True

    print_output(indent() + combatant.name + ' FAILED on a DC' + repr(DC) + ' ' + savetype.name + ' save with a total of ' + repr(savingthrow) + '!')
    return False

# check functions #
def abilitycheck(combatant,checktype,DC,proficient=False):    
    #Pass a DC of 0 to just return the check value (i.e. Initiative, Perception)
    if checktype == ability_check.Strength:
        modifier = strmod(combatant)
    elif checktype == ability_check.Dexterity:
        modifier = dexmod(combatant)        
    elif checktype == ability_check.Constitution:
        modifier = conmod(combatant)
    elif checktype == ability_check.Intelligence:
        modifier = intmod(combatant)        
    elif checktype == ability_check.Wisdom:
        modifier = wismod(combatant)        
    elif checktype == ability_check.Charisma:
        modifier = chamod(combatant)        

    if proficient:
        modifier += combatant.proficiency

    roll = roll_die(20)
    check = roll + modifier
    print_output(combatant.name + ' rolled a ' + repr(roll) + ' on a d20 for the ability check with a +' + repr(modifier) + ' modifier')                                                                                                             
    if DC == 0:
        return(check)

    print_output('<i>Ability Check</i>')
    #print_output(checktype + ' check: Natural roll: ' + repr(roll) + ', modifier: ' + repr(modifier))    
    if check >= DC:
        print_output(indent() + combatant.name + ' succeeded on a DC' + repr(DC) + ' ' + checktype.name + ' check with a total of ' + repr(check))
        return True
    if adv:
        #print_output(combatant.name + ' failed the check, but has advantage on ' + checktype + ' checks!')
        roll = roll_die(20)
        check = roll + modifier
        #print_output(checktype + ' check: Natural roll: ' + repr(roll) + ', modifier: ' + repr(modifier))    
        if check >= DC:
            print_output(indent() + combatant.name + ' succeeded on a DC' + repr(DC) + ' ' + checktype.name + ' check with a total of ' + repr(check))
            return True

    #If the savingthrow fails, and we could make it with a decent roll (say higher than 15), and we have luck, spend luck to reroll the d20
    if combatant.luck_uses > 0 and (DC - modifier <= 15):
        luck_roll = use_luck(combatant)
        if luck_roll > roll:
            check = luck_roll + modifier
            if check >= DC:
                print_output(indent() + combatant.name + ' used a point of Luck, and has now succeeded on a DC' + repr(DC) + ' ' + checktype.name + ' check with a total of ' + repr(check))
                return True

    print_output(indent() + combatant.name + ' FAILED on a DC' + repr(DC) + ' ' + checktype.name + ' check with a total of ' + repr(check))
    return False

# Initiative
def roll_initiative(combatant):
    initiativeroll = abilitycheck(combatant,ability_check.Dexterity,0)      
    if combatant.feral_instinct:
        initiativeroll_adv = abilitycheck(combatant,ability_check.Dexterity,0)
        initiativeroll = max(initiativeroll,initiativeroll_adv)
    if combatant.quickdraw:
        initiativeroll += combatant.proficiency
    combatant.initiative_roll = initiativeroll

def determine_advantage(combatant,range_attack):
    advantage = False
    disadvantage = False
    # Check for all conditions on the combatant, and see if any of them grant advantage/disadvantage directly
    for combatant_condition in combatant.creature_conditions():
        if combatant_condition.grants_advantage:
            advantage = True            
            print_output(combatant.name + ' has advantage on the attack from the ' + combatant_condition.condition.name + ' condition!')        
        if combatant_condition.grants_disadvantage:
            disadvantage = True            
            print_output(combatant.name + ' has disadvantage on the attack from the ' + combatant_condition.condition.name + ' condition!')        
    
    #Check if any conditions are present on the target, as some of them may influence advantage/disadvantage  
    for target_condition in combatant.target.creature_conditions():
        if target_condition.condition == condition.Stunned:
            print_output(combatant.target.name + ' is Stunned, giving all attacks against it advantage!')
            advantage = True            
        if target_condition.condition == condition.Reckless:
            print_output(combatant.name + ' has advantage on the attack, as ' + combatant.target.name + ' used Reckless Attack last round!')
            advantage = True
        if target_condition.condition == condition.Prone and range_attack:
            print_output(combatant.target.name + ' is prone on the ground, giving ' + combatant.name + ' disadvantage on the attack!')
            disadvantage = True

    #Check assassination flag
    if combatant.can_assassinate_target:
        print_output(combatant.name + ' reacts with supernatural speed, and can Assassinate ' + combatant.target.name + ', gaining advantage on the attack')
        advantage = True
        
    #Can we use reckless attack?
    if combatant.reckless and not advantage:
        inflict_condition(combatant,combatant,condition.Reckless,2,True,False)
        print_output(combatant.name + ' uses Reckless Attack, gaining advantage on the attack!')
        advantage = True

    #Is Vow of Enmity up?    
    if combatant.vow_of_enmity_target == combatant.target:
        print_output(combatant.name + ' has advantage on the attack from their Vow of Enmity!')
        advantage = True

    return advantage,disadvantage

def attack_roll(combatant,advantage,disadvantage,to_hit_modifier):
    initroll = roll_die(20)                    
    if advantage and disadvantage:
        print_output(combatant.name + ' has both advantage and disadvantage on the attack, and rolled a ' + repr(initroll) + ' on a d20 with a +' + repr(to_hit_modifier) + ' to hit')
        atkroll = initroll
    if advantage and not disadvantage:
        advroll = roll_die(20)
        print_output(combatant.name + ' has advantage on the attack, and rolled a ' + repr(initroll) + ' and a ' + repr(advroll) + ' on a d20 with a +' + repr(to_hit_modifier) + ' to hit')
        atkroll = max(initroll,advroll)
    if disadvantage and not advantage:
        disadvroll = roll_die(20)
        print_output(combatant.name + ' has disadvantage on the attack, and rolled a ' + repr(initroll) + ' and a ' + repr(disadvroll) + ' on a d20 with a +' + repr(to_hit_modifier) + ' to hit')
        atkroll = min(initroll,disadvroll)
    if not advantage and not disadvantage:
        atkroll = initroll
        print_output(combatant.name + ' rolled a ' + repr(initroll) + ' on a d20 for the attack with a +' + repr(to_hit_modifier) + ' to hit')                                                                                                             
    return atkroll

def calc_total_AC(combatant):
    totalAC = 0
    totalAC += combatant.armour_class
    if check_condition(combatant,condition.Hasted):
        totalAC += 2
    return totalAC

def calc_distance(combatant,target):
    xdistance = int(math.fabs(combatant.xpos-target.xpos))
    ydistance = int(math.fabs(combatant.ypos-target.ypos))
    return int(math.sqrt((xdistance * xdistance) + (ydistance * ydistance)))
