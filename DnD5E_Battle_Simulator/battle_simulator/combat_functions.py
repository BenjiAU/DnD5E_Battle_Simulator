#Explicit imports

#Implicit imports
from .classes import *
from .print_functions import *

#Other imports
import random
import math

indent = '<div class="indent">'
doubleindent = '<div class="doubleindent">'

### Core Round functions ###
def movement(combatant):
    # Only move if a target exists
    if combatant.target:
        # movement #
        movement = combatant.speed
        if combatant.prone:
            # Spend half movement to get up #
            movement = math.floor(movement/2)
            print_output(combatant.name + ' spends ' + repr(movement) + ' feet of movement to stand up from prone ')            
            combatant.prone = False

        if combatant.current_weapon.range == 0:        
            # melee weapon #            
            if combatant.position > combatant.target.position:  
                # melee target out of range #
                if combatant.position - movement <= combatant.target.position:  
                    # movement can close gap to target # 
                    print_output(combatant.name + ' uses their movement to engage in melee with ' + combatant.target.name + '!')            
                    combatant.position = combatant.target.position
                else:
                    # movement cannot close gap to target #
                    print_output(combatant.name + ' uses their movement to travel ' + repr(movement) + ' feet towards ' + combatant.target.name)            
                    combatant.position -= movement
        else:
            # range weapon #
            if combatant.position < combatant.target.position and getdistance(combatant.position,combatant.target.position) <= combatant.current_weapon.range:  
                # distance between target, kite #
                if getdistance(combatant.position - movement,combatant.target.position) < combatant.current_weapon.range:  
                    print_output(combatant.name + ' uses their movement to travel ' + repr(movement) + ' feet away from ' + combatant.target.name)            
                    combatant.position -= movement
                else:
                    movement = combatant.current_weapon.range - getdistance(combatant.position,combatant.target.position)
                    if movement != 0:
                        print_output(combatant.name + ' uses part of their movement to travel ' + repr(movement) + ' feet away from ' + combatant.target.name)            
                        combatant.position -= movement
                    else:
                        print_output(combatant.name + ' stays where they are.')
            else:
                print_output(combatant.name + ' stays where they are.')            

    combatant.movement_used = True

def action(combatant):
    # Only perform an action if target exists
    if combatant.target:
        # Iterate through equipment and use any available spells (if possible)
        for eq in combatant.equipment_inventory():
            if eq.grants_equipment_spell == equipment_spells.Enlarge:
                if not combatant.enlarged:
                    print_output(combatant.name + ' smashes the ' + eq.name + ' together and grows in size!')            
                    combatant.enlarged = True
                    combatant.action_used = True
        
        #Custom monster logic before stepping into main loop
        if combatant.creature_class == creature_class.Monster:
            if combatant.breath_attack and (combatant.breath_range >= getdistance(combatant.position,combatant.target.position)):            
                breath_attack(combatant)
                combatant.action_used = True

        if not combatant.action_used:
            # Swap to a different weapon if it makes sense due to range                    
            current_range = getdistance(combatant.position,combatant.target.position)
            # Attempt a weapon swap - change weapons depending on range
            # This will prefer to swap a non-broken or ruined weapon in
            weapon_swap(combatant,current_range)

            if combatant.current_weapon.range == 0:
                # melee weapon #
                if combatant.position > combatant.target.position:  
                    # melee target out of range - using Action to Dash #
                    movement = combatant.speed
                    print_output(combatant.name + ' uses the Dash action, travelling towards ' + combatant.target.name)
                    if combatant.position - movement <= combatant.target.position:  
                        # movement can close gap to target # 
                        combatant.position = combatant.target.position
                    else:
                        # movement cannot close gap to target #
                        combatant.position -= movement
                else:
                    # melee target in range - using Action to Attack #
                    attack_action(combatant)
            else:
                # If the weapon is Ruined, and we could not swap to a non-ruined weapon, we're out of luck
                if combatant.current_weapon.ruined:
                    print_output(combatant.name + ' can\'t do anything with ' + combatant.current_weapon.name + ', it is damaged beyond repair!')
                    # Can't swap to a valid weapon - just have to sit this one out
                    combatant.action_used = True

                # If the weaopn is broken, and we could not swap to a non-broken weapon, must waste action reparing it
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
        #Rage
        if not combatant.bonus_action_used:
            if combatant.canrage and not combatant.raging:
                print_output(combatant.name + ' uses their Bonus Action to go into a mindless rage! "I would like to RAAAGE!!!"')
                combatant.raging = True;
                combatant.bonus_action_used = True
                # Rage grants advantage on strength checks/saving throws for its duration
                if combatant.armour_type != armour_type.Heavy:
                    combatant.saves.str_adv = True
                    combatant.checks.str_adv = True

        #Second Wind
        if not combatant.bonus_action_used:
            if combatant.second_wind:
                #Don't use Second Wind unless current HP is more than 10+fighter level less than max
                if combatant.current_health + 10 + combatant.fighter_level < combatant.max_health:
                    second_wind_heal = roll_weapon_die(10) + combatant.fighter_level
                    combatant.current_health += second_wind_heal
                    print_output(combatant.name + ' uses their Bonus Action to gain a Second Wind, and restores ' + repr(second_wind_heal) + ' hit points!')
                    combatant.second_wind = False
                    combatant.bonus_action_used = True

        #Frenzy
        if not combatant.bonus_action_used:
            if combatant.raging:
                if combatant.frenzy:            
                    if combatant.position == combatant.target.position:
                        print_output(combatant.name + ' uses their Bonus Action to make a frenzied weapon attack against ' + combatant.target.name)
                        attack(combatant)            
                        combatant.bonus_action_used = True
                        
        #Boots of Feral Leaping        
        if not combatant.bonus_action_used:
            for item in combatant.equipment_inventory():
                if item.grants_equipment_spell == equipment_spells.Leap:
                    if combatant.position != combatant.target.position:
                        print_output(combatant.name + ' is taking a flying leap using his ' + item.name + ' as a Bonus Action!')
                        if abilitycheck(combatant,ability_check.Strength,strmod(combatant),combatant.checks.str_adv,16):
                            print_output(combatant.name + ' leaps forward 20 feet')
                            if combatant.position - 20 <= combatant.target.position:
                                #movement can close gap to target # 
                                combatant.position = combatant.target.position
                            else:
                                #movement cannot close gap to target #
                                combatant.position -= 20
                        else:
                            print_output(combatant.name + ' fell over where he stands!')
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

