#Explicit imports
from battle_simulator import combatants

#Implicit imports
from .classes import *
from .print_functions import *

#Other imports
import random
import math
import operator
from operator import itemgetter, attrgetter

### Core Round functions ###
def movement(combatant):
    # Only move if a target exists
    if combatant.target:
        # movement #
        movement = combatant.speed
        if combatant.hasted:
            movement = movement * 2
        use_movement(combatant,movement)

    combatant.movement_used = True

def use_movement(combatant,movement):
    if combatant.prone:
        # Spend half movement to get up #
        movement = math.floor(movement/2)
        print_output(combatant.name + ' spends ' + repr(movement) + ' feet of movement to stand up from prone ')            
        combatant.prone = False

    # Melee weapon?
    if (combatant.current_weapon.range == 0) and not (combatant.current_weapon.thrown):                    
        if target_in_weapon_range(combatant,combatant.target,combatant.current_weapon.range):            
            print_output(combatant.name + ' stays where they are, in melee range of ' + combatant.target.name)
        else:
            move_to_target(combatant,combatant.target,movement)
    else:
        # Range weapon
        # Have we used our primary action yet? Naively increase distance if so, even if it means running out of range
        if combatant.action_used:
            move_from_target(combatant,combatant.target,movement)
        else:
            #Otherwise use the range of thw eapon to determine where to move
            if target_in_weapon_range(combatant,combatant.target,combatant.current_weapon.range):
                # Don't move out of weapon range - figure out current gap, subtract it from weapon range, thats how far we can move
                #if target_in_weapon_range(combatant,combatant.target,0):
                    #use_bonus_action(combatant,"Disengage")
            
                if movement > combatant.current_weapon.range - calc_distance(combatant,combatant.target):
                    movement = combatant.current_weapon.range - calc_distance(combatant,combatant.target)
            
                if movement > 0:
                    move_from_target(combatant,combatant.target,movement)
            else:
                #Close the distance to be able to use weapon 
                gap_to_close = calc_distance(combatant,combatant.target) - combatant.current_weapon.range;
                if gap_to_close <= movement:
                    move_to_target(combatant,combatant.target,gap_to_close)
                else:
                    move_to_target(combatant,combatant.target,movement)

def use_equipment(combatant):
    # Iterate through equipment and use any available spells (if possible)
    for eq in combatant.equipment_inventory():
        # Enlarge (i.e. from Titanstone Knuckles)
        if eq.grants_equipment_spell == equipment_spells.Enlarge:
            if not combatant.enlarged:
                print_output(combatant.name + ' smashes the ' + eq.name + ' together and grows in size! This uses up their Action')            
                combatant.enlarged = True
                combatant.action_used = True

        # Haste (i.e. from Boots of Haste)
        if eq.grants_equipment_spell == equipment_spells.Haste:
            if not combatant.hasted:
                print_output(combatant.name + ' clicks the ' + eq.name + ' together and begins to move rapidly! This uses up their Bonus Action')            
                combatant.hasted = True
                combatant.hasted_bonus_armour = 2;
                combatant.hasted_action = True;
                combatant.hasted_action_used = False;
                combatant.bonus_action_used = True

        # Blade Return (Belt of Blade Returning - does not use an action/bonus action, just happens at the start of each round)
        if eq.grants_equipment_spell == equipment_spells.BladeReturn:            
            reequip_thrown_weapon = False
            for weapon in combatant.weapon_inventory():                                    
                if weapon.thrown and weapon.was_thrown:
                    reequip_thrown_weapon = True
                    weapon.was_thrown = False
                    print_output(weapon.name + ' re-appears on ' + combatant.name + '\'s ' + eq.name)            

            #Re-equip the first weapon on the list                                
            if reequip_thrown_weapon:
                combatant.current_weapon = itemgetter(0)(combatant.weapon_inventory())     
                print_output(combatant.name + ' draws ' + combatant.current_weapon.name + ' and prepares to fight once more!')                        
            
def action(combatant):
    # Only perform an action if target exists
    if combatant.target:
        if combatant.action_used:
            print_output(combatant.name + ' has already used their Action this turn.')

        if not combatant.action_used:
            #Custom monster logic before stepping into main loop
            if combatant.creature_type == creature_type.Monster:
                if combatant.breath_attack and (combatant.breath_range >= calc_distance(combatant,combatant.target)):            
                    breath_attack(combatant)
                    combatant.action_used = True

        if not combatant.action_used:
            # Swap to a different weapon if it makes sense due to range                    
            current_range = calc_distance(combatant,combatant.target)
            # Attempt a weapon swap - change weapons depending on range
            # This will prefer to swap a non-broken or ruined weapon in
            weapon_swap(combatant,current_range)

            if combatant.current_weapon.broken == False:
                if target_in_weapon_range(combatant,combatant.target,combatant.current_weapon.range):
                    attack_action(combatant)                        
                else:
                    print_output(combatant.name + ' is taking the Dash action!')
                    movement = combatant.speed
                    if combatant.hasted:
                        movement = combatant.speed * 2                                                
                    use_movement(combatant,movement)
                    combatant.action_used = True
            else:
                # If the weapon is Ruined, and we could not swap to a non-ruined weapon, we're out of luck
                if combatant.current_weapon.ruined:
                    print_output(combatant.name + ' can\'t do anything with ' + combatant.current_weapon.name + ', it is damaged beyond repair!')
                    # Can't swap to a valid weapon - just have to sit this one out
                    combatant.action_used = True

                # If the weapon is broken, and we could not swap to a non-broken weapon, must waste action reparing it
                if not combatant.action_used:
                    if combatant.current_weapon.broken:
                        repair_weapon(combatant)            
                        combatant.action_used = True
                
                #If we have not attacked yet, attempt to attack
                if not combatant.action_used:
                    attack_action(combatant)
                    combatant.action_used = True

    combatant.action_used = True

def bonus_action(combatant):    
    #Only do something if a target exists
    if combatant.target:

        if combatant.bonus_action_used:
            print_output(combatant.name + ' has already used their Bonus Action this turn.')
        
        #Cunning Action
        #if not combatant.bonus_action_used:
        #    if combatant.cunning_action:
                #Dodge
                #Disengage
         #       if enemy_in_melee_range(combatant):

                #Hide
        #Rage
        if not combatant.bonus_action_used:
            if combatant.canrage and not combatant.raging:
                print_output(combatant.name + ' uses their Bonus Action to go into a mindless rage! "I would like to RAAAGE!!!"')
                combatant.raging = True;
                # Reset duration of this rage
                combatant.rage_duration = 0
                combatant.bonus_action_used = True
                # Rage grants advantage on strength checks/saving throws for its duration
                if combatant.armour_type != armour_type.Heavy:
                    combatant.saves.str_adv = True
                    combatant.checks.str_adv = True

        #Second Wind
        if not combatant.bonus_action_used:
            if combatant.second_wind:
                #Don't use Second Wind unless current HP is more than 10+fighter level less than max
                fighter_level = get_combatant_class_level(combatant,player_class.Fighter)                
                if combatant.current_health + 10 + fighter_level < combatant.max_health:
                    second_wind_heal = roll_die(10) + fighter_level
                    heal_damage(combatant,second_wind_heal)                    
                    print_output(combatant.name + ' uses their Bonus Action to gain a Second Wind, and restores ' + repr(second_wind_heal) + ' hit points!')
                    combatant.second_wind = False
                    combatant.bonus_action_used = True

        #Frenzy
        if not combatant.bonus_action_used:
            if combatant.raging:
                if combatant.frenzy:            
                    if target_in_weapon_range(combatant,combatant.target,combatant.current_weapon.range):                    
                        print_output(combatant.name + ' uses their Bonus Action to make a frenzied weapon attack against ' + combatant.target.name)
                        attack(combatant)            
                        combatant.bonus_action_used = True
                        
        #Boots of Feral Leaping        
        if not combatant.bonus_action_used:
            for item in combatant.equipment_inventory():
                if item.grants_equipment_spell == equipment_spells.Leap:
                    #For now treat this as special forced movement of 20 feet
                    print_output(combatant.name + ' is taking a flying leap using their ' + item.name + ' as a Bonus Action!')                    
                    if abilitycheck(combatant,ability_check.Strength,strmod(combatant),combatant.checks.str_adv,16):                    
                        print_output(combatant.name + ' leaps 20 feet.')                        
                        use_movement(combatant,20)                            
                    else:
                        print_output(combatant.name + ' fell over where they stand!')
                        combatant.prone = True
                    combatant.bonus_action_used = True

        #Lightning Reload
        if not combatant.bonus_action_used:
            if combatant.current_weapon.weapon_type == weapon_type.Firearm:
                if combatant.lighting_reload:
                    if combatant.current_weapon.currentammo == 0:
                        combatant.current_weapon.currentammo = combatant.current_weapon.reload
                        print_output(combatant.name + ' used a bonus action to reload.')
                        combatant.bonus_action_used = True

        #Vow of Enmity
        if not combatant.bonus_action_used:
            if combatant.channel_divinity and combatant.vow_of_enmity:
                combatant.vow_of_enmity_target = combatant.target
                print_output(combatant.name + ' swears a Vow of Enmity against ' + combatant.target.name)
                combatant.channel_divinity = False
                combatant.bonus_action_used = True

