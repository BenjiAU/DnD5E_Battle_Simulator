#Explicit imports
from battle_simulator import combatants

#Implicit imports
from battle_simulator.classes import *
from battle_simulator.print_functions import *
from battle_simulator.combat_functions.position import *
from battle_simulator.combat_functions.damage import *
from battle_simulator.combat_functions.generics import *
from battle_simulator.combat_functions.conditions import *
from battle_simulator.combat_functions.spells import cast_spell
from battle_simulator.combat_functions.inventory import weapon_swap
from battle_simulator.combat_functions.target import find_target,calculate_area_effect

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
                        if target_in_range(combatant,combatant.target,weapon.range) and ma == weapon.name:                        
                            multiattack_weapons.append(weapon)

                if len(multiattack_weapons) > 0:
                    print_output(combatant.name + ' unleashes a Multiattack!')                
                    for weapon in multiattack_weapons:                                                                            
                        #Repeat the Find Target call after each attack in a multiattack (to avoid instantly killing unconscious players)
                        if not find_target(combatant):
                            print_output('No targets remain!')
                            return
                        attack(combatant,weapon)
                        if check_condition(combatant,condition.Slowed):
                            print_output(combatant.name + ' is Slowed, and cannot take their next Multiattack')
                            return                
                else:
                    #Revert to normal attack/swap to range or reach weapon if required
                    print_output(combatant.name + ' uses the Attack action')                
                    attack(combatant,combatant.main_hand_weapon)    
            else:
                print_output(combatant.name + ' uses the Attack action')                
                attack(combatant,combatant.main_hand_weapon)    
    elif combatant.creature_type == creature_type.Player:
        # Primary attack call for players
        print_output(combatant.name + ' uses the Attack action')        
        attack(combatant,combatant.main_hand_weapon)
        
        # Bonus attack functions for players
        # Bonus Action offhand attack
        # Rules: both weapons must be Light, weapons must be different, off hand weapon must be equipped
        if not combatant.bonus_action_used and enemy_in_melee_range(combatant,None) and combatant.offhand_weapon != None and combatant.main_hand_weapon != combatant.offhand_weapon and combatant.main_hand_weapon.light and combatant.offhand_weapon.light:
            print_output(combatant.name + ' uses their Bonus Action to make an offhand strike!')            
            #Repeat find_target call to see if we offhand strike someone else
            if not find_target(combatant):
                print_output('No targets remain!')
                return
            attack(combatant,combatant.offhand_weapon)
            combatant.bonus_action_used = True
                
        # Flurry of Blows
        if not combatant.bonus_action_used and combatant.flurry_of_blows and enemy_in_melee_range(combatant,None):                      
            if combatant.main_hand_weapon.weapon_type == weapon_type.Unarmed or combatant.main_hand_weapon.monk_weapon:
                if combatant.ki_points > 0:
                    combatant.ki_points -= 1
                    print_output(combatant.name + ' spends 1 Ki Point and unleashes a Flurry of Blows! Current Ki Points: ' + repr(combatant.ki_points) + '/' + repr(combatant.max_ki_points))                    
                    orig_weapon = combatant.main_hand_weapon
                    combatant.main_hand_weapon = unarmed_strike(combatant)
                    #Repeat find_target call to see if we should punch someone else
                    if not find_target(combatant):
                        print_output('No targets remain!')
                        return
                    attack(combatant,combatant.main_hand_weapon)
                    #Repeat find_target call to see if we should punch someone else
                    if not find_target(combatant):
                        print_output('No targets remain!')
                        return
                    attack(combatant,combatant.main_hand_weapon)
                    combatant.main_hand_weapon = orig_weapon
                    combatant.bonus_action_used = True
                else:
                    print_output(combatant.name + ' has no Ki Points remaining, and cannot use Flurry of Blows!')

        # Bonus Action unarmed strike
        if not combatant.bonus_action_used and enemy_in_melee_range(combatant,None):                      
            if combatant.main_hand_weapon.weapon_type == weapon_type.Unarmed or combatant.main_hand_weapon.monk_weapon:
                print_output(combatant.name + ' uses their Bonus Action to make an unarmed strike!')                                        
                orig_weapon = combatant.main_hand_weapon
                combatant.main_hand_weapon = unarmed_strike(combatant)
                #Repeat find_target call to see if we should punch someone else
                if not find_target(combatant):
                    print_output('No targets remain!')
                    return
                attack(combatant,combatant.main_hand_weapon)
                combatant.main_hand_weapon = orig_weapon
                combatant.bonus_action_used = True

        if combatant.extra_attack > 0:
            if check_condition(combatant,condition.Slowed):
                print_output(combatant.name + ' is Slowed, and cannot take an Extra Attack')
                return

            for x in range(0,combatant.extra_attack):
                #Can't attack if weapon is broken, must spend next action to fix it
                if not combatant.main_hand_weapon.broken:
                    print_output('<i>' + combatant.name + ' uses an Extra Attack.</i>')
                    #Repeat find_target call to see if we should punch someone else
                    if not find_target(combatant):
                        print_output('No targets remain!')
                        return
                    attack(combatant,combatant.main_hand_weapon)  
    else:
        print_error(combatant.name + ' does not have a Creature Type defined. Unable to determine attack action.')