#Weapon swap
def weapon_swap(combatant,current_range):
    # A weapon is already equipped; equip a new one
    if combatant.current_weapon.name != "":
        for weap in combatant.weapon_inventory():                
            # Swap to range weapon if within range (preferring shorter range non-broken weapons), unless in melee, in which case only swap to melee                        
                # swap out broken weapon, unless this is the better weapon
            if ((weap.range >= current_range and current_range != 0 and combatant.current_weapon.broken and not weap.broken) or 
                # prefer unbroken shorter range weapon
            (weap.range >= current_range and current_range != 0 and weap.range < combatant.current_weapon.range) or 
                # prefer range weapon at range over melee weapon
            (weap.range >= current_range and current_range != 0 and weap.range != 0 and combatant.current_weapon.range == 0) or
                # prefer melee weapon for melee range, but don't swap out for no reason
            (weap.range == 0 and current_range == 0 and combatant.current_weapon.range != 0)):         
                # Don't swap if we're already using this weapon
                if combatant.current_weapon != weap:
                    # Draw ruined and cry if current weapon is ruined - making it here means there are no better options
                    if weap.ruined and (combatant.current_weapon.ruined):
                        print_output(combatant.name + ' sadly puts away ' + combatant.current_weapon.name + ' and draws out the ruined ' + weap.name)                        
                        combatant.current_weapon = weap                    
                        return True
                    # Draw broken if we have to (i.e. current weapon is broken/ruined, and we need to repair the better one)                    
                    if weap.broken and (combatant.current_weapon.broken or combatant.current_weapon.ruined):  
                        print_output('Frustrated, ' + combatant.name + ' stows ' + combatant.current_weapon.name + ' and draws out the broken ' + weap.name)                        
                        combatant.current_weapon = weap                    
                        return True
                    # If the weapon is neither broken nor ruined, and it makes it here, it's the best choice
                    if not weap.ruined and not weap.broken:
                        print_output(combatant.name + ' stows ' + combatant.current_weapon.name + ' and readies ' + weap.name)                        
                        combatant.current_weapon = weap                    
                        return True                                            
    # No weapon is equipped; draw one
    else:
        for weap in combatant.weapon_inventory():    
            print_output(combatant.name + ' draws ' + weap.name + ' and prepares for battle!')
            combatant.current_weapon = weap                    
            return True
    return False

#Attack action
def attack_action(combatant):
    #one set of rules for monsters
    if combatant.creature_class == creature_class.Monster:
        if combatant.breath_attack and (combatant.breath_range >= getdistance(combatant.position,combatant.target.position)):
            breath_attack(combatant)
        else:
            if combatant.multiattack:
                #Determine which attacks out of the multiattack will reach (due to range, reach)                
                multiattack_weapons = []
                for ma in combatant.multiattack:
                    for weap in combatant.weapon_inventory():
                        if weapon.range >= getdistance(combatant.position,combatant.target.position) and ma == weap.name:                        
                            multiattack_weapons.append(weap)

                if len(multiattack_weapons) > 0:
                    print_output(combatant.name + ' unleashes a Multiattack against ' + combatant.target.name)                
                    for ma_weap in multiattack_weapons:
                        combatant.current_weapon = ma_weap
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
                    print_output(combatant.name + ' uses an Extra Attack.')
                    attack(combatant)  