def hasted_action(combatant):
    print_output('<b>Hasted Action:</b>')
    # Only perform an action if target exists
    if combatant.target:
        # Swap to a different weapon if it makes sense due to range                    
        current_range = calc_distance(combatant,combatant.target)
        # Attempt a weapon swap - change weapons depending on range
        # This will prefer to swap a non-broken or ruined weapon in
        weapon_swap(combatant,current_range)

        if target_in_weapon_range(combatant,combatant.target,combatant.current_weapon.range):
            attack(combatant)
            combatant.hasted_action_used = True
        else:
            print_output(combatant.name + ' uses the Dash action as a Hasted action!')            
            movement = combatant.speed * 2                        
            use_movement(combatant,movement)          
            combatant.hasted_action_used = True

    combatant.hasted_action_used = True

def use_bonus_action(combatant,action):
    # For out of sequence bonus actions (i.e. Disengaging before moving)
    # Only execute anything if we haven't already used the bonus action this round (otherwise it fails)
    if not combatant.bonus_action_used:
        if action == "Disengage":
            if combatant.cunning_action and not combatant.bonus_action_used:
                combatant.disengaged = True
                combatant.bonus_action_used = True
        print_output(combatant.name + ' uses their Bonus action and takes the ' + action + ' Action!')
    
#Weapon swap
def weapon_swap(combatant,current_range):
    # A weapon is already equipped; equip a new one
    if combatant.current_weapon.name != "":                    
        for weapon in combatant.weapon_inventory():                            
            # Swap to range weapon if within range (preferring shorter range non-broken weapons), unless in melee, in which case only swap to melee                        
                # swap out broken weapon, unless this is the better weapon
            if ((weapon.range >= current_range and current_range != 0 and combatant.current_weapon.broken and not weapon.broken) or 
                # prefer unbroken shorter range weapon
            (weapon.range >= current_range and current_range != 0 and weapon.range < combatant.current_weapon.range) or 
                # prefer range weapon at range over melee weapon
            (weapon.range >= current_range and current_range != 0 and weapon.range != 0 and combatant.current_weapon.range == 0) or
                # prefer melee weapon for melee range, but don't swap out for no reason
            (weapon.range == 0 and current_range == 0 and combatant.current_weapon.range != 0)):         
                # Don't swap if we're already using this weapon
                if combatant.current_weapon != weapon:
                    # Draw ruined and cry if current weapon is ruined - making it here means there are no better options
                    if weapon.ruined and (combatant.current_weapon.ruined):
                        print_output(combatant.name + ' sadly puts away ' + combatant.current_weapon.name + ' and draws out the ruined ' + weapon.name)                        
                        combatant.current_weapon = weapon                   
                        return True
                    # Draw broken if we have to (i.e. current weapon is broken/ruined, and we need to repair the better one)                    
                    if weapon.broken and (combatant.current_weapon.broken or combatant.current_weapon.ruined):  
                        print_output('Frustrated, ' + combatant.name + ' stows ' + combatant.current_weapon.name + ' and draws out the broken ' + weapon.name)                        
                        combatant.current_weapon = weapon                   
                        return True
                    # If the weapon is neither broken nor ruined, and it makes it here, it's the best choice
                    if not weapon.ruined and not weapon.broken:
                        print_output(combatant.name + ' stows ' + combatant.current_weapon.name + ' and readies ' + weapon.name)                        
                        combatant.current_weapon = weapon                   
                        return True
                    
            #Thrown weapon handling
            if combatant.current_weapon.was_thrown:                    
                if not weapon.was_thrown:
                    print_output(combatant.name + ' draws  ' + weapon.name + ' after throwing their weapon')                        
                    combatant.current_weapon = weapon
                    return True

    # No weapon is equipped; draw one
    else:
        for weapon in combatant.weapon_inventory():    
            print_output(combatant.name + ' draws ' + weapon.name + ' and prepares for battle!')
            combatant.current_weapon = weapon                   
            return True
    return False

#Attack action
def attack_action(combatant):
    #one set of rules for monsters
    if combatant.creature_type == creature_type.Monster:
        if combatant.breath_attack and (combatant.breath_range >= calc_distance(combatant,combatant.target)):
            breath_attack(combatant)
        else:
            if combatant.multiattack:
                #Determine which attacks out of the multiattack will reach (due to range, reach)                
                multiattack_weapons = []
                for ma in combatant.multiattack:
                    for weapon in combatant.weapon_inventory():
                        if target_in_weapon_range(combatant,combatant.target,weapon.range) and ma == weapon.name:                        
                            multiattack_weapons.append(weapon)

                if len(multiattack_weapons) > 0:
                    print_output(combatant.name + ' unleashes a Multiattack against ' + combatant.target.name)                
                    for ma_weapon in multiattack_weapons:
                        combatant.current_weapon = ma_weapon
                        attack(combatant)
                else:
                    #Revert to normal attack/swap to range or reach weapon if required
                    print_output(combatant.name + ' uses the Attack action against ' + combatant.target.name)                
                    attack(combatant)    
            else:
                print_output(combatant.name + ' uses the Attack action against ' + combatant.target.name)                
                attack(combatant)    
    else:
        print_output(combatant.name + ' uses the Attack action against ' + combatant.target.name)                
        attack(combatant)

        if combatant.extra_attack > 0:
            for x in range(0,combatant.extra_attack):
                #Can't attack if weapon is broken, must spend next action to fix it
                if not combatant.current_weapon.broken:
                    print_output('<i>' + combatant.name + ' uses an Extra Attack.</i>')
                    attack(combatant)  

