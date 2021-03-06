#Explicit imports

#Implicit imports
from battle_simulator.classes import *
from battle_simulator.combat_functions.inventory import * 
from battle_simulator.combat_functions.conditions import *
from battle_simulator.initialise_spells import * 

#Other imports

def reset_combatants(init_combatants):
    #Initialise Battle
    for combatant in init_combatants:                   

        # remove any conditions affecting combatats
        combatant.creature_conditions().clear()
        
        # Reset creature values #
        combatant.alive = True
        combatant.death_saving_throw_failure = 0
        combatant.death_saving_throw_success = 0
        combatant.current_health = combatant.max_health        
        combatant.action_surge = 0
        combatant.extra_attack = 0
        
        # Clear any pending damage against the combatant that was not resolved (i.e. damage dealt via crit to unconscious player doesn't get deducted from hp)
        combatant.pending_damage().clear()

        # Reset weapons
        for weap in combatant.weapon_inventory():
            weap.ruined = False
            weap.broken = False
            weap.current_ammo = weap.ammunition
        
        # Wield the first weapon in inventory
        if len(combatant.weapon_inventory()) > 0:
            wield(combatant,combatant.weapon_inventory()[0],True)

        # If the combatant has two weapon fighting, wield the next weapon in inventory as well
        if combatant.fighting_style == fighting_style.Two_Weapon_Fighting:
            if combatant.weapon_inventory()[1] != None:
                wield(combatant,combatant.weapon_inventory()[1],False)

        # Clear any properties on the blade
        if combatant.main_hand_weapon != None:
            combatant.main_hand_weapon.active_crimson_rite = None

        # Reset equipment
        for eq in combatant.equipment_inventory():
            eq.current_charges = eq.max_charges

        # Hemorraging Critical tracking
        combatant.hemo_damage = 0        
        combatant.hemo_damage_type = 0

        #Setup feats
        combatant.luck_uses = 0
        for ft in combatant.creature_feats():
            if ft == feat.Sharpshooter:
                combatant.sharpshooter = True
                combatant.use_sharpshooter = False
            if ft == feat.Great_Weapon_Master:
                combatant.great_weapon_master = True
                combatant.use_great_weapon_master = False
            if ft == feat.Lucky:
                combatant.luck_uses = 3

        # Set up class features (i.e. Rage, Sneak Attack, innate abilities)
        initialise_class_features(combatant)      
                        
        # Set up spellslots
        initialise_class_spellslots(combatant)           
                
        # Set up spells
        initialise_spells(combatant)

        # Racial Features
        # Goliath
        if combatant.race == race.Goliath:        
            combatant.stones_endurance = True
            combatant.stones_endurance_used = False    

        ### monsters###
        if combatant.creature_type == creature_type.Monster:
            if combatant.monster_type == monster_type.Ancient_Black_Dragon:
                combatant.multiattack = ["Bite","Claw","Claw"]
                combatant.breath_attack = True
                combatant.breath_damage_die = 8
                combatant.breath_range = 90               

            ### Trinket ###
            if combatant.monster_type == monster_type.Bear:
                combatant.multiattack = ["Bite","Claw"]

            ### Doty ###
            if combatant.monster_type == monster_type.Doty:                            
                combatant.multiattack = ["Bash","Headbutt"]

            ### Hill Giant
            if combatant.monster_type == monster_type.Hill:                            
                combatant.multiattack = ["Greatclub","Greatclub"]
            
            ### Oni
            if combatant.monster_type == monster_type.Oni:
                combatant.multiattack = ["Glaive","Glaive"]

            ### Venom Troll
            if combatant.monster_type == monster_type.Venom:                            
                combatant.multiattack = ["Claw","Bite"]

            ### Hydra (one bite per head)
            if combatant.monster_type == monster_type.Hydra:                            
                #Initialise at head count
                combatant.multiattack = []
                i = 1
                while i <= combatant.current_head_count:
                    combatant.multiattack.append("Bite")
                    i += 1
                combatant.head_lost_this_turn = False
                combatant.last_turn_head_count = combatant.current_head_count

            ### Fire Giant 
            if combatant.monster_type == monster_type.FireGiant:
                combatant.multiattack = ["Greatsword","Greatsword"]
                
            ### Fire Giant 
            if combatant.monster_type == monster_type.FireGiantDreadnought  :
                combatant.multiattack = ["Fireshield","Fireshield"]

            ### Beast forms
            if combatant.monster_type == monster_type.Eagle:
                combatant.multiattack = ["Beak","Talon"]
            