def unarmed_strike(combatant):    
    # Create and equip a phantom 'unarmed strike' weapon to proceed with attack calculations
    unarmed_strike = weapon()
    unarmed_strike.name = "Unarmed Strike"
    unarmed_strike.weapon_type = weapon_type.Unarmed
    unarmed_strike.monk_weapon = True    
    unarmed_strike.weapon_damage_type = damage_type.Bludgeoning
    if combatant.martial_arts:
        unarmed_strike.damage_die = combatant.martial_arts_die
        unarmed_strike.damage_die_count = 1
    if combatant.ki_empowered_strikes:
        unarmed_strike.magic = True
    return unarmed_strike

def breath_attack(combatant):
    print_output(combatant.name + ' rears back and unleashes a devastating breath attack! (10 feet width, 90 feet length)')       

    # Black dragon breath attack is a 10 ft wide 90 ft line (all dragons are different)
    affected_targets = []
        
    affected_targets = calculate_area_effect(combatant,combatant.xpos,combatant.ypos,combatant.target.xpos,combatant.target.ypos,area_of_effect_shape.Line,10,90,True)   

    # Calculate damage
    breath_damage = 0
    breath_damage_type = 0
    die_damage = 0
    if combatant.monster_type == monster_type.Ancient_Black_Dragon:
        breath_damage_type = damage_type.Acid
        i = 1
        for i in range(1,15):
            die_damage = roll_die(combatant.breath_damage_die)
            print_indent( combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.breath_damage_die) + ' (Breath Damage)')
            breath_damage += die_damage
            
    print_indent( 'The breath attack deals a total of ' + damage_text(repr(breath_damage)) + ' points of ' + breath_damage_type.name + ' damage!')   

    # Retrieve the combatant list reference if it hasn't passed throuhg?
    for affected_target in affected_targets:    
        print_output(affected_target.name + ' is in the affected area (located at (' + repr(affected_target.xpos) + ',' + repr(affected_target.ypos) + ')')   
        if savingthrow(affected_target,saving_throw.Dexterity,23):
            #If target has evasion and saves, nothing happens
            if affected_target.evasion:
                print_output(affected_target.name + ' avoids all damage from the attack thanks to Evasion!') 
            else:                
                deal_damage(combatant,affected_target,breath_damage/2,breath_damage_type,True,False)
                #statistics, count this as a hit attack
                combatant.attacks_hit += 1
        else:
            #statistics, count this as a hit attack
            combatant.attacks_hit += 1
            #If target has evasion and fails, half damage
            if affected_target.evasion:
                print_output(affected_target.name + ' halves the damage of the attack thanks to Evasion!') 
                deal_damage(combatant,affected_target,breath_damage/2,breath_damage_type,True,False)
            else:
                deal_damage(combatant,affected_target,breath_damage,breath_damage_type,True,False)
                    
        #See if the damage droped target below 0 hp
        resolve_damage(affected_target)
        resolve_fatality(affected_target)

    combatant.breath_attack = False

def breath_recharge(combatant):    
    die = roll_die(6)
    if die >= 5:
        print_output(combatant.name + ' rolled a ' + repr(die) + ' on a d6 and recharged their Breath Attack!')
        combatant.breath_attack = True
    else:
        print_output(combatant.name + ' rolled a ' + repr(die) + ' on a d6 and did not recharge their Breath Attack.')