def breath_attack(combatant):
    print_output(combatant.name + ' rears back and unleashes a devastating breath attack!')   
    breath_damage = 0
    breath_damage_type = 0
    die_damage = 0
    if combatant.monster_type == monster_type.Ancient_Black_Dragon:
        breath_damage_type = damage_type.Acid
        i = 1
        for i in range(1,15):
            die_damage = roll_die(combatant.breath_damage_die)
            print_output(indent() + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.breath_damage_die) + ' (Breath Damage)')
            breath_damage += die_damage
    if savingthrow(combatant.target,saving_throw.Dexterity,dexmod(combatant.target),combatant.target.saves.dex_adv,23):
        #If target has evasion and saves, nothing happens
        if not combatant.target.evasion:
            deal_damage(combatant,combatant.target,breath_damage/2,breath_damage_type,True)
    else:
        #If target has evasion and fails, half damage
        if combatant.target.evasion:
            deal_damage(combatant,combatant.target,breath_damage/2,breath_damage_type,True)
        else:
            deal_damage(combatant,combatant.target,breath_damage,breath_damage_type,True)

    combatant.breath_attack = False

    #See if the damage droped target below 0 hp
    resolve_damage(combatant.target)
    resolve_fatality(combatant.target)

def breath_recharge(combatant):    
    die = roll_die(6)
    if die >= 5:
        print_output(combatant.name + ' rolled a ' + repr(die) + ' on a d6 and recharged their Breath Attack!')
        combatant.breath_attack = True
    else:
        print_output(combatant.name + ' rolled a ' + repr(die) + ' on a d6 and did not recharge their Breath Attack.')