def breath_attack(combatant):
    print_output(combatant.name + ' rears back and unleashes a devastating breath attack!')   
    breath_damage = 0
    breath_damage_type = 0
    die_damage = 0
    if combatant.creature_subclass == creature_subclass.Ancient_Black_Dragon:
        breath_damage_type = damage_type.Acid
        i = 1
        for i in range(1,15):
            die_damage = roll_weapon_die(combatant.breath_damage_die)
            print_output(combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.breath_damage_die) + ' (Breath Damage)')
            breath_damage += die_damage
    if savingthrow(combatant.target,saving_throw.Dexterity,dexmod(combatant.target),combatant.target.saves.dex_adv,23):
        deal_damage(combatant.target,breath_damage/2,breath_damage_type,True)
    else:
        deal_damage(combatant.target,breath_damage,breath_damage_type,True)

    combatant.breath_attack = False

    #See if the damage droped target below 0 hp
    resolve_damage(combatant.target)
    resolve_fatality(combatant.target)

def breath_recharge(combatant):    
    die = roll_weapon_die(6)
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
        if combatant.current_weapon.range >= getdistance(combatant.position,combatant.target.position):
            # only resolve attack if target is alive
            if combatant.target.alive:
                attackcomplete = False    
                calledshot = False
                advantage = False
                disadvantage = False
        
                combatant.use_sharpshooter = False
                # Recalculate all +hit modifiers (based on current weapon, fighting style, ability modifiers etc.)
                to_hit_modifier = calc_to_hit_modifier(combatant)

                # Before-roll weapon features
                if combatant.current_weapon.weapon_type == weapon_type.Firearm:
                    # Check that the Firearm is not ruined - if it is ruined, no attacks can be made
                    if not attackcomplete:
                        if combatant.current_weapon.broken and combatant.current_weapon.ruined:
                            print_output(combatant.name + ' can\'t do anything with ' + combatant.current_weapon.name + ', it is damaged beyond repair!')
                            attackcomplete = True
            
                    if not attackcomplete:
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

                    if not attackcomplete:
                        # check to spend grit for trick shot if available #
                        if combatant.current_grit > 0:
                            # legs trick shot #
                            # don't bother if target is already prone #
                            if combatant.target.prone:
                                #print_output(combatant.target.name + ' is prone on the ground - ' + combatant.name + ' is saving his Grit for later')
                                disadvantage = True
                            else:
                                print_output(combatant.name + ' spends 1 Grit Point to perform a Leg Trick Shot. Current Grit: ' + repr(combatant.current_grit-1))
                                combatant.current_grit -= 1
                                calledshot = True

                    #Check condition of target
                    if not attackcomplete:
                        if combatant.target.prone:
                            print_output(combatant.target.name + ' is prone on the ground, giving ' + combatant.name + ' disadvantage on the attack!')
                            disadvantage = True

                    if not attackcomplete:
                        #Modifier conditions (i.e. GWM, sharpshooter)        
                        if combatant.sharpshooter:
                            if (combatant.target.armour_class < to_hit_modifier+5) and not disadvantage:
                                print_output(combatant.name + ' uses Sharpshooter, taking a penalty to the attack')
                                combatant.use_sharpshooter = True           
                            else:
                                combatant.use_sharpshooter = False
        
                #Great Weapon Master
                if combatant.current_weapon.heavy and combatant.great_weapon_master:
                    if (combatant.target.armour_class < to_hit_modifier+5) and not disadvantage:
                        print_output(combatant.name + ' uses Great Weapon Master, taking a penalty to the attack')
                        combatant.use_great_weapon_master = True
            
                #Advnatage/disadvnatage conditions (not weapon specific)
                if combatant.reckless:
                    combatant.use_reckless = True
                    print_output(combatant.name + ' uses Reckless Attack, gaining advantage on the strike')
                    advantage = True

                if combatant.target.use_reckless and combatant.current_weapon.range == 0:
                    print_output(combatant.name + ' has advantage on the strike, as ' + combatant.target.name + ' used Reckless Attack last round!')
                    advantage = True

                # Make attack roll # 
                if not attackcomplete:
                    initroll = roll_d20()
                    if advantage and disadvantage:
                        atkroll = initroll
                    if advantage and not disadvantage:
                        #print_output(combatant.name + ' has advantage on the attack')
                        advroll = roll_d20()
                        atkroll = max(initroll,advroll)
                    if disadvantage and not advantage:
                        #print_output(combatant.name + ' has disadvantage on the attack')
                        disadvroll = roll_d20()
                        atkroll = min(initroll,disadvroll)
                    if not advantage and not disadvantage:
                        atkroll = initroll
            
                    print_output(combatant.name + ' rolled a ' + repr(atkroll) + ' on a d20 (attack)')

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

                    crit = False
                    track_hemo = False
                    if atkroll >= calc_min_crit(combatant):
                        crit = True
                        print_output('************************')
                        print_output('It\'s a CRITICAL ROLE!!!')
                        print_output('************************')

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
                        totalatk = totalatk-5

                    if combatant.use_great_weapon_master:
                        totalatk = totalatk-5

                    if totalatk >= combatant.target.armour_class:
                        print_output(combatant.name + '\'s attack with ' + combatant.current_weapon.name + ' on ' + combatant.target.name + ' hit! (' + repr(totalatk) + ' versus AC ' + repr(combatant.target.armour_class) + ')')            
                        print_output(indent + 'Rolling damage for weapon attack: ')
                        # resolve trick shot #
                        if calledshot:
                            # logic to choose the right kind of called shot? lol #
                            if savingthrow(combatant.target,saving_throw.Strength,strmod(combatant.target),combatant.target.saves.str_adv,8+combatant.proficiency + dexmod(combatant)):
                                print_output(combatant.target.name + ' succeeded on the Leg Shot save, and remains standing')
                            else:
                                print_output(combatant.target.name + ' failed the Leg Shot save - they are now prone!')
                                combatant.target.prone = True

                        #Great Weapon Fighting (reroll 1s and 2s)                    
                        weapon_damage_type = damage_type(combatant.current_weapon.weapon_damage_type)
                        for x in range(0,combatant.current_weapon.damage_die_count):                                    
                            die_damage = roll_weapon_die(combatant.current_weapon.damage_die)   
                            print_output(doubleindent + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.current_weapon.damage_die) + ' (Weapon Damage)')
                            if greatweaponfighting(combatant) and die_damage <= 2:
                                print_output(doubleindent + combatant.name + ' rerolled a weapon die due to Great Weapon Fighting!')
                                die_damage = roll_weapon_die(combatant.current_weapon.damage_die)   
                                print_output(doubleindent + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.current_weapon.damage_die) + ' (Weapon Damage)')    
                            dice_damage += die_damage                    
                     
                        if crit:
                            dice_damage = dice_damage * 2
                                                                        
                            # restore grit on critical # 
                            if combatant.current_grit < combatant.max_grit:
                                print_output(indent + combatant.name + ' regained 1 grit point for scoring a critical hit!')
                                combatant.current_grit = combatant.current_grit + 1;
                    
                            #Brutal Critical feature
                            if combatant.brutal_critical:
                                print_output(indent + combatant.name + ' dealt massive damage with Brutal Critical! Rolling an additional ' + repr(combatant.brutal_critical_dice) + ' d' + repr(combatant.current_weapon.damage_die))
                                for x in range(0,combatant.brutal_critical_dice):                            
                                    die_damage = roll_weapon_die(combatant.current_weapon.damage_die)            
                                    print_output(doubleindent + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.current_weapon.damage_die) + ' (Brutal Critical damage)')
                                    #Per https://www.reddit.com/r/criticalrole/comments/823w9v/spoilers_c1_another_dnd_combat_simulation/dv7r55m/
                                    # Brutal Critical does not benefit from Great Weapon Fighting (only applies to the attack)
                                    #if greatweaponfighting and die_damage <= 2:
                                    #    print_output(combatant.name + ' rerolled a weapon die due to Great Weapon Fighting!')                                           
                                    #    die_damage = roll_weapon_die(combatant.current_weapon.damage_die)            
                                    #    print_output(combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.current_weapon.damage_die) + ' (Brutal Critical damage)')
                                    dice_damage += die_damage              
                            
                            #Hemorraghing Critical feature
                            if combatant.hemorrhaging_critical and combatant.current_weapon.weapon_type == weapon_type.Firearm:
                                print_output(combatant.name + ' scored a Hemorraghing Critical!')
                                #Set boolean to track and increase hemo damage (possible multiple crits per round)
                                track_hemo = True                        

                        damage_modifier = calc_damage_modifier(combatant)
                
                        if combatant.use_sharpshooter:
                            damage_modifier = damage_modifier + 10
                            print_output(indent + combatant.name + ' dealt extra damage because of Sharpshooter')

                        if combatant.use_great_weapon_master:
                            damage_modifier = damage_modifier + 10
                            print_output(indent + combatant.name + ' dealt extra damage because of Great Weapon Master')
                
                        totaldamage = dice_damage + damage_modifier             
                        print_output(indent + combatant.name + '\'s strike dealt ' + repr(totaldamage) + ' points of ' + weapon_damage_type.name + ' damage (dice damage: ' + repr(dice_damage) + ' modifier: ' + repr(damage_modifier) + ')')
                        deal_damage(combatant.target,totaldamage,weapon_damage_type,combatant.current_weapon.magic)
                
                        if track_hemo:
                            print_output(indent + combatant.name + ' adds an extra ' + repr(int(totaldamage/2)) + ' damage via Hemorrhaging Critical, which will be dealt at the end of ' + combatant.target.name + '\'s turn.')
                            combatant.target.hemo_damage += int(totaldamage/2)
                            combatant.target.hemo_damage_type = weapon_damage_type
                            track_hemo = False

                        #Bonus damage (from weapon)
                        if combatant.current_weapon.bonus_damage_die > 0:
                            resolve_bonus_damage(combatant,combatant.current_weapon.bonus_damage_target,combatant.current_weapon.bonus_damage_type,combatant.current_weapon.bonus_damage_die,combatant.current_weapon.bonus_damage_die_count,crit,combatant.current_weapon.name)
                    
                        #Bonus damage (from hand of Vecna, 2d8 cold damage on melee hit)
                        for item in combatant.equipment_inventory():
                            if item.grants_equipment_spell == equipment_spells.HandOfVecna and combatant.current_weapon.range == 0:
                                print_output(combatant.name + '\'s left hand crackles with power! They dealt bonus damage with the ' + item.name)
                                resolve_bonus_damage(combatant,0,item.damage_type,item.damage_die,item.damage_die_count,crit,item.name)
                        
                        # Bonus damage (from critical weapon effect)
                        if crit and combatant.current_weapon.crit_bonus_damage_die > 0:
                            print_output(combatant.current_weapon.name + ' surges with power, dealing bonus damage on a critical strike!')                            
                            resolve_bonus_damage(combatant,0,combatant.current_weapon.crit_bonus_damage_type,combatant.current_weapon.crit_bonus_damage_die,combatant.current_weapon.crit_bonus_damage_die_count,crit,combatant.current_weapon.name)                        

                        # Bonus damage (from Improved Divine Smite)
                        if combatant.improved_divine_smite:
                            print_output(combatant.name + '\'s eyes glow, as their attacks are infused with radiant energy!')                                                    
                            resolve_bonus_damage(combatant,0,damage_type.Radiant,8,1,crit,"Improved Divine Smite")
                        #Conditionall cast spells/use items on crit after initial damage resolved
                        #Smite (ideally you would only do this on crit)
                        for spell in combatant.creature_spells():
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
                                        print_output(combatant.name + ' activates ' + eq.name + ', pouring ' +  repr(eq.current_charges) + ' charges into ' + combatant.target.name + '!')
                                        for x in range(0,eq.current_charges):
                                            die_damage = roll_weapon_die(eq.damage_die)                                
                                            equipment_damage += die_damage * 2         
                                            print_output(combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(eq.damage_die) + ' (Cabal\'s Ruin damage)')
                                        eq.current_charges = 0                
                                        print_output(combatant.name + ' dealt an additional ' + repr(equipment_damage) + ' points of ' + equipment_damage_type.name + ' damage with ' + eq.name)
                                        deal_damage(combatant.target,equipment_damage,equipment_damage_type,True)
                
                        #After all the damage from the attack action is resolved, check the fatality
                        #Do this sparingly or players wlil die multiple times from one attack 
                        #i.e. fail death saving throws/activate relentless rage each time they drop below 0
                        resolve_damage(combatant.target)

                        resolve_fatality(combatant.target)
                    else:
                        print_output(combatant.name + '\'s attack on ' + combatant.target.name + ' with ' + combatant.current_weapon.name + ' MISSED! (' + repr(totalatk) + ' versus AC ' + repr(combatant.target.armour_class) + ')')            

                    # consume ammo after shot #
                    if combatant.current_weapon.reload > 0:
                        combatant.current_weapon.currentammo = combatant.current_weapon.currentammo - 1            

                    attackcomplete = True
            else:
                print_output(combatant.target.name + ' is unconscious!')
        else:
            print_output(combatant.target.name + ' is out of range of ' + combatant.current_weapon.name + '!')