#Make an attack
def attack(combatant,weapon):    
    attack_hit = False
    in_range = False
    in_long_range = False        
    #Only attack with a weapon
    # Unarmed strikes or improvised weapons must create a phantom weapon object to use this function

    if weapon.name != "":        
        if target_in_range(combatant,combatant.target,weapon.range):
            in_range = True
        elif target_in_range(combatant,combatant.target,weapon.long_range):
            in_long_range = True            

        # only resolve attack if target is within one of the range increments
        if in_range or in_long_range:
            # only resolve attack if target is alive
            if combatant.target.alive:
                # Only continue with attack steps if we don't break out because of something else interfering
                # i.e. weapon breaking, reloading
                attackcomplete = False    
                range_attack = False
                while not attackcomplete:
                
                    trick_shot = False
                    trick_shot_target = ""
                    advantage = False
                    disadvantage = False
        
                    combatant.use_sharpshooter = False
                    # Recalculate all +hit modifiers (based on main hand weapon, fighting style, ability modifiers etc.)
                    to_hit_modifier = calc_to_hit_modifier(combatant,weapon)

                    # Before-roll weapon features                    

                    # Determine if attack is ranged or not                    
                    # Decide whether to throw or stab with weapon
                    if weapon.thrown and calc_distance(combatant,combatant.target) > melee_range():
                        print_output(combatant.name + ' throws ' + weapon.name + ' at ' + combatant.target.name + '!')
                        range_attack = True
                        weapon.was_thrown = True                   
                        
                    if weapon.weapon_type == weapon_type.Crossbow:
                        range_attack = True

                    if weapon.weapon_type == weapon_type.Longbow:
                        range_attack = True

                    if weapon.weapon_type == weapon_type.Firearm:
                        # Check that the Firearm is not ruined - if it is ruined, no attacks can be made
                        if not attackcomplete:
                            if weapon.broken and weapon.ruined:
                                print_output(combatant.name + ' can\'t do anything with ' + weapon.name + ', it is damaged beyond repair!')
                                attackcomplete = True
            
                        if not attackcomplete:
                            range_attack = True
                            if weapon.currentammo == 0:
                                # reload weapon # 
                                if combatant.bonus_action_used:
                                    weapon.currentammo = weapon.reload                                    
                                    print_output(combatant.name + ' used their attack to reload ' + weapon.name + '. Ammo: ' + repr(weapon.currentammo) + '/' + repr(weapon.reload))
                                    attackcomplete = True
                                else:
                                    #Use Lightning Reflexes to bonus action reload
                                    weapon.currentammo = weapon.reload                                    
                                    print_output(combatant.name + ' used their Bonus Action to reload ' + weapon.name + '. Ammo: ' + repr(weapon.currentammo) + '/' + repr(weapon.reload))
                                    combatant.bonus_action_used = True                                        

                    #Advantage/disadvantage conditions (not weapon specific)                
                    if not attackcomplete:

                        advantage,disadvantage = determine_advantage(combatant,range_attack)                        
                    
                        #Modifier conditions (i.e. GWM, sharpshooter)       
                        if range_attack:                            
                            if combatant.sharpshooter:                            
                                if in_long_range:
                                    print_output(combatant.name + ' fires at long range with no penalty thanks to Sharpshooter!')
                                if (combatant.target.armour_class < to_hit_modifier+5) and not disadvantage:
                                    print_output(combatant.name + ' uses the Sharpshooter feat, taking a -5 penalty to the attack')
                                    combatant.use_sharpshooter = True           
                                else:
                                    combatant.use_sharpshooter = False
                            else:
                                if in_long_range:
                                    print_output(combatant.name + ' fires at long range with disadvantage!')
                                    disadvantage = True

                        #Great Weapon Master
                        if weapon.heavy and combatant.great_weapon_master:
                            if (combatant.target.armour_class < to_hit_modifier+5) and not disadvantage:
                                print_output(combatant.name + ' uses Great Weapon Master, taking a -5 penalty to the attack')
                                combatant.use_great_weapon_master = True           

                        # Other weapon pre-attack features                    
                        if weapon.weapon_type == weapon_type.Firearm and not attackcomplete:                            
                            # Check to spend grit for trick shot if available #
                            # Only trick shot if we don't have disadvantage
                            # Trick Shot (including Deadeye Shot) (Gunslinger)
                            if combatant.current_grit > 0 and not disadvantage:          
                                grit_selector = roll_die(6)                                                

                                print_output(combatant.name + ' is deciding whether to spend a Grit point...')
                                curr_grit = combatant.current_grit
                                if grit_selector <= 2:
                                    # Head Shot #
                                    # Don't bother if they already have disadvantage/were head-shotted
                                    if not combatant.target.has_disadvantage or combatant.target.head_shotted:                                    
                                        combatant.current_grit -= 1
                                        print_output(combatant.name + ' spends 1 Grit Point to perform a Head Trick Shot. Current Grit: ' + repr(combatant.current_grit))                                        
                                        trick_shot_target = "Head"
                                        trick_shot = True

                                elif grit_selector <= 4:
                                    # Leg Shot #
                                    # Don't bother if target is already prone:
                                    if not check_condition(combatant.target,condition.Prone):
                                        # Only leg shot melee attackers
                                        if combatant.target.main_hand_weapon != None:
                                            if combatant.target.main_hand_weapon.range == 0:
                                                combatant.current_grit -= 1
                                                print_output(combatant.name + ' spends 1 Grit Point to perform a Leg Trick Shot. Current Grit: ' + repr(combatant.current_grit))                                            
                                                trick_shot_target = "Legs"
                                                trick_shot = True

                                elif grit_selector <= 6:
                                    # Deadeye Shot (Gunslinger)
                                    if not advantage:
                                        #Spend grit to gain advantage. Do nothing if we have advantage.
                                        combatant.current_grit -= 1
                                        print_output(combatant.name + ' spends 1 Grit Point to perform a Deadeye Shot. They gain advantage on the next attack! Current Grit: ' + repr(combatant.current_grit))                                        
                                        advantage = True              

                                if curr_grit == combatant.current_grit:
                                    print_output(combatant.name + ' decides to forego spending a Grit point on this attack.')

                    # Make attack roll #                     
                    if not attackcomplete:                        
                        atkroll = attack_roll(combatant,advantage,disadvantage,to_hit_modifier)
                        
                        #Decide if we need to use luck to reroll
                        #If the attack misses, see if we can hit with Luck
                        if combatant.luck_uses > 0 and (atkroll + to_hit_modifier < combatant.target.armour_class):
                            luck_roll = use_luck(combatant)
                            if luck_roll > atkroll:                                
                                atkroll = luck_roll          

                        #Track critical 
                        crit = False
                        if atkroll >= calc_min_crit(combatant,weapon):
                            crit = True
                            print_output('************************')
                            print_output('It\'s a CRITICAL ROLE!!!')
                            print_output('************************')

                        # After-roll weapon features
                        if weapon.weapon_type == weapon_type.Firearm:
                            if weapon.misfire >= atkroll:
                                # weapon misfire, attack fail #
                                print_output(combatant.name + 's attack misfired with a natural ' + repr(atkroll) + '! ' + weapon.name + ' is now ' + damage_text('broken!'))
                                weapon.broken = True
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
                
                        totalAC = calc_total_AC(combatant.target)

                        if totalatk >= totalAC:
                            # Allow target to use reaction if attack would hit them
                            if can_use_reaction(combatant.target):
                                # Cast a reaction spell? (i.e. Shield)
                                selected_spell = select_spell(combatant.target,spell_casting_time.Reaction)                
                                if selected_spell != None:                    
                                    # Check if the Shield will work, or not
                                    if selected_spell.condition == condition.Shielded:
                                        if totalAC + 5 > totalatk:
                                            print_output('<b>Reaction:</b>')
                                            print_indent(combatant.target.name + ' uses the Cast a Spell Reaction to cast ' + selected_spell.name + '!')
                                            cast_spell(combatant.target,selected_spell)
                                            combatant.target.reaction_used = True
                                            print_indent(combatant.target.name + ' has spent their reaction to cast ' + selected_spell.name + '!')
                                            totalAC = calc_total_AC(combatant.target)

                        if totalatk >= totalAC:
                            attack_hit = True
                            #Update statistics
                            combatant.attacks_hit += 1

                            if feat_penalty == 0:
                                print_output(combatant.name + '\'s attack (' + repr(totalatk) + ') against '+ combatant.target.name + ' (AC ' + repr(totalAC) + ') with ' + weapon.name + ' HIT!!!')
                            else:
                                print_output(combatant.name + '\'s attack (' + repr(atkroll + to_hit_modifier) + '-' + repr(feat_penalty) + ') against '+ combatant.target.name + ' (AC ' + repr(totalAC) + ') with ' + weapon.name + ' HIT!!!')
                            if check_condition(combatant.target,condition.Unconscious) and not crit and weapon.range == 0:
                                print_output('The blow strikes the unconscious form of ' + combatant.target.name + ' and deals CRITICAL DAMAGE!')
                                crit = True       
                            
                            # resolve trick shot #
                            if trick_shot:
                                if trick_shot_target == "Head":
                                    if savingthrow(combatant.target,saving_throw.Constitution,8+combatant.proficiency + dexmod(combatant)):
                                        print_double_indent( combatant.target.name + ' succeeded on the Head Shot save, and is immune to its effect.')
                                    else:
                                        print_double_indent( combatant.target.name + ' FAILED the Head Shot save - they now had disadvantage on attacks until the end of their next turn!')
                                        inflict_condition(combatant.target,combatant,condition.Headshot,1)                                        
                                elif trick_shot_target == "Legs":
                                    # logic to choose the right kind of called shot? lol #
                                    if savingthrow(combatant.target,saving_throw.Strength,8+combatant.proficiency + dexmod(combatant)):
                                        print_double_indent( combatant.target.name + ' succeeded on the Leg Shot save, and remains standing')
                                    else:
                                        print_double_indent( combatant.target.name + ' FAILED the Leg Shot save - they are now prone!')
                                        inflict_condition(combatant.target,combatant,condition.Prone)
                                         
                            # Calculate damage modifier (adds strmod/dexmod to attack)
                            damage_modifier = calc_damage_modifier(combatant,weapon)
                            
                            # Calculate main attack dice
                            print_indent( 'The blow from ' + weapon.name + ' strikes true (' + repr(weapon.damage_die_count) + 'd' + repr(weapon.damage_die) + ' + ' + repr(damage_modifier) + ' '  + weapon.weapon_damage_type.name + ' damage)!')
                            weapon_damage_type = damage_type(weapon.weapon_damage_type)
                            for x in range(0,weapon.damage_die_count):                                    
                                die_damage = roll_die(weapon.damage_die)   
                                print_double_indent( combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(weapon.damage_die) + ' (Weapon Damage)')
                                #Great Weapon Fighting (reroll 1s and 2s)                                                
                                if greatweaponfighting(combatant) and die_damage <= 2:
                                    print_double_indent( combatant.name + ' rerolled a weapon die due to Great Weapon Fighting!')
                                    die_damage = roll_die(weapon.damage_die)   
                                    print_double_indent( combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(weapon.damage_die) + ' (Weapon Damage)')    
                                dice_damage += die_damage                    
                            
                            # Special rule for unarmed strike; if no damage has been calculated, we aren't a monk, so force the damage to be 1 + strmod
                            if dice_damage == 0 and weapon.weapon_type == weapon_type.Unarmed:
                                dice_damage = 1 + strmod(combatant)

                            # Sneak attack (if we had advantage on the strike)
                            if combatant.sneak_attack:
                                # Check if we have snuck attack this turn
                                if not combatant.sneak_attack_used:
                                    # Ensure weapon is appropriate for sneak attack
                                    if (weapon.range != 0) or weapon.finesse:
                                        can_sneak_attack = False                                        
                                        if advantage:
                                            print_indent( combatant.name + ' has advantage on the strike, and gains Sneak Attack!')
                                            can_sneak_attack = True
                                        elif enemy_in_melee_range(combatant.target,combatant) and not check_condition(combatant,condition.Incapacitated): 
                                            print_indent( 'Another enemy is in melee range of ' + combatant.target.name + ', granting ' + combatant.name + ' Sneak Attack!')
                                            can_sneak_attack = True
                                        if can_sneak_attack:
                                            for x in range(0,combatant.sneak_attack_damage_die_count):                                    
                                                die_damage = roll_die(combatant.sneak_attack_damage_die)
                                                print_double_indent( combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.sneak_attack_damage_die) + ' (Sneak Attack Damage)')
                                                dice_damage += die_damage
                                            combatant.sneak_attack_used = True                                            

                            ### Critical Hit features ###
                            if crit:
                                dice_damage = dice_damage * 2
                                                                        
                                # restore grit on critical # 
                                if combatant.current_grit < combatant.max_grit:
                                    print_indent( combatant.name + ' regained 1 grit point for scoring a critical hit!')
                                    combatant.current_grit = combatant.current_grit + 1;
                    
                                #Brutal Critical feature
                                if combatant.brutal_critical:
                                    print_indent( combatant.name + ' dealt massive damage with Brutal Critical! Rolling an additional ' + repr(combatant.brutal_critical_dice) + 'd' + repr(weapon.damage_die))
                                    for x in range(0,combatant.brutal_critical_dice):                            
                                        die_damage = roll_die(weapon.damage_die)            
                                        print_double_indent( combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(weapon.damage_die) + ' (Brutal Critical damage)')
                                        #Per https://www.reddit.com/r/criticalrole/comments/823w9v/spoilers_c1_another_dnd_combat_simulation/dv7r55m/
                                        # Brutal Critical does not benefit from Great Weapon Fighting (only applies to the attack)
                                        #if greatweaponfighting and die_damage <= 2:
                                        #    print_output(combatant.name + ' rerolled a weapon die due to Great Weapon Fighting!')                                           
                                        #    die_damage = roll_die(weapon.damage_die)            
                                        #    print_output(combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(weapon.damage_die) + ' (Brutal Critical damage)')
                                        dice_damage += die_damage              
                            
                                #Hemorraghing Critical feature
                                if combatant.hemorrhaging_critical and weapon.weapon_type == weapon_type.Firearm:
                                    print_indent( combatant.name + ' scored a Hemorraghing Critical!')
                                    #Set boolean to track and increase hemo damage (possible multiple crits per round)
                                    track_hemo = True                                                
                            
                            # Feat damage features:
                            if combatant.use_sharpshooter:
                                feat_bonus = 10
                                print_double_indent( combatant.name + ' dealt an additional ' + repr(feat_bonus) + ' damage because of Sharpshooter')

                            if combatant.use_great_weapon_master:
                                feat_bonus = 10
                                print_double_indent( combatant.name + ' dealt an additional ' + repr(feat_bonus) + ' damage because of Great Weapon Master')
                
                            # Total initial damage of attack
                            totaldamage = dice_damage + damage_modifier + feat_bonus            

                            if feat_bonus == 0:
                                print_indent( combatant.name + '\'s strike dealt a total of ' + damage_text(repr(totaldamage)) + ' points of ' + weapon_damage_type.name + ' damage')
                            else:
                                print_indent( combatant.name + '\'s strike dealt a total of ' + damage_text(repr(totaldamage)) + ' points of ' + weapon_damage_type.name + ' damage')
                            
                            deal_damage(combatant,combatant.target,totaldamage,weapon_damage_type,weapon.magic,crit)
                
                            if track_hemo:
                                print_indent( combatant.name + ' adds an extra ' + damage_text(repr(int(totaldamage/2))) + ' damage via Hemorrhaging Critical, which will be dealt at the end of ' + combatant.target.name + '\'s turn.')
                                combatant.target.hemo_damage += int(totaldamage/2)
                                combatant.target.hemo_damage_type = weapon_damage_type
                                track_hemo = False

                            ### Bonus damage effects
                            # Temporary effects (i.e. Enlarge)
                            if check_condition(combatant,condition.Enlarged):
                                print_indent( 'The sheer size of ' + combatant.name + ' allows them to deal an additional 1d4 damage thanks to Enlarge!')
                                resolve_bonus_damage(combatant,weapon.bonus_damage_target,weapon_damage_type,4,1,0,crit,'Enlarge',weapon.magic)

                            # Bonus damage (from weapon)
                            if weapon.bonus_damage_die > 0:
                                print_indent( 'The strike from ' + weapon.name + ' deals an additional ' + repr(weapon.bonus_damage_die_count) + 'd' + repr(weapon.bonus_damage_die) + ' ' + weapon.bonus_damage_type.name + ' damage!')
                                resolve_bonus_damage(combatant,weapon.bonus_damage_target,weapon.bonus_damage_type,weapon.bonus_damage_die,weapon.bonus_damage_die_count,0,crit,weapon.name,weapon.magic)

                            # Bonus damage (from critical weapon effect, i.e. Arkhan's weapon)
                            if crit and weapon.crit_bonus_damage_die > 0:
                                print_indent( weapon.name + ' surges with power, dealing bonus damage on a critical strike!')                            
                                resolve_bonus_damage(combatant,0,weapon.crit_bonus_damage_type,weapon.crit_bonus_damage_die,weapon.crit_bonus_damage_die_count,0,crit,weapon.name,weapon.magic)                        
    
                            # Bonus damage (from Blood Hunter's Crimson Rite)
                            if combatant.crimson_rite:
                                if weapon.active_crimson_rite != None:
                                    print_indent( 'The ' + weapon.active_crimson_rite.colour + ' light on ' + weapon.name + ' flares as the Crimson ' + weapon.active_crimson_rite.name + ' deals additional damage!')
                                    crimson_rite_bonus = 0
                                    # Add bonus damge (i.e. Ghostslayer gets +wismod on undead up to level 11, +wismod on everything after that)
                                    if weapon.active_crimson_rite.bonus_damage != 0:
                                        if weapon.active_crimson_rite.bonus_damage_target == None or combatant.target.race == weapon.active_crimson_rite.bonus_damage_target:
                                            crimson_rite_bonus = weapon.active_crimson_rite.bonus_damage

                                    resolve_bonus_damage(combatant,0,damage_type(weapon.active_crimson_rite.damage_type),combatant.crimson_rite_damage_die,1,crimson_rite_bonus,crit,weapon.active_crimson_rite.name,True)                        

                            #Bonus damage (from hand of Vecna, 2d8 cold damage on melee hit)
                            for item in combatant.equipment_inventory():
                                if item.grants_equipment_spell == equipment_spells.HandOfVecna and weapon.range == 0:
                                    print_indent( combatant.name + '\'s left hand crackles with power! They dealt bonus damage with the ' + item.name)
                                    resolve_bonus_damage(combatant,0,item.damage_type,item.damage_die,item.damage_die_count,0,crit,item.name,True)
                        
                            # Bonus damage (from Barbarian Zealot's Divine Fury - 1d6 + half barbairna level, damage type selected by player)
                            if combatant.divine_fury:
                                if not combatant.divine_fury_used:
                                    print_indent( combatant.name + '\'s weapon crackles with the strength of their Divine Fury, dealing bonus damage (1d6 + half barbarian level)!')

                                    resolve_bonus_damage(combatant,0,combatant.divine_fury_damage_type,6,1,math.floor(get_combatant_class_level(combatant,player_class.Barbarian)/2),crit,"Divine Fury",True)
                                    combatant.divine_fury_used = True

                            # Bonus damage (from Improved Divine Smite)
                            if combatant.improved_divine_smite:
                                print_indent( combatant.name + '\'s eyes glow, as their attacks are infused with radiant energy from Improved Divine Smite!')                                                    
                                resolve_bonus_damage(combatant,0,damage_type.Radiant,8,1,0,crit,"Improved Divine Smite",True)

                            # All pre-attack resolutions must occur before this point - anything that can be reduced by Uncanny Dodge should be loaded against the 
                            # Check if any modifiers kick in to reduce the damage of the attack (i.e. Rogue Uncanny Dodge)
                            calculate_reduction_after_attack(combatant.target)                

                            #Conditionally cast spells/use items on crit after initial damage resolved
                            # Do some preliminary checking to make sure we do not inadvertantly burn a spell slot
                            if not check_condition(combatant.target,condition.Unconscious):    
                                if crit:                            
                                    #Cabal's Ruin
                                    #Only use cabal's on a crit, dump all charges
                                    for eq in combatant.equipment_inventory():
                                        if eq.grants_equipment_spell == equipment_spells.CabalsRuin:                              
                                            equipment_damage_type = eq.damage_type
                                            if eq.current_charges > 0:
                                                print_indent( combatant.name + ' activates ' + eq.name + ', pouring ' +  repr(eq.current_charges) + ' charges into ' + combatant.target.name + '!')
                                                for x in range(0,eq.current_charges):
                                                    die_damage = roll_die(eq.damage_die)                                
                                                    equipment_damage += die_damage * 2         
                                                    print_double_indent( combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(eq.damage_die) + ' (Cabal\'s Ruin damage)')
                                                eq.current_charges = 0                
                                                print_indent( combatant.name + ' dealt an additional ' + damage_text(repr(equipment_damage)) + ' points of ' + equipment_damage_type.name + ' damage with ' + eq.name)
                                                deal_damage(combatant,combatant.target,equipment_damage,equipment_damage_type,True,crit)                                                               

                                #Divine Smite
                                for spell in combatant.spell_list():
                                    if spell.name == "Divine Smite":
                                        #Casting Divine Smite should be the last resolution of any attack action
                                        #Note: Casting a spell calls its own 'resolve_damage' function, so this needs to be kept near the end of damage calculations
                                        cast_spell(combatant,spell,crit)

                            #Resolve all of the damage created by the attack and stored against the combatant object
                            resolve_damage(combatant.target)                
                            
                            #Resolve the fatality to check if the combatant is still alive/conscious
                            resolve_fatality(combatant.target)
                        else:
                            print_output(combatant.name + '\'s attack (' + repr(totalatk) + ') against ' + combatant.target.name +  ' (AC ' + repr(totalAC) + ') with ' + weapon.name + ' MISSED!')        
                            #Update statistics
                            combatant.attacks_missed += 1

                        # consume ammo after shot #
                        if weapon.reload > 0:
                            weapon.currentammo = weapon.currentammo - 1            
                            print_output(weapon.name + ' Ammo: ' + repr(weapon.currentammo) + '/' + repr(weapon.reload))

                        #Thrown weapons get automatically unequipped after being thrown
                        if weapon.was_thrown == True:                            
                            weapon_swap(combatant,calc_distance(combatant,combatant.target))
                        
                        attackcomplete = True
            else:
                print_output(combatant.target.name + ' is dead on the ground, and not worthy of an attack.')
        else:
            print_output(combatant.target.name + ' is out of range of ' + weapon.name + '!')

    #Post-Attack features/decisions
    if attack_hit and can_continue_turn(combatant):
        # Stunning Strike - after a hit, spend 1 ki point to stun
        if combatant.stunning_strike and combatant.ki_points > 0:
            # Do not burn stunning strike if target is not threaten
            if can_continue_turn(combatant.target):
                combatant.ki_points -= 1
                print_output(combatant.name + ' focuses on the flow of Ki in ' + combatant.target.name + '\'s body, and attempts a Stunning Strike! Current Ki Points: ' + repr(combatant.ki_points) + '/' + repr(combatant.max_ki_points))            
                if savingthrow(combatant.target,saving_throw.Constitution,8+combatant.proficiency+wismod(combatant)):
                    print_output(combatant.target.name + ' resists the attempt to manipulate the flow of ki in their body, and is unaffected by the Stunning Strike!')
                else:
                    print_output(combatant.target.name + ' seizes up as the flow of Ki through their body is disrupted by the Stunning Strike!')
                    inflict_condition(combatant.target,combatant,condition.Incapacitated,1)
                    inflict_condition(combatant.target,combatant,condition.Stunned,1)

    return(attack_hit)