#Make an attack
def attack(combatant):    
    #Only attack with a weapon
    if combatant.current_weapon.name != "":
        # only resolve attack if target is within range
        if target_in_weapon_range(combatant,combatant.target,combatant.current_weapon.range):
            # only resolve attack if target is alive
            if combatant.target.alive:
                # Only continue with attack steps if we don't break out because of something else interfering
                # i.e. weapon breaking, reloading
                attackcomplete = False    
                range_attack = False
                while not attackcomplete:
                
                    calledshot = False
                    advantage = False
                    disadvantage = False
        
                    combatant.use_sharpshooter = False
                    # Recalculate all +hit modifiers (based on current weapon, fighting style, ability modifiers etc.)
                    to_hit_modifier = calc_to_hit_modifier(combatant)

                    # Before-roll weapon features                    

                    # Determine if attack is ranged or not                    
                    # Decide whether to throw or stab with weapon
                    if combatant.current_weapon.thrown and calc_distance(combatant,combatant.target) > melee_range():
                        print_output(combatant.name + ' throws ' + combatant.current_weapon.name + ' at ' + combatant.target.name + '!')
                        range_attack = True
                        combatant.current_weapon.was_thrown = True                            

                    if combatant.current_weapon.weapon_type == weapon_type.Firearm:
                        # Check that the Firearm is not ruined - if it is ruined, no attacks can be made
                        if not attackcomplete:
                            if combatant.current_weapon.broken and combatant.current_weapon.ruined:
                                print_output(combatant.name + ' can\'t do anything with ' + combatant.current_weapon.name + ', it is damaged beyond repair!')
                                attackcomplete = True
            
                        if not attackcomplete:
                            range_attack = True
                            if combatant.current_weapon.currentammo == 0:
                                # reload weapon # 
                                if combatant.bonus_action_used:
                                    print_output(combatant.name + ' used their attack to reload ' + combatant.current_weapon.name)
                                    combatant.current_weapon.currentammo = combatant.current_weapon.reload
                                    attackcomplete = True
                                else:
                                    #Use Lightning Reflexes to bonus action reload
                                    print_output(combatant.name + ' used their Bonus Action to reload ' + combatant.current_weapon.name)
                                    combatant.current_weapon.currentammo = combatant.current_weapon.reload
                                    combatant.bonus_action_used = True                                        

                    #Advantage/disadvantage conditions (not weapon specific)
                
                    #Check condition of target                
                    if combatant.target.prone and range_attack:
                        print_output(combatant.target.name + ' is prone on the ground, giving ' + combatant.name + ' disadvantage on the attack!')
                        disadvantage = True

                    #Check assassination flag
                    if combatant.can_assassinate_target:
                        print_output(combatant.name + ' reacts with supernatural speed, and can Assassinate ' + combatant.target.name + ', gaining advantage on the attack')
                        advantage = True

                    #Did the target use reckless attack last round?
                    if combatant.target.use_reckless and not range_attack:
                        print_output(combatant.name + ' has advantage on the strike, as ' + combatant.target.name + ' used Reckless Attack last round!')
                        advantage = True

                    #Can we use reckless attack?
                    if combatant.reckless and not advantage:
                        combatant.use_reckless = True
                        print_output(combatant.name + ' uses Reckless Attack, gaining advantage on the strike')
                        advantage = True

                    #Is Vow of Enmity up?
                    if combatant.vow_of_enmity_target == combatant.target:
                        print_output(combatant.name + ' has advantage on the strike from their Vow of Enmity!')
                        advantage = True
                    
                    #Modifier conditions (i.e. GWM, sharpshooter)        
                    if combatant.sharpshooter and range_attack:
                        if (combatant.target.armour_class < to_hit_modifier+5) and not disadvantage:
                            print_output(combatant.name + ' uses Sharpshooter, taking a -5 penalty to the attack')
                            combatant.use_sharpshooter = True           
                        else:
                            combatant.use_sharpshooter = False
        
                    #Great Weapon Master
                    if combatant.current_weapon.heavy and combatant.great_weapon_master:
                        if (combatant.target.armour_class < to_hit_modifier+5) and not disadvantage:
                            print_output(combatant.name + ' uses Great Weapon Master, taking a -5 penalty to the attack')
                            combatant.use_great_weapon_master = True           

                    # Other weapon pre-attack features
                    # Called shot (Gunslinger)
                    if combatant.current_weapon.weapon_type == weapon_type.Firearm and not attackcomplete:
                        # check to spend grit for trick shot if available #
                        if combatant.current_grit > 0:
                            # legs trick shot #
                            # don't bother if we have disadvantage on the shot
                            if not disadvantage:
                                print_output(combatant.name + ' spends 1 Grit Point to perform a Leg Trick Shot. Current Grit: ' + repr(combatant.current_grit-1))
                                combatant.current_grit -= 1
                                calledshot = True

                    # Make attack roll # 
                    if not attackcomplete:
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
                        
                        #Decide if we need to use luck to reroll
                            #If the savingthrow fails, and we could make it with a decent roll (say higher than 15), and we have luck, spend luck to reroll the d20
                        if combatant.luck_uses > 0 and (atkroll + to_hit_modifier < combatant.target.armour_class):
                            luck_roll = use_luck(combatant)
                            if luck_roll > atkroll:                                
                                atkroll = luck_roll                                                                

                        #Track critical 
                        crit = False
                        if atkroll >= calc_min_crit(combatant):
                            crit = True
                            print_output('************************')
                            print_output('It\'s a CRITICAL ROLE!!!')
                            print_output('************************')

                        # After-roll weapon features
                        if combatant.current_weapon.weapon_type == weapon_type.Firearm:
                            if combatant.current_weapon.misfire >= atkroll:
                                # weapon misfire, attack fail #
                                print_output(combatant.name + 's attack misfired with a natural ' + repr(atkroll) + '! ' + combatant.current_weapon.name + ' is now broken!')
                                combatant.current_weapon.broken = True
                                attackcomplete = True
                
                    # Resolve attack
                    if not attackcomplete:
                        totalatk = atkroll + to_hit_modifier;
                        feat_penalty = 0
                        feat_bonus = 0
                        track_hemo = False

                        dice_damage = 0
                        weapon_damage_type = damage_type.Bludgeoning
                        bonus_dice_damage = 0
                        bonus_damage_type = damage_type.Bludgeoning
                        crit_bonus_dice_damage = 0
                        crit_bonus_damage_type = damage_type.Bludgeoning
                        equipment_damage = 0
                        equipment_damage_type = 0

                        #Resolve sharpshooter/great weapon master
                        if combatant.use_sharpshooter: 
                            feat_penalty = 5
                            totalatk = totalatk-feat_penalty

                        if combatant.use_great_weapon_master:
                            feat_penalty = 5
                            totalatk = totalatk-feat_penalty
                
                        totalAC = combatant.target.armour_class + combatant.target.hasted_bonus_armour

                        if totalatk >= totalAC:
                            #Update statistics
                            combatant.attacks_hit += 1

                            if feat_penalty == 0:
                                print_output(combatant.name + '\'s attack with ' + combatant.current_weapon.name + ' on ' + combatant.target.name + ' hit! (' + repr(atkroll) + ' + ' + repr(to_hit_modifier) + ' versus AC ' + repr(totalAC) + ')')            
                            else:
                                print_output(combatant.name + '\'s attack with ' + combatant.current_weapon.name + ' on ' + combatant.target.name + ' hit! (' + repr(atkroll) + ' + ' + repr(to_hit_modifier) + ' - ' + repr(feat_penalty) + ' = ' + repr(totalatk) + ' versus AC ' + repr(totalAC) + ')')            
                            if combatant.target.conscious == False and not crit and combatant.current_weapon.range == 0:
                                print_output('The blow strikes the unconscious form of ' + combatant.target.name + ' and deals CRITICAL DAMAGE!')
                                crit = True       
                            
                            # resolve trick shot #
                            if calledshot:
                                # logic to choose the right kind of called shot? lol #
                                if savingthrow(combatant.target,saving_throw.Strength,strmod(combatant.target),combatant.target.saves.str_adv,8+combatant.proficiency + dexmod(combatant)):
                                    print_output(combatant.target.name + ' succeeded on the Leg Shot save, and remains standing')
                                else:
                                    print_output(combatant.target.name + ' failed the Leg Shot save - they are now prone!')
                                    combatant.target.prone = True
                                         
                            # Calculate damage modifier (adds strmod/dexmod to attack)
                            damage_modifier = calc_damage_modifier(combatant)

                            # Calculate main attack dice
                            print_output(indent() + combatant.current_weapon.name + ' deals ' + repr(combatant.current_weapon.damage_die_count) + 'd' + repr(combatant.current_weapon.damage_die) + ' + ' + repr(damage_modifier) + ' '  + combatant.current_weapon.weapon_damage_type.name + ' damage: ')
                            weapon_damage_type = damage_type(combatant.current_weapon.weapon_damage_type)
                            for x in range(0,combatant.current_weapon.damage_die_count):                                    
                                die_damage = roll_die(combatant.current_weapon.damage_die)   
                                print_output(doubleindent() + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.current_weapon.damage_die) + ' (Weapon Damage)')
                                #Great Weapon Fighting (reroll 1s and 2s)                                                
                                if greatweaponfighting(combatant) and die_damage <= 2:
                                    print_output(doubleindent() + combatant.name + ' rerolled a weapon die due to Great Weapon Fighting!')
                                    die_damage = roll_die(combatant.current_weapon.damage_die)   
                                    print_output(doubleindent() + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.current_weapon.damage_die) + ' (Weapon Damage)')    
                                dice_damage += die_damage                    
                            
                            # Sneak attack (if we had advantage on the strike)
                            if advantage and combatant.sneak_attack and not combatant.sneak_attack_used:
                                print_output(indent() + combatant.name + ' deals Sneak Attack damage with their attack!')
                                for x in range(0,combatant.sneak_attack_damage_die_count):                                    
                                    die_damage = roll_die(combatant.sneak_attack_damage_die)
                                    print_output(doubleindent() + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.sneak_attack_damage_die) + ' (Sneak Attack Damage)')
                                    dice_damage += die_damage
                                combatant.sneak_attack_used = True

                            if crit:
                                dice_damage = dice_damage * 2
                                                                        
                                # restore grit on critical # 
                                if combatant.current_grit < combatant.max_grit:
                                    print_output(indent() + combatant.name + ' regained 1 grit point for scoring a critical hit!')
                                    combatant.current_grit = combatant.current_grit + 1;
                    
                                #Brutal Critical feature
                                if combatant.brutal_critical:
                                    print_output(indent() + combatant.name + ' dealt massive damage with Brutal Critical! Rolling an additional ' + repr(combatant.brutal_critical_dice) + ' d' + repr(combatant.current_weapon.damage_die))
                                    for x in range(0,combatant.brutal_critical_dice):                            
                                        die_damage = roll_die(combatant.current_weapon.damage_die)            
                                        print_output(doubleindent() + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.current_weapon.damage_die) + ' (Brutal Critical damage)')
                                        #Per https://www.reddit.com/r/criticalrole/comments/823w9v/spoilers_c1_another_dnd_combat_simulation/dv7r55m/
                                        # Brutal Critical does not benefit from Great Weapon Fighting (only applies to the attack)
                                        #if greatweaponfighting and die_damage <= 2:
                                        #    print_output(combatant.name + ' rerolled a weapon die due to Great Weapon Fighting!')                                           
                                        #    die_damage = roll_die(combatant.current_weapon.damage_die)            
                                        #    print_output(combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.current_weapon.damage_die) + ' (Brutal Critical damage)')
                                        dice_damage += die_damage              
                            
                                #Hemorraghing Critical feature
                                if combatant.hemorrhaging_critical and combatant.current_weapon.weapon_type == weapon_type.Firearm:
                                    print_output(indent() + combatant.name + ' scored a Hemorraghing Critical!')
                                    #Set boolean to track and increase hemo damage (possible multiple crits per round)
                                    track_hemo = True                                                
                
                            if combatant.use_sharpshooter:
                                feat_bonus = 10
                                print_output(indent() + combatant.name + ' dealt an additional ' + repr(feat_bonus) + ' damage because of Sharpshooter')

                            if combatant.use_great_weapon_master:
                                feat_bonus = 10
                                print_output(indent() + combatant.name + ' dealt an additional ' + repr(feat_bonus) + ' damage because of Great Weapon Master')
                
                            totaldamage = dice_damage + damage_modifier + feat_bonus            

                            if feat_bonus == 0:
                                print_output(indent() + combatant.name + '\'s strike dealt a total of ' + repr(totaldamage) + ' points of ' + weapon_damage_type.name + ' damage (Dice: ' + repr(dice_damage) + ' Modifier: ' + repr(damage_modifier) + ')')
                            else:
                                print_output(indent() + combatant.name + '\'s strike dealt a total of ' + repr(totaldamage) + ' points of ' + weapon_damage_type.name + ' damage (Dice: ' + repr(dice_damage) + ' Modifier: ' + repr(damage_modifier) + ' Bonus ' + repr(feat_bonus) + ')')
                            deal_damage(combatant,combatant.target,totaldamage,weapon_damage_type,combatant.current_weapon.magic)
                
                            if track_hemo:
                                print_output(indent() + combatant.name + ' adds an extra ' + repr(int(totaldamage/2)) + ' damage via Hemorrhaging Critical, which will be dealt at the end of ' + combatant.target.name + '\'s turn.')
                                combatant.target.hemo_damage += int(totaldamage/2)
                                combatant.target.hemo_damage_type = weapon_damage_type
                                track_hemo = False

                            #Bonus damage (from weapon)
                            if combatant.current_weapon.bonus_damage_die > 0:
                                print_output(indent() + 'The strike from ' + combatant.current_weapon.name + ' deals an additional ' + repr(combatant.current_weapon.bonus_damage_die_count) + 'd' + repr(combatant.current_weapon.bonus_damage_die) + ' ' + combatant.current_weapon.bonus_damage_type.name + ' damage!')
                                resolve_bonus_damage(combatant,combatant.current_weapon.bonus_damage_target,combatant.current_weapon.bonus_damage_type,combatant.current_weapon.bonus_damage_die,combatant.current_weapon.bonus_damage_die_count,0,crit,combatant.current_weapon.name)
                        
                            #Bonus damage (from hand of Vecna, 2d8 cold damage on melee hit)
                            for item in combatant.equipment_inventory():
                                if item.grants_equipment_spell == equipment_spells.HandOfVecna and combatant.current_weapon.range == 0:
                                    print_output(indent() + combatant.name + '\'s left hand crackles with power! They dealt bonus damage with the ' + item.name)
                                    resolve_bonus_damage(combatant,0,item.damage_type,item.damage_die,item.damage_die_count,0,crit,item.name)
                        
                            # Bonus damage (from critical weapon effect)
                            if crit and combatant.current_weapon.crit_bonus_damage_die > 0:
                                print_output(indent() + combatant.current_weapon.name + ' surges with power, dealing bonus damage on a critical strike!')                            
                                resolve_bonus_damage(combatant,0,combatant.current_weapon.crit_bonus_damage_type,combatant.current_weapon.crit_bonus_damage_die,combatant.current_weapon.crit_bonus_damage_die_count,0,crit,combatant.current_weapon.name)                        

                            # Bonus damage (from Zealot's Divine Fury - 1d6 + half barbairna level, damage type selected by player)
                            if combatant.divine_fury:
                                if not combatant.divine_fury_used:
                                    print_output(indent() + combatant.name + '\'s weapon crackles with the strength of their Divine Fury, dealing bonus damage!')

                                    resolve_bonus_damage(combatant,0,combatant.divine_fury_damage_type,6,1,math.floor(get_combatant_class_level(combatant,player_class.Barbarian)/2),crit,"Divine Fury")
                                    combatant.divine_fury_used = True

                            # Bonus damage (from Improved Divine Smite)
                            if combatant.improved_divine_smite:
                                print_output(indent() + combatant.name + '\'s eyes glow, as their attacks are infused with radiant energy from Improved Divine Smite!')                                                    
                                resolve_bonus_damage(combatant,0,damage_type.Radiant,8,1,0,crit,"Improved Divine Smite")

                            #Conditionally cast spells/use items on crit after initial damage resolved
                            #Smite (ideally you would only do this on crit)
                            for spell in combatant.spell_list():
                                if spell.name == "Divine Smite":
                                    #Casting Divine Smite should be the last resolution of any attack action
                                    #Casting a spell calls its own 'resolve_damage' function
                                    cast_spell(combatant,spell,crit)

                            if crit:                            
                                #Cabal's Ruin
                                #Only use cabal's on a crit, dump all charges
                                for eq in combatant.equipment_inventory():
                                    if eq.grants_equipment_spell == equipment_spells.CabalsRuin:                              
                                        equipment_damage_type = eq.damage_type
                                        if eq.current_charges > 0:
                                            print_output(indent() + combatant.name + ' activates ' + eq.name + ', pouring ' +  repr(eq.current_charges) + ' charges into ' + combatant.target.name + '!')
                                            for x in range(0,eq.current_charges):
                                                die_damage = roll_die(eq.damage_die)                                
                                                equipment_damage += die_damage * 2         
                                                print_output(doubleindent() + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(eq.damage_die) + ' (Cabal\'s Ruin damage)')
                                            eq.current_charges = 0                
                                            print_output(indent() + combatant.name + ' dealt an additional ' + repr(equipment_damage) + ' points of ' + equipment_damage_type.name + ' damage with ' + eq.name)
                                            deal_damage(combatant,combatant.target,equipment_damage,equipment_damage_type,True)
                
                            #After all the damage from the attack action is resolved, check the fatality
                            #Do this sparingly or players wlil die multiple times from one attack 
                            #i.e. activate relentless rage each time they drop below 0
                            if combatant.target.conscious:
                                resolve_damage(combatant.target)
                            else:                            
                                if crit:
                                    print_output('***' + 'The critical blow strikes the unconscious form of ' + combatant.target.name + ' and causes them to fail two Death Saving Throws!' + '***')
                                    combatant.target.death_saving_throw_failure += 2
                                else:
                                    print_output('***' + 'The blow strikes the unconscious form of ' + combatant.target.name + ' and causes them to fail a Death Saving Throw!' + '***')
                                    combatant.target.death_saving_throw_failure += 1
                            
                                print_output(indent() + 'Death Saving Throw Successes: ' + repr(combatant.target.death_saving_throw_success) + ' Failures: ' + repr(combatant.target.death_saving_throw_failure))

                            resolve_fatality(combatant.target)
                        else:
                            print_output(combatant.name + '\'s attack on ' + combatant.target.name + ' with ' + combatant.current_weapon.name + ' MISSED! (' + repr(totalatk) + ' versus AC ' + repr(totalAC) + ')')            
                            #Update statistics
                            combatant.attacks_missed += 1

                        # consume ammo after shot #
                        if combatant.current_weapon.reload > 0:
                            combatant.current_weapon.currentammo = combatant.current_weapon.currentammo - 1            

                        #Thrown weapons get automatically unequipped after being thrown
                        if combatant.current_weapon.was_thrown == True:                            
                            weapon_swap(combatant,calc_distance(combatant,combatant.target))
                        
                        attackcomplete = True
            else:
                print_output(combatant.target.name + ' is dead on the ground, and not worthy of an attack.')
        else:
            print_output(combatant.target.name + ' is out of range of ' + combatant.current_weapon.name + '!')