#Cast a spell  
def cast_spell(combatant,spell,crit):
    #Check if a spell slot is available to be used
    #Always use highest level spellslot to cast spell (for now...)
    spellslot = check_slot_available(combatant,spell)
    #Don't burn a spell slot that doesn't give a benefit
    if spellslot >= spell.min_spell_slot and spellslot <= spell.max_spell_slot:    
        #Check that components (V,S,M) are available for spell?
        #Evaluate if spell is targetted or self (i.e. buff?)?
        #Check that target is in range of spell
        if spell.range <= getdistance(combatant.position,combatant.target.position):
            #Resolve saving throw
            #if spell.saving_throw:
                #Resolve saving throw to see if damage/condition is applied
            #Consume the spell slot from player's available slots
            print_output(combatant.name + ' is burning a ' + repr(spellslot) + 'th level spell slot to cast ' + spell.name)                            
            print_output(indent + 'Rolling spell damage:')
            consume_spell_slot(combatant,spellslot);
            spell_damage = 0
            if spell.damage_die > 0:
                for x in range(0,spell.damage_die_count):
                    die_damage = roll_weapon_die(spell.damage_die)
                    print_output(doubleindent + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(spell.damage_die) + ' (Spell Damage)')
                    spell_damage += die_damage
                #Add additional damage for levels of expended spell slot
                if spell.min_spell_slot < spellslot:
                    if spellslot > spell.max_spell_slot:
                        # Treat spellslot as the spell's maximum from now on (already marked off)
                        spellslot = spell.max_spell_slot
                    for x in range(spell.min_spell_slot,spellslot):
                        for y in range(0,spell.damage_die_count_per_spell_slot):
                            die_damage = roll_weapon_die(spell.damage_die_per_spell_slot)
                            print_output(doubleindent + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(spell.damage_die_per_spell_slot) + ' (Additional Spell Damage from Spell Slot)')
                            spell_damage += die_damage
                #Add bonus damage
                if combatant.target.race == spell.bonus_damage_target:
                    for x in range(0,spell.bonus_damage_die_count):
                        die_damage = roll_weapon_die(spell.bonus_damage_die)
            
            #Double dice if crit
            if crit:
                spell_damage = spell_damage + 2
            # Add modifier

            print_output(indent + combatant.name + ' cast ' + spell.name + ' and dealt a total of ' + repr(spell_damage) + ' points of ' + spell.damage_type.name + ' damage!')                    
            deal_damage(combatant.target,spell_damage,spell.damage_type,True)
            #Resolve spell damage immediately
            resolve_damage(combatant.target)