def initialise_class_features(combatant):
    ### Initialise Class Abilities ###        
    for class_instance in combatant.player_classes():
        #############
        # Barbarian #
        #############
        if class_instance.player_class == player_class.Barbarian:
            # Rage (1st level)
            if class_instance.player_class_level >= 1:
                combatant.barbarian_unarmoured_defense = True
                combatant.canrage = True                
                #+2 Rage Damage (1st through 8th)
                combatant.rage_damage = 2
            # Reckless Attack (2nd level)
            if class_instance.player_class_level >= 2:
                combatant.reckless = True        
                combatant.use_reckless = False
                # Danger Sense (2nd level)        
                combatant.saves.dex_adv = True                
            # Extra Attack (+1 at 5th level)
            if class_instance.player_class_level >= 5:
                if combatant.extra_attack <= 1:
                    combatant.extra_attack = 1
            # Feral Instinct (7th level)
            if class_instance.player_class_level >= 7:
                combatant.feral_instinct = True
            # Brutal Critical (1 die, 9th level)
            if class_instance.player_class_level >= 9:
                combatant.brutal_critical = True
                combatant.brutal_critical_dice = 1
                #+3 Rage Damage (9th through 16th)
                combatant.rage_damage = 3
            # Relentless (11th level)
            if class_instance.player_class_level >= 11:
                combatant.relentless_rage = True
                combatant.relentless_rage_DC = 10        
            # Brutal Critical (2 die, 13th level)
            if class_instance.player_class_level >= 13:
                combatant.brutal_critical_dice = 2
            if class_instance.player_class_level >= 16:
                #+3 Rage Damage (9th through 16th)
                combatant.rage_damage = 4
            # Brutal Critical (3 die, 17th level)
            if class_instance.player_class_level >= 17:
                combatant.brutal_critical_dice = 3
                            
            ## Barbarian Subclasses ##
            # Path of the Beserker
            if class_instance.player_subclass == player_subclass.PathOfTheBeserker:
                # Frenzy (3rd level)
                if class_instance.player_class_level >= 3:
                    combatant.frenzy = True
                # Retaliation (14th level)
                if class_instance.player_class_level >= 14:
                    combatant.retaliation = True

            # Path of the Zealot
            if class_instance.player_subclass == player_subclass.PathOfTheZealot:
                # Divine Fury (3rd level, 1d6+half barb level to first attack each turn while raging)
                if class_instance.player_class_level >= 3:
                    combatant.divine_fury = True
                    combatant.divine_fury_damage_type = damage_type.Necrotic
                # Fanatical Focus (6th level, reroll one failed save per rage, must take second roll)
                if class_instance.player_class_level >= 6:
                    combatant.fanatical_focus = True
                # Zealous Presence (10th level, once per LR advantage on attacks/saving throws to 10 creatures in 60 feet as bonus action until end of next turn)
                if class_instance.player_class_level >= 10:
                    combatant.zealous_presence = True
                # Rage Beyond death (14th level, while raging, fall below 0 you don't go unconscious - still make Death Saving Throws)
                if class_instance.player_class_level >= 14:
                    combatant.rage_beyond_death = True
        #############
        #### Bard ###
        #############
        if class_instance.player_class == player_class.Bard:            
            if class_instance.player_class_level >= 1:
                combatant.max_bardic_inspirations = chamod(combatant)
                combatant.bardic_inspirations = combatant.max_bardic_inspirations
                combatant.bardic_inspiration_die = 6
            if class_instance.player_class_level >= 5:
                combatant.bardic_inspiration_die = 8
            if class_instance.player_class_level >= 10:
                combatant.bardic_inspiration_die = 10
            if class_instance.player_class_level >= 15:
                combatant.bardic_inspiration_die = 12

            if class_instance.player_subclass == player_subclass.CollegeOfLore:
                if class_instance.player_class_level >= 3:
                    combatant.cutting_words = True

        #############
        #Blood Hunter
        #############
        if class_instance.player_class == player_class.BloodHunter:            
            if class_instance.player_class_level >= 1:
                combatant.crimson_rite = True          
                combatant.crimson_rite_damage_die = 4
                #Crimson rites are normally constructed on the player object; add a generic rite here if none exist
                if len(combatant.crimson_rites()) == 0:
                    init_rite = crimson_rite()
                    init_rite.name = "Rite of the Flame"
                    init_rite.damage_type = damage_type.Fire
                    init_rite.primal = True
                    init_rite.activation_damage = characterlevel(combatant)
                    init_rite.colour = "red"
                    combatant.crimson_rites().append(init_rite)                
            if class_instance.player_class_level >= 2:
                combatant.blood_maledict = True
                combatant.blood_maledict_uses = 1            
                #Blood Curses are normally constructed on the player object; add a generic curse here if none exist
                if len(combatant.blood_curses()) == 0:
                    init_curse = blood_curse()
                    init_curse.name = "Blood Curse of the Marked"
                    init_curse.uses_bonus_action = True
                    init_curse.amplify_hit_die_cost = 1
                    init_curse.duration = 1
                    combatant.blood_curses().append(init_curse)
            if class_instance.player_class_level >= 5:
                combatant.crimson_rite_damage_die = 6
                if combatant.extra_attack <= 1:
                    combatant.extra_attack = 1
                combatant.blood_maledict_uses = 2                              
            # Dark Velocity (+10 feet speed, AoO on you have disadvantge)
            if class_instance.player_class_level >= 11:
                combatant.crimson_rite_damage_die = 8
                combatant.blood_maledict_uses = 3
                combatant.dark_velocity = True
            # Hardened Soul (immune to Frightened, advantage on Charm saving throws)
            if class_instance.player_class_level >= 14:
                combatant.hardened_soul = True 
            if class_instance.player_class_level >= 17:
                combatant.crimson_rite_damage_die = 10
                combatant.blood_maledict_uses = 4
            # Max crimson rite damage die on 1/4 hit points; regain blood maledict use on crit
            if class_instance.player_class_level >= 20:
                combatant.sanguine_mastery = True

            ## Blood Hunter Subclasses ##
            # Ghostslayer
            if class_instance.player_subclass == player_subclass.OrderOfTheGhostslayer:
                if class_instance.player_class_level >= 3:                                    
                    init_rite = crimson_rite()
                    init_rite.name = "Rite of the Dawn"
                    init_rite.damage_type = damage_type.Radiant
                    init_rite.primal = False
                    init_rite.activation_damage = int(characterlevel(combatant)/2)
                    init_rite.bonus_damage = wismod(combatant)
                    init_rite.bonus_damage_target = race.Undead
                    init_rite.colour = "white"
                    combatant.crimson_rites().append(init_rite)
                if class_instance.player_class_level >= 7:
                    combatant.hallowed_veins = True
                if class_instance.player_class_level >= 10:
                    combatant.supernal_flurry = True
                if class_instance.player_class_level >= 11:
                    for rite in combatant.crimson_rites:
                        if rite.name == "Rite of the Dawn":
                            rite.bonus_damage_target = None
                if class_instance.player_class_level >= 18:
                    combatant.vengeful_spirit = True
        
        #############
        ### Druid ###
        #############
        if class_instance.player_class == player_class.Druid:            
            if class_instance.player_class_level >= 2:
                combatant.wild_shape = True
                combatant.max_wild_shapes = 2
                wild_shape_max_cr = class_instance.player_class_level / 8
            if class_instance.player_class_level >= 18:
                combatant.beast_spells = True
            if class_instance.player_class_level >= 20:
                combatant.max_wild_shapes = 999

        #############
        ## Fighter ##
        #############
        if class_instance.player_class == player_class.Fighter:
            # Action surge (1 at 2nd level
            if class_instance.player_class_level >= 2:
                combatant.action_surge += 1
            # Action surge (2 at 17th level)
            if class_instance.player_class_level >= 17:
                combatant.action_surge += 1

            # Extra Attack (+1 at 5th level)
            if class_instance.player_class_level >= 5:
                if combatant.extra_attack <= 1:
                    combatant.extra_attack = 1
            # Extra Attack (+1 at 11th level)
            if class_instance.player_class_level >= 11:
                if combatant.extra_attack <= 2:
                    combatant.extra_attack = 2
            # Extra Attack (+1 at 20th level)
            if class_instance.player_class_level >= 20:
                if combatant.extra_attack <= 3:
                    combatant.extra_attack = 3
            
            # Second Wind (1 use at 1st level)
            if class_instance.player_class_level >= 1:
                combatant.second_wind = True                        
        
            ## Fighter Subclasses ##
            # Gunslinger (examine profiencies for Firearm proficiency, use fighter levels to determine abilities)        
            if class_instance.player_subclass == player_subclass.Gunslinger:
                # Grit (3rd level)
                combatant.max_grit = wismod(combatant) #Some debate as to whether this should be Int or Wis (Int was used by Percy in some fights)
                combatant.current_grit = combatant.max_grit

                #Quickdraw (7th level)
                if class_instance.player_class_level >= 7:
                    combatant.quickdraw = True
                #Lightning Reload (15th level)
                if class_instance.player_class_level >= 15:
                    combatant.lighting_reload = True        
                #Vicious Intent (18th level)
                if class_instance.player_class_level >= 18:
                    combatant.vicious_intent = True       
                #Hemorrhaging Critical (20th level)
                if class_instance.player_class_level >= 20:
                    combatant.hemorrhaging_critical = True

        #############
        #### Monk ###
        #############
        if class_instance.player_class == player_class.Monk:
            if class_instance.player_class_level >= 1:
                combatant.monk_unarmoured_defense = True
                combatant.martial_arts = True
                combatant.martial_arts_die = 4                
            if class_instance.player_class_level >= 2:
                combatant.ki = True
                # Max Ki Points = Monk level                
                combatant.max_ki_points = class_instance.player_class_level
                combatant.ki_points = combatant.max_ki_points
                combatant.flurry_of_blows = True
                combatant.patient_defense = True
                combatant.step_of_the_wind = True
                combatant.unarmoured_movement = True
                combatant.unarmoured_movement_bonus = 10
            if class_instance.player_class_level >= 3:
                combatant.deflect_missiles = True
            if class_instance.player_class_level >= 4:
                combatant.slow_fall = True
            if class_instance.player_class_level >= 5:
                combatant.martial_arts_die = 6       
                if combatant.extra_attack <= 1:
                    combatant.extra_attack = 1
                combatant.stunning_strike = True
            if class_instance.player_class_level >= 6:
                combatant.unarmoured_movement_bonus = 15
                combatant.ki_empowered_strikes = True
            if class_instance.player_class_level >= 7:
                combatant.stillness_of_mind = True
                combatant.evasion = True
            if class_instance.player_class_level >= 10:
                combatant.unarmoured_movement_bonus = 20
                combatant.purity_of_body = True
            if class_instance.player_class_level >= 11:
                combatant.martial_arts_die = 8                       
            if class_instance.player_class_level >= 14:
                combatant.unarmoured_movement_bonus = 25
                combatant.diamond_soul = True                
            if class_instance.player_class_level >= 18:
                combatant.unarmoured_movement_bonus = 30
            if class_instance.player_class_level >= 17:
                combatant.martial_arts_die = 10       


        #############
        ## Paladin ##
        #############
        if class_instance.player_class == player_class.Paladin:
            # Divine Smite (2nd level)
            if class_instance.player_class_level >= 2:
                combatant.divine_smite = True                                

            # Channel Divinity
            if class_instance.player_class_level >= 3: 
                combatant.channel_divinity = True

            # Extra Attack (5th level)
            if class_instance.player_class_level >= 5:
                # Extra attacks from multiclassing do not stack, only give one attack                
                if combatant.extra_attack <= 1:
                    combatant.extra_attack = 1

            # Improved Divine Smite (14th level)
            if class_instance.player_class_level >= 14:
                combatant.improved_divine_smite = True   
                
            ## Paladin Subclasses ##
            # Oath of Vengeance
            if class_instance.player_subclass == player_subclass.Vengeance:
                if class_instance.player_class_level >= 3:
                    combatant.vow_of_enmity = True
                    combatant.vow_of_enmity_target = None

        #############
        ### Ranger ##
        #############
        if class_instance.player_class == player_class.Ranger:
            if class_instance.player_class_level >= 5:
                if combatant.extra_attack <= 1:
                    combatant.extra_attack = 1

        #############
        ### Rogue ###
        #############
        if class_instance.player_class == player_class.Rogue:
            # Sneak Attack
            if class_instance.player_class_level >= 1:
                combatant.sneak_attack = True
                combatant.sneak_attack_damage_die = 6
                combatant.sneak_attack_damage_die_count = int(round(class_instance.player_class_level/2))

            # Cunning Action (Dash/Hide/Disengage as Bonus)
            if class_instance.player_class_level >= 2:
                combatant.cunning_action = True
            # Uncanny Dodge (Use reaction to halve damage from melee strike)
            if class_instance.player_class_level >= 5:
                combatant.uncanny_dodge = True
            # Evasion (Fail Dex save = half damage, succeed = 0)
            if class_instance.player_class_level >= 7:
                combatant.evasion = True
            # Blindsense (always detect hidden/invis creatures in 10 feet)
            if class_instance.player_class_level >= 14:
                combatant.blindsense = True
            # Slippery Mind (prof in Wisdom saving throws)
            if class_instance.player_class_level >= 15:
                combatant.slippery_mind = True
            # Elusive (no attacks have advantage against you while not incapacitated)
            if class_instance.player_class_level >= 18:
                combatant.elusive = True
            # Stroke of Luck (any miss can hit, any fail check can critically succeed, recharge short/long rest)
            if class_instance.player_class_level >= 20:
                combatant.elusive = True

            ## Rogue Subclasses ##
            # Assassin
            if class_instance.player_subclass == player_subclass.Assassin:
                if class_instance.player_class_level >= 3:
                    combatant.assassinate = True               

def set_starting_positions(combatants):
    for combatant in combatants:
        combatant.xpos = combatant.starting_xpos
        combatant.ypos = combatant.starting_ypos        