#Cast a spell  
def cast_spell(combatant,spell,crit):
    #Check if a spell slot is available to be used
    #Always use highest level spellslot to cast spell (for now...)
    spellslot = get_highest_spellslot(combatant,spell)
    #See if a spellslot was returned by the function
    if spellslot:               
        #Check that components (V,S,M) are available for spell?
        #Evaluate if spell is targetted or self (i.e. buff?)?
        #Check that target is in range of spell (spells with range 0 always satisfy this condition - i.e. Divine Smite is tied to attack)
        if (spell.range == 0) or calc_distance(combatant,combatant.target) <= spell.range:
            #Resolve saving throw
            #if spell.saving_throw:
                #Resolve saving throw to see if damage/condition is applied
            #Consume the spell slot from player's available slots
            print_output(combatant.name + ' is burning a ' + numbered_list(spellslot.level) + ' level spellslot to cast ' + spell.name)                            
            # Deduct one usage from the spellslot
            spellslot.current -= 1             
            
            print_output(indent() + 'Rolling spell damage:')                        
            spell_damage = 0
            if spell.damage_die > 0:
                # Start with base damage of spell
                for x in range(0,spell.damage_die_count):
                    die_damage = roll_die(spell.damage_die)
                    print_output(doubleindent() + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(spell.damage_die) + ' (Spell Damage)')
                    spell_damage += die_damage

                #Add additional damage for levels of expended spell slot
                if spellslot.level > spell.min_spellslot_level:
                    # If the spell gains no benefit for spells higher than the maximum, we still burn the higher slot, but only get benefit from the maximum against the spell                
                    if spell.max_spellslot_level < spellslot.level:
                        spellslot_bonus = spell.max_spellslot_level
                    else:
                        spellslot_bonus = spellslot.level                
                
                    for x in range(spell.min_spellslot_level,spellslot_bonus):
                        for y in range(0,spell.damage_die_count_per_spell_slot):
                            die_damage = roll_die(spell.damage_die_per_spell_slot)
                            print_output(doubleindent() + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(spell.damage_die_per_spell_slot) + ' (Additional Spell Damage from Spell Slot)')
                            spell_damage += die_damage

                #Add bonus damage
                if combatant.target.race == spell.bonus_damage_target:
                    for x in range(0,spell.bonus_damage_die_count):
                        die_damage = roll_die(spell.bonus_damage_die)
                        spell_damage += die_damage
            
            #Double dice if crit
            if crit:
                spell_damage = spell_damage * 2
            # Add modifier

            print_output(indent() + combatant.name + ' cast ' + spell.name + ' and dealt a total of ' + repr(spell_damage) + ' points of ' + spell.damage_type.name + ' damage!')                    
            deal_damage(combatant,combatant.target,spell_damage,spell.damage_type,True)
            #Resolve spell damage immediately
            resolve_damage(combatant.target)

            #Check if we have spellslots left
            if spellslot.current == 0:
                print_output(combatant.name + ' has no ' + numbered_list(spellslot.level) + ' level spellslots remaining!')