def check_slot_available(combatant,spell):
    if spell.min_spell_slot <= 9 and combatant.creature_spellslots.NinthLevel > 0:
        return 9
    if spell.min_spell_slot <= 8 and combatant.creature_spellslots.EigthLevel > 0:
        return 8
    if spell.min_spell_slot <= 7 and combatant.creature_spellslots.SeventhLevel > 0:
        return 7
    if spell.min_spell_slot <= 6 and combatant.creature_spellslots.SixthLevel > 0:
        return 6    
    if spell.min_spell_slot <= 5 and combatant.creature_spellslots.FifthLevel > 0:
        return 5
    if spell.min_spell_slot <= 4 and combatant.creature_spellslots.FourthLevel > 0:
        return 4    
    if spell.min_spell_slot <= 3 and combatant.creature_spellslots.ThirdLevel > 0:
        return 3    
    if spell.min_spell_slot <= 2 and combatant.creature_spellslots.SecondLevel > 0:
        return 2    
    if spell.min_spell_slot == 1 and combatant.creature_spellslots.FirstLevel > 0:
        return 1    
    return 0
  
def consume_spell_slot(combatant,spellslot):
    if spellslot == 1:
       combatant.creature_spellslots.FirstLevel -= 1
    if spellslot == 2:
       combatant.creature_spellslots.SecondLevel -= 1
    if spellslot == 3:
       combatant.creature_spellslots.ThirdLevel -= 1
    if spellslot == 4:
       combatant.creature_spellslots.FourthLevel -= 1
    if spellslot == 5:
       combatant.creature_spellslots.FifthLevel -= 1
    if spellslot == 6:
       combatant.creature_spellslots.SixthLevel -= 1
    if spellslot == 7:
       combatant.creature_spellslots.SeventhLevel -= 1
    if spellslot == 8:
       combatant.creature_spellslots.EigthLevel -= 1
    if spellslot == 9:
       combatant.creature_spellslots.NinthLevel -= 1
    
    
