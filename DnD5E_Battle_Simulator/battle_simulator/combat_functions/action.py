#Explicit imports
from battle_simulator import combatants
from battle_simulator import classes
from battle_simulator import print_functions
from battle_simulator.combat_functions.combat import *
from battle_simulator.combat_functions.spells import *
from battle_simulator.combat_functions.damage import * 
from battle_simulator.combat_functions.inventory import *
from battle_simulator.combat_functions.position import *
from battle_simulator.combat_functions.target import *
            
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

        # Cast a Spell
        if not combatant.action_used:
            # See if we have any action-cost spells to use
            if combatant.spellcaster:
                # Select an appropriate action-cost spell
                selected_spell = select_spell(combatant,spell_casting_time.Action)                
                if selected_spell != None:                    
                    cast_spell(combatant,selected_spell)
                    combatant.action_used = True

        # If we get to this point, use our default attack if available
        if not combatant.action_used:
            # Swap to a different weapon if it makes sense due to range                    
            current_range = calc_distance(combatant,combatant.target)
            # Attempt a weapon swap - change weapons depending on range
            # This will prefer to swap a non-broken or ruined weapon in
            weapon_swap(combatant,current_range)

            if combatant.main_hand_weapon.broken == False:
                if target_in_weapon_range(combatant,combatant.target,combatant.main_hand_weapon.range):
                    attack_action(combatant)                        
                else:
                    # Check the upper range increment (if the weapon has one) instead and potentially fire at disadvantage
                    if target_in_weapon_range(combatant,combatant.target,combatant.main_hand_weapon.long_range):
                        attack_action(combatant)                        
                    else:
                        # Dash Action
                        print_output(combatant.name + ' is taking the Dash action!')
                        combatant.movement = combatant.speed
                        if combatant.hasted:
                            combatant.movement = combatant.speed * 2                                                
                        use_movement(combatant)
                        combatant.action_used = True
            else:
                # If the weapon is Ruined, and we could not swap to a non-ruined weapon, we're out of luck
                if combatant.main_hand_weapon.ruined:
                    print_output(combatant.name + ' can\'t do anything with ' + combatant.main_hand_weapon.name + ', it is damaged beyond repair!')
                    # Can't swap to a valid weapon - just have to sit this one out
                    combatant.action_used = True

                # If the weapon is broken, and we could not swap to a non-broken weapon, must waste action reparing it
                if not combatant.action_used:
                    if combatant.main_hand_weapon.broken:
                        repair_weapon(combatant)            
                        combatant.action_used = True
                
                #If we have not attacked yet, attempt to attack
                if not combatant.action_used:
                    attack_action(combatant)
                    combatant.action_used = True

    combatant.action_used = True