def get_highest_spellslot(combatant,spell):
    # Sort spells by level (use highest slots first)
    initkey = operator.attrgetter("level")
    sorted_spells = sorted(combatant.spellslots(), key=initkey,reverse=True)    

    for spellslot in sorted_spells:
        if spellslot.level >= spell.min_spellslot_level and spellslot.current > 0:
            return spellslot             
    
def repair_weapon(combatant):
    print_output(combatant.name + ' attempts to repair ' + combatant.current_weapon.name)    
    if abilitycheck(combatant,ability_check.Dexterity,dexmod(combatant)+combatant.proficiency,False,10+combatant.current_weapon.misfire):  
        print_output(combatant.name + ' successfully repaired ' + combatant.current_weapon.name)
        combatant.current_weapon.broken = False
    else:
        combatant.current_weapon.broken = True
        combatant.current_weapon.ruined = True
        print_output(combatant.current_weapon.name + ' has been ruined in the repair attempt! ' + combatant.name + ' needs to go back to their workshop to fix it! ')

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
            if greatweaponfighting(combatant) and die_damage <= 2 and source == combatant.current_weapon.name:
                print_output(doubleindent() + combatant.name + ' rerolled a weapon die due to Great Weapon Fighting!')
                die_damage = roll_die(die)
                print_output(doubleindent() + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(die) + ' (' + source + ' (Bonus Damage)')
            bonus_damage += die_damage
        if crit:
            crit_damage = bonus_damage * 2           
                        
    if crit:
        print_output(indent() + combatant.name + ' dealt an additional ' + repr(crit_damage+flat) + ' (roll = ' + repr(bonus_damage) + ') points of ' + type.name + ' damage with ' + source)
        deal_damage(combatant,combatant.target,crit_damage+flat,type,combatant.current_weapon.magic)
    else:
        print_output(indent() + combatant.name + ' dealt an additional ' + repr(bonus_damage+flat) + ' points of ' + type.name + ' damage with ' + source)
        deal_damage(combatant,combatant.target,bonus_damage+flat,type,combatant.current_weapon.magic)

def resolve_hemo_damage(combatant):        
    #Gunslinger - Hemorrhaging Shot; damage and type is stored against the target and resolved after the target takes its turn (treated as nonmagical always?)
    if combatant.hemo_damage > 0:
        print_output(combatant.name + ' bleeds profusely from an earlier gunshot wound, suffering ' + repr(combatant.hemo_damage) + ' points of damage from Hemorrhaging Critical!')
        #hack
        #combatant.hemo_damage_type = combatant.target.current_weapon.weapon_damage_type
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
            print_output(doubleindent() + target.name + ' shrugs off ' + repr(damage) + ' points of damage in their rage!')
    if target.enlarged:
        if dealt_damage_type in (damage_type.Fire,damage_type.Cold,damage_type.Lightning):
            damage = int(damage/2)              
            print_output(doubleindent() + target.name + ' shrugs off ' + repr(damage) + ' points of damage due to the effects of Enlarge!')

    #Reduce bludgeoning/piercing/slashing if dealt by non-magical dealt_
    if target.monster_type == monster_type.Ancient_Black_Dragon:            
        if dealt_damage_type in (damage_type.Piercing,damage_type.Bludgeoning,damage_type.Slashing) and not magical:
            damage = int(damage/2)              
            print_output(doubleindent() + target.name + ' shrugs off ' + repr(damage) + ' points of damage from the non-magical attack!')

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

                # Uncanny Dodge
                if combatant.uncanny_dodge:
                    reduction = total_damage/2
                    total_damage = int(total_damage - reduction)
                    print_output(combatant.name + ' uses their reaction, and uses Uncanny Dodge to reduce the damage by ' + repr(reduction) + '! ')
                    damage_string += 'reduced by ' + repr(int(reduction)) + ' (Uncanny Dodge)'
                    combatant.reaction_used = True

            combatant.current_health = combatant.current_health - total_damage 
                        
            print_output('Damage Summary: ' + damage_string)        
            print_output(combatant.name + ' suffers a total of ' + repr(int(total_damage)) + ' points of damage. Current HP: ' + repr(int(combatant.current_health)) + '/' + repr(combatant.max_health))        

def resolve_fatality(combatant):
    if combatant.alive and combatant.conscious and combatant.current_health <= 0:
        # Default proposition - combatant goes unconscious
        combatant.conscious = False   
        print_output(combatant.name + ' is knocked unconscious by the force of the blow!')

        #Relentless rage
        if combatant.relentless_rage and combatant.raging:
            if savingthrow(combatant,saving_throw.Consitution,combatant.saves.con,False,combatant.relentless_rage_DC):
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
    
    # Turn off rage if combatant unconscious after evaluating Rage features
    if not combatant.conscious:
        combatant.raging = False

    #Resolve death
    if not combatant.alive and not combatant.conscious and combatant.current_health <=0:
        print_output('********' + 'HOW DO YOU WANT TO DO THIS??' + '********')        

def death_saving_throw(combatant):
    i = roll_die(20)
    print_output(' *** ' + combatant.name + ' makes a Death Saving Throw: they rolled a ' + repr(i) + ' *** ')
    if i <= 1:
        combatant.death_saving_throw_failure += 2
    elif i <= 9:
        combatant.death_saving_throw_failure += 1
    elif i <= 19:
        combatant.death_saving_throw_success += 1
    elif i == 20:
        combatant.death_saving_throw_success = 3
    print_output(indent() + 'Death Saving Throw Successes: ' + repr(combatant.death_saving_throw_success) + ' Failures: ' + repr(combatant.death_saving_throw_failure))

def calc_to_hit_modifier(combatant):
    to_hit = 0
    # Add 2 for fighting style when using ranged weapon with Archery
    if combatant.fighting_style == fighting_style.Archery and combatant.current_weapon.range > 0:
        to_hit += 2;

    # Add Dex modifier for finesse weapons, otherwise Str
    if combatant.current_weapon.finesse:
        to_hit += dexmod(combatant)
    else:
        to_hit += strmod(combatant)

    # Add proficiency bonus if proficiency in weapon
    for combatant_weapon_proficiency in combatant.weapon_proficiency():
        if combatant.current_weapon.weapon_type != 0 and combatant.current_weapon.weapon_type == combatant_weapon_proficiency:
            to_hit += combatant.proficiency

    # Add weapon bonus (i.e. +3 weapon)
    to_hit += combatant.current_weapon.magic_to_hit_modifier
        
    return to_hit

def calc_damage_modifier(combatant):
    damage = 0
    
    # Add Dex modifier for finesse weapons, otherwise Str
    if combatant.current_weapon.finesse:
        damage += dexmod(combatant)
    else:
        damage += strmod(combatant)

    # Rage
    if combatant.raging and not combatant.armour_type == armour_type.Heavy:
        damage += combatant.ragedamage
    
    # Add weapon bonus (i.e. +3 weapon)
    damage += combatant.current_weapon.magic_damage_modifier
        
    return damage


