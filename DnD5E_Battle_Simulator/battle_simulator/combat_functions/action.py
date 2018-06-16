#Explicit imports
from battle_simulator import combatants

#Implicit imports
from battle_simulator.classes import *
from battle_simulator.print_functions import *
from battle_simulator.combat_functions.combat import *
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
                    breath_attack(combatant,combatant.main_hand_weapon)
                    combatant.action_used = True

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
                print_output(combatant.name + ' gains Resistance to Bludgeoning/Piercing/Slashing damage, Advantage on Strength Saving Throws and Ability Checks, and +' + repr(combatant.rage_damage) + ' to damage with melee attacks.)')
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
                # Check if our main hand weapon has a rite active
                if combatant.main_hand_weapon.active_crimson_rite == None:
                    # Check current HP
                    if combatant.current_health >= characterlevel(combatant):
                        # Select the correct rite - this will need some sort of target analysis to choose rites based on potential weaknesses
                        # For now, just forcing to Dawn for Molly
                        rite = select_crimson_rite(combatant)
                        activate_crimson_rite(combatant,combatant.main_hand_weapon,rite)
                        
                        # Check if our offhand weapon has a rite active
                        if combatant.offhand_weapon != None and combatant.offhand_weapon != combatant.main_hand_weapon and combatant.offhand_weapon.active_crimson_rite == None:
                            # Check current HP
                            if combatant.current_health >= characterlevel(combatant):
                                rite = select_crimson_rite(combatant)
                                activate_crimson_rite(combatant,combatant.offhand_weapon,rite)
                                # Select the correct rite - this will need some sort of target analysis to choose rites based on potential weaknesses
                                # For now, just forcing to Dawn for Molly

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
    print_output(combatant.name + ' drags the blade of their ' + weapon.name + ' across their skin, and ' + rite.colour + ' light engulfs it as the Crimson ' + rite.name + ' is activated!')
    deal_damage(combatant,combatant,rite.activation_damage,damage_type.Generic,False)
    resolve_damage(combatant)                            
    weapon.active_crimson_rite = rite

def use_luck(combatant):
    if combatant.luck_uses > 0:        
        random.seed
        luck_die_roll = random.randint(1,20)        
        combatant.luck_uses -= 1
        print_output(indent() + combatant.name + ' used a point of Luck, and rolled a ' + repr(luck_die_roll) + ' on the lucky d20!')
        return(luck_die_roll)        

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