def repair_weapon(combatant):
    print_output(combatant.name + ' attempts to repair ' + combatant.current_weapon.name)    
    if abilitycheck(combatant,ability_check.Dexterity,dexmod(combatant)+combatant.proficiency,False,10+combatant.current_weapon.misfire):  
        print_output(combatant.name + ' successfully repaired ' + combatant.current_weapon.name)
        combatant.current_weapon.broken = False
    else:
        combatant.current_weapon.broken = True
        combatant.current_weapon.ruined = True
        print_output(combatant.current_weapon.name + ' has been ruined in the repair attempt! ' + combatant.name + ' needs to go back to their workshop to fix it! ')

def resolve_bonus_damage(combatant,bonus_target,type,die,count,crit,source):
    bonus_damage = 0
    crit_damage = 0
    if (bonus_target == 0) or (bonus_target == combatant.target.race):
        if bonus_target == 0:
            print_output(indent + 'Rolling bonus damage: ')
        else:
            print_output(indent + 'Rolling bonus damage against ' + combatant.target.race.name + ': ')                    
        for x in range(0,count):
            die_damage = roll_weapon_die(die)
            print_output(doubleindent + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(die) + ' (' + source + ' Bonus Damage)')
            if greatweaponfighting(combatant) and die_damage <= 2 and source == combatant.current_weapon.name:
                print_output(doubleindent + combatant.name + ' rerolled a weapon die due to Great Weapon Fighting!')
                die_damage = roll_weapon_die(die)
                print_output(doubleindent + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(die) + ' (' + source + ' (Bonus Damage)')
            bonus_damage += die_damage
        if crit:
            crit_damage = bonus_damage * 2           
                        
    if crit:
        print_output(indent + combatant.name + ' dealt an additional ' + repr(crit_damage) + ' (roll = ' + repr(bonus_damage) + ') points of ' + type.name + ' damage with ' + source)
        deal_damage(combatant.target,crit_damage,type,combatant.current_weapon.magic)
    else:
        print_output(indent + combatant.name + ' dealt an additional ' + repr(bonus_damage) + ' points of ' + type.name + ' damage with ' + source)
        deal_damage(combatant.target,bonus_damage,type,combatant.current_weapon.magic)