def calc_min_crit(combatant):
    min_crit = 20
    # Vicious Intent, crit on a 19
    if combatant.vicious_intent and combatant.current_weapon.weapon_type == weapon_type.Firearm:
        min_crit = 19
    return min_crit

# roll functions #
def roll_die(die):
    random.seed
    return random.randint(1,die)

def use_luck(combatant):
    if combatant.luck_uses > 0:        
        random.seed
        luck_die_roll = random.randint(1,20)        
        combatant.luck_uses -= 1
        print_output(indent() + combatant.name + ' used a point of Luck, and rolled a ' + repr(luck_die_roll) + ' on the lucky d20!')
        return(luck_die_roll)        

# mod functions #

def strmod(combatant):
    return math.floor((combatant.stats.str-10)/2)

def dexmod(combatant):
    return math.floor((combatant.stats.dex-10)/2)

def intmod(combatant):
    return math.floor((combatant.stats.intel-10)/2)

def wismod(combatant):
    return math.floor((combatant.stats.wis-10)/2)

def conmod(combatant):
    return math.floor((combatant.stats.con-10)/2)

def chamod(combatant):
    return math.floor((combatant.stats.cha-10)/2)

# save functions #

def savingthrow(combatant,savetype,modifier,adv,DC):
    print_output('<i>Saving Throw</i>')
    roll = roll_die(20)
    savingthrow = roll + modifier    
    #print_output(savetype + ' save: Natural roll: ' + repr(roll) + ', modifier: ' + repr(modifier))
    if savingthrow >= DC:
        print_output(indent() + combatant.name + ' succeeded on a DC' + repr(DC) + ' ' + savetype.name + ' save with a saving throw of ' + repr(savingthrow))
        return True
    if adv:
        #print_output(combatant.name + ' failed the save, but has advantage on ' + savetype + ' saving throws!')
        roll = roll_die(20)
        savingthrow = roll + modifier
        #print_output(savetype + ' save: Natural roll: ' + repr(roll) + ', modifier: ' + repr(modifier))        
        if savingthrow >= DC:
            print_output(indent() + combatant.name + ' succeeded on a DC' + repr(DC) + ' ' + savetype.name + ' save with a saving throw of ' + repr(savingthrow))
            return True

    #If the savingthrow fails, and we could make it with a decent roll (say higher than 15), and we have luck, spend luck to reroll the d20
    if combatant.luck_uses > 0 and (DC - modifier <= 15):
        luck_roll = use_luck(combatant)
        if luck_roll > roll:
            savingthrow = luck_roll + modifier
            if savingthrow >= DC:
                print_output(indent() + combatant.name + ' used a point of Luck, and has now succeeded on a DC' + repr(DC) + ' ' + savetype.name + ' save with a saving throw of ' + repr(savingthrow))
                return True

    print_output(indent() + combatant.name + ' FAILED on a DC' + repr(DC) + ' ' + savetype.name + ' save with a saving throw of ' + repr(savingthrow))
    return False

# check functions #
def abilitycheck(combatant,checktype,modifier,adv,DC):    
    #Pass a DC of 0 to just return the check value (i.e. Initiative, Perception)
    roll = roll_die(20)
    check = roll + modifier
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
    initiativeroll = abilitycheck(combatant,ability_check.Dexterity,dexmod(combatant),False,0)      
    if combatant.feral_instinct:
        initiativeroll_adv = abilitycheck(combatant,ability_check.Dexterity,dexmod(combatant),True,0)
        initiativeroll = max(initiativeroll,initiativeroll_adv)
    if combatant.quickdraw:
        initiativeroll += combatant.proficiency
    combatant.initiative_roll = initiativeroll

# Position/movement functions
def getposition(combatant):
    return(combatant.xpos,combatant.ypos)

def move_grid(combatant,direction):
    if direction == cardinal_direction.Stay:
        return 

    xpos = 0
    ypos = 0
    initialxpos = combatant.xpos
    initialypos = combatant.ypos    

    #1 = Southwest
    #2 = South
    #3 = Southeast
    #4 = East
    #5 = NorthEast
    #6 = North
    #7 = Northwest
    #8 = West    
    #9 = Random

    if direction == None or direction == cardinal_direction.Random:       
        rand_direction = random.randint(1,8)
        direction = cardinal_direction(rand_direction)

        print_output(indent() + combatant.name + ' chooses to travel ' + direction.name)

    if direction == cardinal_direction.SouthWest:
        xpos = -5
        ypos = -5
    elif direction == cardinal_direction.South:
        xpos = 0
        ypos = -5
    elif direction == cardinal_direction.SouthEast:
        xpos = 5
        ypos = -5
    elif direction == cardinal_direction.East:
        xpos = 5
        ypos = 0
    elif direction == cardinal_direction.NorthEast:
        xpos = 5
        ypos = 5
    elif direction == cardinal_direction.North:
        xpos = 0
        ypos = 5
    elif direction == cardinal_direction.NorthWest:
        xpos = -5
        ypos = 5
    elif direction == cardinal_direction.West:
        xpos = -5
        ypos = 0

    combatant.xpos += xpos;
    combatant.ypos += ypos;

    print_output(indent() + combatant.name + ' moves ' + direction.name + ' from (' + repr(initialxpos) + ',' + repr(initialypos) + ') to (' + repr(combatant.xpos) + ',' + repr(combatant.ypos) + ')')

def calc_distance(combatant,target):
    xdistance = int(math.fabs(combatant.xpos-target.xpos))
    ydistance = int(math.fabs(combatant.ypos-target.ypos))
    return int(math.sqrt((xdistance * xdistance) + (ydistance * ydistance)))

def move_to_target(combatant,target,movement):
    # Goal - decrease the distance between us and target
    print_output(combatant.name + ' is currently located at position: (' + repr(combatant.xpos) + ',' + repr(combatant.ypos) + '), and wants to move towards ' + combatant.target.name + ' at (' + repr(combatant.target.xpos) + ',' + repr(combatant.target.ypos) + ')')    
    initial_distance = calc_distance(combatant,target)
    initial_grids = calc_no_of_grids(initial_distance)
    grids_to_move = calc_no_of_grids(initial_distance)
    initial_grid_movement = calc_no_of_grids(movement)
    grid_movement = calc_no_of_grids(movement)
    
    print_output(combatant.name + ' has ' + repr(initial_grid_movement) + ' grids, or ' + repr(movement) + ' feet of movement to spend. (Distance to destination: ' + repr(initial_grids) + ' grids, or ' + repr(initial_distance) + ' feet)')

    grids_moved = 0
    while grids_to_move > 0 and grid_movement > 0:      
        initial_xpos = combatant.xpos
        initial_ypos = combatant.ypos

        if settings.verbose_movement:
            print_output(indent() + combatant.name + ' is ' + repr(grids_to_move) + ' grids away from their destination and has ' + repr(grid_movement) + ' grids of movement remaining')

        direction = cardinal_direction.Stay

        if combatant.xpos > target.xpos and combatant.ypos > target.ypos:
            direction = cardinal_direction.SouthWest
        elif combatant.xpos > target.xpos and combatant.ypos < target.ypos:
            direction = cardinal_direction.NorthWest
        elif combatant.xpos < target.xpos and combatant.ypos < target.ypos:
            direction = cardinal_direction.NorthEast
        elif combatant.xpos < target.xpos and combatant.ypos > target.ypos:
            direction = cardinal_direction.SouthEast
        elif combatant.xpos < target.xpos and combatant.ypos == target.ypos:
            direction = cardinal_direction.East
        elif combatant.xpos > target.xpos and combatant.ypos == target.ypos:
            direction = cardinal_direction.West
        elif combatant.xpos == target.xpos and combatant.ypos < target.ypos:
            direction = cardinal_direction.North
        elif combatant.xpos == target.xpos and combatant.ypos > target.ypos:
            direction = cardinal_direction.South
        
        move_grid(combatant,direction)  
        grids_moved += 1
        #Evaluate after each step if the target is in range of our weapon
        if target_in_weapon_range(combatant,combatant.target,combatant.current_weapon.range):                        
            print_output(indent() + combatant.name + ' skids to a halt at at (' + repr(combatant.xpos) + ',' + repr(combatant.ypos) + '), now in range of ' + combatant.target.name)
            grids_to_move = 0
            grid_movement = 0
            grids_moved -= 1

        grids_to_move -= 1
        grid_movement -= 1
        
    final_distance = calc_distance(combatant,combatant.target)
    final_grid_distance = calc_no_of_grids(final_distance)
    used_movement = grids_moved*5
    print_output(combatant.name + ' uses ' + repr(grids_moved) + ' grids, or ' + repr(used_movement) + ' feet of their movement to travel towards ' + combatant.target.name + ' (Distance to target: ' + repr(final_grid_distance) + ' grids, or ' + repr(final_distance) + ' feet)')