def calc_to_hit_modifier(combatant,weapon):
    to_hit = 0
    # Add 2 for fighting style when using ranged weapon with Archery
    if combatant.fighting_style == fighting_style.Archery and weapon.range > 0:
        to_hit += 2;

    stat_modifier_applied = False
    for class_instance in combatant.player_classes():
        if class_instance.player_class == player_class.Warlock:
            if class_instance.player_subclass == player_subclass.PactOfTheBlade:
                to_hit += chamod(combatant)    
                stat_modifier_applied = True

    if not stat_modifier_applied:
        # Add Dex modifier for finesse weapons, otherwise Str
        # Monk weapons also have this property (which is actually independent of Finesse)    
        if weapon.finesse or weapon.monk_weapon or weapon.range > 0:
            to_hit += dexmod(combatant)
        else:
            to_hit += strmod(combatant)

    # Add proficiency bonus if proficiency in weapon
    for combatant_weapon_proficiency in combatant.weapon_proficiency():
        if weapon.weapon_type != 0 and weapon.weapon_type == combatant_weapon_proficiency:
            to_hit += combatant.proficiency

    # Add weapon bonus (i.e. +3 weapon)
    to_hit += weapon.magic_to_hit_modifier
        
    return to_hit

def calc_damage_modifier(combatant,weapon):
    additional_damage = 0
    
    stat_modifier_applied = False
    for class_instance in combatant.player_classes():
        if class_instance.player_class == player_class.Warlock:
            if class_instance.player_subclass == player_subclass.PactOfTheBlade:
                additional_damage += chamod(combatant)    
                stat_modifier_applied = True

    if not stat_modifier_applied:
        # Do not add ability modifier to additional_damage on bonus action attacks (unless we have a feat or class feature)
        if ((weapon == weapon) or (weapon == combatant.offhand_weapon and combatant.fighting_style == fighting_style.Two_Weapon_Fighting)):
            # Add Dex modifier for finesse weapons and range weapons if it is higher than Str; otherwise Str
            # Monk weapons also have this property (which is actually independent of Finesse)
            if (dexmod(combatant) > strmod(combatant) and (weapon.finesse or weapon.monk_weapon or (weapon.range > 0 and not weapon.thrown))):        
                additional_damage += dexmod(combatant)
                stat_modifier_applied = True
            else:
                additional_damage += strmod(combatant)
                stat_modifier_applied = True

    # Rage
    if check_condition(combatant,condition.Raging) and not combatant.armour_type == armour_type.Heavy:
        additional_damage += combatant.rage_damage
    
    # Add weapon bonus (i.e. +3 weapon)
    additional_damage += weapon.magic_damage_modifier
        
    return additional_damage

def calc_min_crit(combatant,weapon):
    min_crit = 20
    # Fighter - Gunslinger - Vicious Intent, crit on a 19 with Firearm
    if combatant.vicious_intent and weapon.weapon_type == weapon_type.Firearm:
        min_crit = 19
    return min_crit