def deal_damage(combatant,damage,dealt_damage_type,magical):    
    #Reduce bludgeoning/piercing/slashing if raging (and not wearing Heavy armour)
    if combatant.raging and not combatant.armour_type == armour_type.Heavy:            
        if dealt_damage_type in (damage_type.Piercing,damage_type.Bludgeoning,damage_type.Slashing):
            damage = int(damage/2)              
            print_output(doubleindent + combatant.name + ' shrugs off ' + repr(damage) + ' points of damage in his rage!')
    if combatant.enlarged:
        if dealt_damage_type in (damage_type.Fire,damage_type.Cold,damage_type.Lightning):
            damage = int(damage/2)              
            print_output(doubleindent + combatant.name + ' shrugs off ' + repr(damage) + ' points of damage due to the effects of Enlarge!')

    #Reduce bludgeoning/piercing/slashing if dealt by non-magical dealt_
    if combatant.creature_subclass == creature_subclass.Ancient_Black_Dragon:            
        if dealt_damage_type in (damage_type.Piercing,damage_type.Bludgeoning,damage_type.Slashing) and not magical:
            damage = int(damage/2)              
            print_output(doubleindent + combatant.name + ' shrugs off ' + repr(damage) + ' points of damage from the non-magical attack!')

    if damage > 0:
        #Check if creature already has a type of this damage pending to be deducted from hit points
        for x in combatant.pending_damage():
            if x.pending_damage_type == dealt_damage_type:
                x.damage += damage
                damage = 0
        #If there is still damage, create a new pending damage object against the creature
        if damage > 0:
            pd = pending_damage()
            pd.pending_damage_type = dealt_damage_type
            pd.damage = damage
            combatant.pending_damage().append(pd)        
        
def resolve_damage(combatant):
    total_damage = 0
    damage_string = ""
    #Calculate total damage
    #Track the damage dealt for output purposes and set the damage for that type back to zero    
    for x in combatant.pending_damage():        
        if x.damage > 0:
            total_damage += x.damage
            damage_string += '\n'
            damage_string += indent + repr(int(x.damage)) + ' points of ' + x.pending_damage_type.name + " damage"
    
    #Empty the list of pending damage
    combatant.pending_damage().clear()
    if total_damage > 0:
        
        #Use Reaction if it can do anything
        if not combatant.reaction_used:
            if combatant.stones_endurance:
                if not combatant.stones_endurance_used:
                    #Don't waste stones endurance on small hits
                    if total_damage > conmod(combatant)+12:
                        reduction = conmod(combatant) + roll_weapon_die(12)
                        total_damage = int(total_damage - reduction)
                        print_output(combatant.name + ' uses their reaction, and uses Stones Endurance to reduce the damage by ' + repr(reduction) + '! ')
                        damage_string += 'reduced by ' + repr(int(reduction)) + ' (Stones Endurance)'
                        combatant.stones_endurance_used = True
                        combatant.reaction_used = True

        combatant.current_health = combatant.current_health - total_damage 
                        
        print_output('Damage Summary: ' + damage_string)        
        print_output(combatant.name + ' suffers a total of ' + repr(int(total_damage)) + ' points of damage. Current HP: ' + repr(int(combatant.current_health)) + '/' + repr(combatant.max_health))