def move_from_target(combatant,target,movement):
    # Goal - extend the distance between us and target
    #Essentially figure out where we are in relation to the target, and keep travelling in that direction
    print_output(combatant.name + ' is currently located at position: (' + repr(combatant.xpos) + ',' + repr(combatant.ypos) + '), and wants to move away from ' + combatant.target.name + ' at (' + repr(combatant.target.xpos) + ',' + repr(combatant.target.ypos) + ')')
    initial_distance = movement
    initial_grids = calc_no_of_grids(initial_distance)    

    grids_to_move = calc_no_of_grids(initial_distance)
    grid_movement = calc_no_of_grids(movement)
    
    print_output(combatant.name + ' has ' + repr(grid_movement) + ' grids, or ' + repr(movement) + ' feet of movement to spend. (Distance to destination: ' + repr(initial_grids) + ' grids, or ' + repr(initial_distance) + ' feet)')

    grids_moved = 0
    while grids_to_move > 0 and grid_movement > 0:
        initial_xpos = combatant.xpos
        initial_ypos = combatant.ypos

        if settings.verbose_movement:
            print_output(indent() + combatant.name + ' is ' + repr(grids_to_move) + ' grids away from their destination and has ' + repr(grid_movement) + ' grids of movement remaining')

        direction = cardinal_direction.Stay

        if combatant.xpos == target.xpos and combatant.ypos == target.ypos:
            #Choose a random direction to move in         
            direction = cardinal_direction.Random
        elif combatant.xpos > target.xpos and combatant.ypos > target.ypos:
            direction = cardinal_direction.NorthEast
        elif combatant.xpos > target.xpos and combatant.ypos < target.ypos:
            direction = cardinal_direction.SouthEast
        elif combatant.xpos < target.xpos and combatant.ypos < target.ypos:
            direction = cardinal_direction.SouthWest
        elif combatant.xpos < target.xpos and combatant.ypos > target.ypos:
            direction = cardinal_direction.NorthWest
        elif combatant.xpos < target.xpos and combatant.ypos == target.ypos:
            direction = cardinal_direction.West
        elif combatant.xpos > target.xpos and combatant.ypos == target.ypos:
            direction = cardinal_direction.East
        elif combatant.xpos == target.xpos and combatant.ypos < target.ypos:
            direction = cardinal_direction.South
        elif combatant.xpos == target.xpos and combatant.ypos > target.ypos:
            direction = cardinal_direction.North
                
        if direction != 0:
            move_grid(combatant,direction)         
            grids_moved += 1
        
        #If we haven't attacked yet, we don't want to run out of our weapon range
        #If movement would take us outside the maximum range of our weapon, stop here instead
        if not combatant.action_used: 
            if not target_in_weapon_range(combatant,combatant.target,combatant.current_weapon.range):                        
                print_output(indent() + combatant.name + ' changes their mind at the last second, moving back to (' + repr(initial_xpos) + ',' + repr(initial_ypos) + ') to stay in weapon range of ' + combatant.target.name)
                combatant.xpos = initial_xpos;
                combatant.ypos = initial_ypos;
                grids_to_move = 0
                grid_movement = 0
                grids_moved -= 1

        grids_to_move -= 1
        grid_movement -= 1

    final_distance = calc_distance(combatant,combatant.target)
    final_grid_distance = calc_no_of_grids(final_distance)
    used_movement = grids_moved*5
    print_output(combatant.name + ' uses ' + repr(grids_moved) + ' grids, or ' + repr(used_movement) + ' feet of their movement to travel away from ' + combatant.target.name + ' (Distance to target: ' + repr(final_grid_distance) + ' grids, or ' + repr(final_distance) + ' feet)')
    
def calc_no_of_grids(distance):
    return(int(round(math.fabs(distance/5))))

def enemy_in_range(combatant,range):
    enemies = []
    identify_enemies(combatant,enemies)        
    for enemy in enemies:
        if calc_distance(combatant,enemy) <= range:
            return True                   
    return False

def target_in_weapon_range(combatant,target,range):
    if range == 0:        
        range = melee_range()
    #Calculate distance in feet
    distance_to_target = calc_distance(combatant,target)
    if (distance_to_target < range) or (combatant.current_weapon.reach and distance_to_target < range + 5):
        return True
    #Check that no grids are adjacent for melee attacks
    if is_adjacent(combatant,target):
        return True
    return False

def melee_range():
    #Treating default melee weapon range as 5 feet, upped to 8 to avoid clipping issues on corners of grid
    return 8

def is_adjacent(combatant,target):
    if (combatant.xpos == target.xpos) or (combatant.xpos == target.xpos-5) or (combatant.xpos == target.xpos+5):
        if (combatant.ypos == target.ypos) or (combatant.ypos == target.ypos-5) or (combatant.ypos == target.ypos+5):
            return True
    elif (combatant.ypos == target.ypos) or (combatant.ypos == target.ypos-5) or (combatant.ypos == target.ypos+5):
        if (combatant.xpos == target.xpos) or (combatant.xpos == target.xpos-5) or (combatant.xpos == target.xpos+5):
            return True
    return False

def find_target(combatant):    
    #Always set the target as a reference to the master list of combatants (to avoid having to constantly refresht to pick up changes in the target)
    combatant.target = None    
    for potential_enemy in combatants.list:
        if combatant.name != potential_enemy.name and combatant.team != potential_enemy.team:
            if potential_enemy.alive:
                if combatant.target == None or calc_distance(combatant,potential_enemy) <= calc_distance(combatant,combatant.target):
                    combatant.target = potential_enemy                
  
    if combatant.target:
        print_output(combatant.name + ' is now targetting ' + combatant.target.name)
        #Swap to an appropriate weapon as a free action
        weapon_swap(combatant,calc_distance(combatant,combatant.target))                        
        return True
    else:
        return False

# helper functions #
def greatweaponfighting(combatant):
    if combatant.fighting_style == fighting_style.Great_Weapon_Fighting and (combatant.current_weapon.two_handed or combatant.current_weapon.versatile):
        return True
    return False

def get_combatant_class_level(combatant,combatant_class):
    for class_instance in combatant.player_classes():
        if class_instance.player_class == combatant_class:
            return class_instance.player_class_level