def bonus_action(combatant): 
    print_output('<b>Bonus Action:</b>') 
    #Only do something if a target exists
    if combatant.target:

        if combatant.bonus_action_used:
            print_output(combatant.name + ' has already used their Bonus Action this turn.')
                
        # Barbarian bonus actions
        #Rage
        if not combatant.bonus_action_used:
            if combatant.canrage and not combatant.raging:
                print_output(combatant.name + ' uses their Bonus Action to go into a mindless rage! "I would like to RAAAGE!!!"')
                print_output(indent() + '(' + combatant.name + ' gains Resistance to Bludgeoning/Piercing/Slashing damage, Advantage on Strength Saving Throws and Ability Checks, and +' + repr(combatant.rage_damage) + ' to damage with melee attacks.)')
                combatant.raging = True;
                # Reset duration of this rage
                combatant.rage_duration = 0
                combatant.bonus_action_used = True
                # Rage grants advantage on strength checks/saving throws for its duration
                if combatant.armour_type != armour_type.Heavy:
                    combatant.saves.str_adv = True
                    combatant.checks.str_adv = True

        #Frenzy
        if not combatant.bonus_action_used:
            if combatant.raging:
                if combatant.frenzy:      
                    #You can make a single melee weapon Attack as a Bonus Action on each of your turns after this one (does not have to be tied to Attack action)
                    if target_in_weapon_range(combatant,combatant.target,combatant.main_hand_weapon.range):                    
                        print_output(combatant.name + ' uses their Bonus Action to make a frenzied weapon attack against ' + combatant.target.name)
                        attack(combatant,combatant.main_hand_weapon)            
                        combatant.bonus_action_used = True
                        
        # Blood Hunter bonus actions
        if not combatant.bonus_action_used:
            if combatant.crimson_rite:
                # Check current HP
                if combatant.current_health >= characterlevel(combatant):                    
                    # Check if our main hand weapon has a rite active
                    if combatant.main_hand_weapon.active_crimson_rite == None:
                        # Select the correct rite - this will need some sort of target analysis to choose rites based on potential weaknesses                        
                        rite = select_crimson_rite(combatant)
                        activate_crimson_rite(combatant,combatant.main_hand_weapon,rite)
                        
                    # Check if our offhand weapon has a rite active
                    if combatant.offhand_weapon != None and combatant.offhand_weapon != combatant.main_hand_weapon:
                        if combatant.offhand_weapon.active_crimson_rite == None:
                            rite = select_crimson_rite(combatant)
                            activate_crimson_rite(combatant,combatant.offhand_weapon,rite)                        

        # Fighter bonus actions
        #Second Wind
        if not combatant.bonus_action_used:
            if combatant.second_wind:
                #Don't use Second Wind unless current HP is more than 10+fighter level less than max
                fighter_level = get_combatant_class_level(combatant,player_class.Fighter)                
                if combatant.current_health + 10 + fighter_level < combatant.max_health:
                    second_wind_heal = roll_die(10) + fighter_level
                    heal_damage(combatant,second_wind_heal)                    
                    print_output(combatant.name + ' uses their Bonus Action to gain a Second Wind, and restores ' + healing_text(repr(second_wind_heal)) + ' hit points! ' + hp_text(combatant.current_health,combatant.max_health))
                    combatant.second_wind = False
                    combatant.bonus_action_used = True

        #Lightning Reload
        if not combatant.bonus_action_used:
            if combatant.main_hand_weapon.weapon_type == weapon_type.Firearm:
                if combatant.lighting_reload:
                    if combatant.main_hand_weapon.currentammo == 0:
                        combatant.main_hand_weapon.currentammo = combatant.main_hand_weapon.reload
                        print_output(combatant.name + ' used a bonus action to reload. ' + combatant.main_hand_weapon.name + ' Ammo: ' + repr(combatant.main_hand_weapon.currentammo) + '/' + repr(combatant.main_hand_weapon.reload))
                        combatant.bonus_action_used = True

        # Monk bonus actions

        # Paladin bonus actions
        #Vow of Enmity
        if not combatant.bonus_action_used:
            if combatant.channel_divinity and combatant.vow_of_enmity:
                combatant.vow_of_enmity_target = combatant.target
                print_output(combatant.name + ' swears a Vow of Enmity against ' + combatant.target.name)
                combatant.channel_divinity = False
                combatant.bonus_action_used = True

        # Rogue bonus actions
        #Cunning Action
        if not combatant.bonus_action_used:
            if combatant.cunning_action:
                #Disengage if we're using ranged weapons and someone is in melee range
                if enemy_in_melee_range(combatant,None) and combatant.main_hand_weapon.range > 0:                                     
                    print_output(combatant.name + ' is using their Cunning Action, and taking the Disengage bonus action!')
                    combatant.disengaged = True
                    combatant.bonus_action_used = True

                #Dash if we've used our Action to increase the gap                 
                if not combatant.bonus_action_used and combatant.action_used:                    
                    print_output(combatant.name + ' is using their Cunning Action, and taking the Dash bonus action!')
                    combatant.movement = combatant.speed
                    if combatant.hasted:
                        combatant.movement = combatant.speed * 2                                                
                    use_movement(combatant)
                    combatant.bonus_action_used = True

                #Dodge         

                #Hide

        # Equipment bonus actions
        #Boots of Feral Leaping        
        if not combatant.bonus_action_used:
            for item in combatant.equipment_inventory():
                if item.grants_equipment_spell == equipment_spells.Leap:
                    #For now treat this as special forced combatant.movement of 20 feet
                    print_output(combatant.name + ' is taking a flying leap using their ' + item.name + ' as a Bonus Action!')                    
                    if abilitycheck(combatant,ability_check.Strength,strmod(combatant),combatant.checks.str_adv,16):                    
                        print_output(combatant.name + ' leaps 20 feet.')                        
                        combatant.movement = 20
                        use_movement(combatant)                            
                    else:
                        print_output(combatant.name + ' fell over where they stand!')
                        combatant.prone = True
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

        if target_in_weapon_range(combatant,combatant.target,combatant.main_hand_weapon.range):
            attack(combatant,combatant.main_hand_weapon)
            combatant.hasted_action_used = True
        else:
            print_output(combatant.name + ' uses the Dash action as a Hasted action!')                        
            combatant.movement = combatant.speed * 2                        
            use_movement(combatant)
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
    
def repair_weapon(combatant):
    print_output(combatant.name + ' attempts to repair ' + combatant.main_hand_weapon.name)    
    if abilitycheck(combatant,ability_check.Dexterity,dexmod(combatant)+combatant.proficiency,False,10+combatant.main_hand_weapon.misfire):  
        print_output(combatant.name + ' successfully repaired ' + combatant.main_hand_weapon.name)
        combatant.main_hand_weapon.broken = False
    else:
        combatant.main_hand_weapon.broken = True
        combatant.main_hand_weapon.ruined = True
        print_output(combatant.main_hand_weapon.name + ' has been ruined in the repair attempt! ' + combatant.name + ' needs to go back to their workshop to fix it! ')

def select_crimson_rite(combatant):
    selected_rite = None
    for rite in combatant.crimson_rites():
        if rite.name == "Rite of the Dawn":
            selected_rite = rite
    return(selected_rite)

def activate_crimson_rite(combatant,weapon,rite):
    if not combatant.bonus_action_used:
        print_output(combatant.name + ' drags the blade of their ' + weapon.name + ' across their skin, and ' + rite.colour + ' light engulfs it as the Crimson ' + rite.name + ' is activated!')
        deal_damage(combatant,combatant,rite.activation_damage,damage_type.Generic,False)
        resolve_damage(combatant)                            
        weapon.active_crimson_rite = rite
        combatant.bonus_action_used = True