def resolve_fatality(combatant):
    if combatant.current_health <= 0:
        #Relentless rage
        if combatant.relentless_rage:
            if savingthrow(combatant,saving_throw.Consitution,combatant.saves.con,False,combatant.relentless_rage_DC):
                print_output(combatant.name + ' was dropped below 0 hit points, but recovers to 1 hit point due to his Relentless Rage!')
                combatant.alive = True
                combatant.current_health = 1
                combatant.relentless_rage_DC += 5
            else:                
                print_output('The relentless fury within ' + combatant.name + '\'s eyes fades, and he slumps to the ground, unconscious.')
                combatant.alive = False      
                combatant.relentless_rage = False
        else:            
            combatant.alive = False                    
    if not combatant.alive:
        print_output('HOW DO YOU WANT TO DO THIS??')        

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
        if combatant.current_weapon.weapon_type != 0:
            if combatant.current_weapon.weapon_type == combatant_weapon_proficiency:
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

def roll_d20(): 
    random.seed
    return random.randint(1,20)

def roll_weapon_die(weapon_die):
    random.seed
    return random.randint(1,weapon_die)

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
    roll = roll_d20()
    savingthrow = roll + modifier
    #print_output(savetype + ' save: Natural roll: ' + repr(roll) + ', modifier: ' + repr(modifier))
    if savingthrow >= DC:
        print_output(combatant.name + ' made a ' + savetype.name + ' save against a DC of ' + repr(DC) + ' with a saving throw of ' + repr(savingthrow))
        return True
    if adv:
        #print_output(combatant.name + ' failed the save, but has advantage on ' + savetype + ' saving throws!')
        roll = roll_d20()
        savingthrow = roll + modifier
        #print_output(savetype + ' save: Natural roll: ' + repr(roll) + ', modifier: ' + repr(modifier))        
        if savingthrow >= DC:
            print_output(combatant.name + ' made a ' + savetype.name + ' save against a DC of ' + repr(DC) + ' with a saving throw of ' + repr(savingthrow))
            return True
    print_output(combatant.name + ' failed the ' + savetype.name + ' save with a saving throw of ' + repr(savingthrow) + ' versus DC ' + repr(DC))
    return False

# check functions #
def abilitycheck(combatant,checktype,modifier,adv,DC):
    roll = roll_d20()
    check = roll + modifier
    if DC == 0:
        return(check)

    #print_output(checktype + ' check: Natural roll: ' + repr(roll) + ', modifier: ' + repr(modifier))    
    if check >= DC:
        print_output(combatant.name + ' succeeded on a DC ' + repr(DC) + ' ' + checktype.name + ' check with a total of ' + repr(check))
        return True
    if adv:
        #print_output(combatant.name + ' failed the check, but has advantage on ' + checktype + ' checks!')
        roll = roll_d20()
        check = roll + modifier
        #print_output(checktype + ' check: Natural roll: ' + repr(roll) + ', modifier: ' + repr(modifier))    
        if check >= DC:
            print_output(combatant.name + ' succeeded on a DC ' + repr(DC) + ' ' + checktype.name + ' check with a total of ' + repr(check))
            return True
    print_output(combatant.name + ' FAILED on a DC ' + repr(DC) + ' ' + checktype.name + ' check with a total of ' + repr(check))
    return False

# Initiative
def roll_initiative(combatant):
    initiativeroll = abilitycheck(combatant,saving_throw.Dexterity,dexmod(combatant),False,0)            
    if combatant.feral_instinct:
        initiativeroll_adv = abilitycheck(combatant,saving_throw.Dexterity,dexmod(combatant),True,0)
        initiativeroll = max(initiativeroll,initiativeroll_adv)
    if combatant.quickdraw:
        initiativeroll += combatant.proficiency
    combatant.initiative_roll = initiativeroll

# helper functions #

def greatweaponfighting(combatant):
    if combatant.fighting_style == fighting_style.Great_Weapon_Fighting and (combatant.current_weapon.two_handed or combatant.current_weapon.versatile):
        return True
    return False

def characterlevel(combatant):
    return(combatant.barbarian_level + 
           combatant.fighter_level + 
           combatant.rogue_level + 
           combatant.ranger_level +
           combatant.paladin_level)

def getdistance(combatantpos,targetpos):
    return int(math.fabs(combatantpos-targetpos))

