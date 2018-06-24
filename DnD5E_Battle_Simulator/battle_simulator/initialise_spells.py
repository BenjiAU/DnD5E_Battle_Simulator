#Explicit imports

#Implicit imports
from battle_simulator.classes import *
from battle_simulator.combat_functions.inventory import * 
from battle_simulator.combat_functions.conditions import * 
#Other imports

def initialise_class_spellslots(combatant):
    reset_spellslots(combatant)

    ### Set maximum number of spellslots based on spells available to classes ###        
    for class_instance in combatant.player_classes():        
        ### Cleric spellslots ###
        if class_instance.player_class == player_class.Cleric:
            if class_instance.player_class_level == 1:
                add_spellslot(combatant,1,2)
            if class_instance.player_class_level >= 2:
                add_spellslot(combatant,1,1)                
            if class_instance.player_class_level >= 3:
                add_spellslot(combatant,1,1)         
                add_spellslot(combatant,2,2)         
            if class_instance.player_class_level >= 4:
                add_spellslot(combatant,2,1)         
            if class_instance.player_class_level >= 5:
                add_spellslot(combatant,3,2)         
            if class_instance.player_class_level >= 6:
                add_spellslot(combatant,3,1)         
            if class_instance.player_class_level >= 7:
                add_spellslot(combatant,4,1)         
            if class_instance.player_class_level >= 8:
                add_spellslot(combatant,4,1)         
            if class_instance.player_class_level >= 9:
                add_spellslot(combatant,4,1)         
                add_spellslot(combatant,5,1)         
            if class_instance.player_class_level >= 10:
                add_spellslot(combatant,5,1)         
            if class_instance.player_class_level >= 11:
                add_spellslot(combatant,6,1)                     
            if class_instance.player_class_level >= 13:
                add_spellslot(combatant,7,1)         
            if class_instance.player_class_level >= 15:
                add_spellslot(combatant,8,1)                                     
            if class_instance.player_class_level >= 17:
                add_spellslot(combatant,9,1)         
            if class_instance.player_class_level >= 18:
                add_spellslot(combatant,5,1)         
            if class_instance.player_class_level >= 19:
                add_spellslot(combatant,6,1)         
            if class_instance.player_class_level >= 20:
                add_spellslot(combatant,7,1)         

        ### Paladin Spellslots ###
        if class_instance.player_class == player_class.Paladin:
            if class_instance.player_class_level >= 2:
                add_spellslot(combatant,1,2)                
            if class_instance.player_class_level >= 3:
                add_spellslot(combatant,1,1)
            if class_instance.player_class_level >= 4:
                add_spellslot(combatant,1,1)
            if class_instance.player_class_level >= 5:
                add_spellslot(combatant,2,2)
            if class_instance.player_class_level >= 7:
                add_spellslot(combatant,2,1)
            if class_instance.player_class_level >= 9:
                add_spellslot(combatant,3,2)
            if class_instance.player_class_level >= 11:
                add_spellslot(combatant,3,1)
            if class_instance.player_class_level >= 13:
                add_spellslot(combatant,4,1)
            if class_instance.player_class_level >= 15:
                add_spellslot(combatant,4,1)
            if class_instance.player_class_level >= 17:
                add_spellslot(combatant,4,1)
                add_spellslot(combatant,5,1)
            if class_instance.player_class_level >= 19:
                add_spellslot(combatant,5,1)

        ### Druid Spellslots ###
        if class_instance.player_class == player_class.Druid:
            if class_instance.player_class_level == 1:
                add_spellslot(combatant,1,2)
            if class_instance.player_class_level >= 2:
                add_spellslot(combatant,1,1)                

        ### Warlock Spellslots ###
        if class_instance.player_class == player_class.Warlock:
            if class_instance.player_class_level == 1:
                add_spellslot(combatant,1,2)
            if class_instance.player_class_level >= 2:
                add_spellslot(combatant,1,1)                
            if class_instance.player_class_level >= 3:
                add_spellslot(combatant,1,1)         
                add_spellslot(combatant,2,2)         
            if class_instance.player_class_level >= 4:
                add_spellslot(combatant,2,1)         
            if class_instance.player_class_level >= 5:
                add_spellslot(combatant,3,2)         
            if class_instance.player_class_level >= 6:
                add_spellslot(combatant,3,1)         
            if class_instance.player_class_level >= 7:
                add_spellslot(combatant,4,1)         
            if class_instance.player_class_level >= 8:
                add_spellslot(combatant,4,1)         
            if class_instance.player_class_level >= 9:
                add_spellslot(combatant,4,1)         
                add_spellslot(combatant,5,1)         
            if class_instance.player_class_level >= 10:
                add_spellslot(combatant,5,1)         
            if class_instance.player_class_level >= 11:
                add_spellslot(combatant,6,1)                     
            if class_instance.player_class_level >= 13:
                add_spellslot(combatant,7,1)         
            if class_instance.player_class_level >= 15:
                add_spellslot(combatant,8,1)                                     
            if class_instance.player_class_level >= 17:
                add_spellslot(combatant,9,1)         
            if class_instance.player_class_level >= 18:
                add_spellslot(combatant,5,1)         
            if class_instance.player_class_level >= 19:
                add_spellslot(combatant,6,1)         
            if class_instance.player_class_level >= 20:
                add_spellslot(combatant,7,1)         
                
        ### Wizard Spellslots ###
        if class_instance.player_class == player_class.Wizard:
            if class_instance.player_class_level == 1:
                add_spellslot(combatant,1,2)
            if class_instance.player_class_level >= 2:
                add_spellslot(combatant,1,1)                
            if class_instance.player_class_level >= 3:
                add_spellslot(combatant,1,1)         
                add_spellslot(combatant,2,2)         
            if class_instance.player_class_level >= 4:
                add_spellslot(combatant,2,1)         
            if class_instance.player_class_level >= 5:
                add_spellslot(combatant,3,2)         
            if class_instance.player_class_level >= 6:
                add_spellslot(combatant,3,1)         
            if class_instance.player_class_level >= 7:
                add_spellslot(combatant,4,1)         
            if class_instance.player_class_level >= 8:
                add_spellslot(combatant,4,1)         
            if class_instance.player_class_level >= 9:
                add_spellslot(combatant,4,1)         
                add_spellslot(combatant,5,1)         
            if class_instance.player_class_level >= 10:
                add_spellslot(combatant,5,1)         
            if class_instance.player_class_level >= 11:
                add_spellslot(combatant,6,1)                     
            if class_instance.player_class_level >= 13:
                add_spellslot(combatant,7,1)         
            if class_instance.player_class_level >= 15:
                add_spellslot(combatant,8,1)                                     
            if class_instance.player_class_level >= 17:
                add_spellslot(combatant,9,1)         
            if class_instance.player_class_level >= 18:
                add_spellslot(combatant,5,1)         
            if class_instance.player_class_level >= 19:
                add_spellslot(combatant,6,1)         
            if class_instance.player_class_level >= 20:
                add_spellslot(combatant,7,1)         

def add_spellslot(combatant,spell_level,spellslot_count):
    for existing_spellslot in combatant.spellslots():
        if existing_spellslot.level == spell_level:
            existing_spellslot.current += spellslot_count
            existing_spellslot.max += spellslot_count
            return

    #Slot doesn't exist, create a new one
    newslot = spellslot()
    newslot.level = spell_level    
    newslot.current = spellslot_count
    newslot.max = spellslot_count
    combatant.spellslots().append(newslot)

def reset_spellslots(combatant):
    combatant.spellslots().clear()

def initialise_spells(combatant):
    
    
    
    for spell in combatant.spell_list():
    
    #############
    # Class Feats
    #############    
        if spell.name == "Divine Smite":                                                                                        
            spell.school = spell_school.Evocation
            spell.category = spell_category.Damage
            spell.min_spellslot_level = 1
            spell.max_spellslot_level = 6
            spell.casting_time = spell_casting_time.Instant
            spell.range = 0
            spell.origin = origin_point.Self
            spell.instance = 1

            spell.damage_die = 8
            spell.damage_die_count = 2
            spell.damage_type = damage_type.Radiant
            spell.bonus_damage_die = 8
            spell.bonus_damage_die_count = 1
            spell.bonus_damage_target = race.Undead
            spell.damage_die_per_spell_slot = 8
            spell.damage_die_count_per_spell_slot = 1       

    #############
    ## Cantrips #
    #############        

        if spell.name == "Sacred Flame":
            spell.school = spell_school.Evocation
            spell.category = spell_category.Damage
            spell.cantrip = True
                    
            spell.instance = 1
            spell.casting_time = spell_casting_time.Action
            spell.range = 60
            spell.origin = origin_point.Self                    
                                                            
            spell.player_classes().append(player_class.Cleric)

            spell.saving_throw_attribute = saving_throw.Dexterity
            spell.damage_die = 8
            spell.damage_die_count = 1
            spell.damage_type = damage_type.Radiant
                    
            if characterlevel(combatant) >= 1:                        
                spell.description = "A small burst of divine flame singes the flesh of"
            if characterlevel(combatant)  >= 5:
                spell.damage_die_count = 2                        
                spell.description = "A bright flash of divine energy engulfs the form of"
            if characterlevel(combatant)  >= 11:
                spell.damage_die_count = 3
                spell.description = "A powerful burst of radiant energy momentarily consumes the form of"
            if characterlevel(combatant)  >= 17:
                spell.damage_die_count = 4
                spell.description = "The sun appears to dim as a torrent of divine energy threatens to reduce into ash"

        if spell.name == "Eldritch Blast":                    
            spell.school = spell_school.Evocation
            spell.category = spell_category.Damage
            spell.cantrip = True
            spell.min_spellslot_level = 0
            spell.max_spellslot_level = 0
            spell.spell_attack = True
            spell.casting_time = spell_casting_time.Action

            spell.range = 120
            spell.origin = origin_point.Self                    
                    
            spell.damage_die = 10
            spell.damage_die_count = 1
            spell.damage_type = damage_type.Force

            if characterlevel(combatant) >= 1:
                spell.instance = 1
                spell.description = "A crackling beam of energy leaps toward"
            if characterlevel(combatant) >= 5:
                spell.instance = 2
                spell.description = "Two crackling beams of energy leap toward"
            if characterlevel(combatant) >= 11:
                spell.instance = 3
                spell.description = "Three crackling beams of energy leap toward"
            if characterlevel(combatant) >= 17:
                spell.instance = 4
                spell.description = "Four crackling beams of energy leap toward"

        if spell.name == "Firebolt":                    
            spell.school = spell_school.Evocation
            spell.category = spell_category.Damage
            spell.cantrip = True
            spell.min_spellslot_level = 0
            spell.max_spellslot_level = 0
            spell.spell_attack = True
            spell.instance = 1
            spell.casting_time = spell_casting_time.Action
            spell.range = 120
            spell.origin = origin_point.Self                    
                    
            spell.damage_die = 10
                    
            spell.damage_type = damage_type.Fire
            spell.player_classes().append(player_class.Wizard)

            if characterlevel(combatant)  >= 1:
                spell.damage_die_count = 1
                spell.description = "A mote of fire hurls towards"
            if characterlevel(combatant)  >= 5:
                spell.damage_die_count = 2
                spell.description = "A small globe of flame hurls towards"
            if characterlevel(combatant)  >= 11:
                spell.damage_die_count = 3
                spell.description = "A searing bolt of flame hurls towards"
            if characterlevel(combatant)  >= 17:
                spell.damage_die_count = 4
                spell.description = "A great roaring inferno hurls towards"       

    #############
    ## Level 1 ##
    #############        

        if spell.name == "Healing Word":                    
            spell.school = spell_school.Evocation
            spell.category = spell_category.Healing
            spell.min_spellslot_level = 1
            spell.max_spellslot_level = 9
            
            spell.instance = 1
            spell.casting_time = spell_casting_time.Bonus_Action
            spell.range = 60
            spell.origin = origin_point.Self                    
                                        
            spell.player_classes().append(player_class.Bard)
            spell.player_classes().append(player_class.Cleric)
            spell.player_classes().append(player_class.Druid)
                                
            spell.healing_die = 4
            spell.healing_die_count = 1                    
            
            spell.healing_die_per_spell_slot = 4
            spell.healing_die_count_per_spell_slot = 1                    

        if spell.name == "Cure Wounds":                    
            spell.school = spell_school.Evocation
            spell.category = spell_category.Healing
            spell.min_spellslot_level = 1
            spell.max_spellslot_level = 9
            
            spell.instance = 1
            spell.casting_time = spell_casting_time.Action
            spell.range = melee_range()
            spell.origin = origin_point.Self                    
                                        
            spell.player_classes().append(player_class.Bard)
            spell.player_classes().append(player_class.Cleric)
            spell.player_classes().append(player_class.Druid)
            spell.player_classes().append(player_class.Paladin)
            spell.player_classes().append(player_class.Ranger)
                                
            spell.healing_die = 8
            spell.healing_die_count = 1                    
            
            spell.healing_die_per_spell_slot = 8
            spell.healing_die_count_per_spell_slot = 1   

        if spell.name == "Chromatic Orb":                                            
            spell.school = spell_school.Evocation   
            spell.category = spell_category.Damage
            spell.min_spellslot_level = 1
            spell.max_spellslot_level = 9
            spell.spell_attack = True
            spell.instance = 1
            spell.casting_time = spell_casting_time.Action
            spell.range = 90
            spell.origin = origin_point.Self                    
                    
            spell.verbal = True
            spell.somatic = True
            spell.material = True
            spell.material_cost = 50

            spell.damage_die = 8
            spell.damage_die_count = 3

            spell.damage_die_per_spell_slot = 8
            spell.damage_die_count_per_spell_slot = 1

            spell.damage_type = damage_type.Fire # Default damage type, chosen based on targeT?
            spell.player_classes().append(player_class.Wizard)
            spell.player_classes().append(player_class.Sorcerer)

            spell.description = "A diamond spins in <casters> hand, and an orb of energy fires out towards"   

        if spell.name == "Burning Hands":                                            
            spell.school = spell_school.Evocation           
            spell.category = spell_category.AoE_Damage
            spell.min_spellslot_level = 1
            spell.max_spellslot_level = 9
            spell.instance = 1
            spell.casting_time = spell_casting_time.Action
            spell.range = 0
            spell.origin = origin_point.Self                    
            spell.shape = area_of_effect_shape.Line
            spell.shape_width = 15
            spell.shape_length = 15

            spell.verbal = True
            spell.somatic = True

            spell.damage_die = 6
            spell.damage_die_count = 3
            spell.saving_throw_attribute = saving_throw.Dexterity
            spell.saving_throw_damage_multiplier = 0.5

            spell.damage_die_per_spell_slot = 6
            spell.damage_die_count_per_spell_slot = 1

            spell.damage_type = damage_type.Fire
            spell.player_classes().append(player_class.Wizard)
            spell.player_classes().append(player_class.Sorcerer)

            spell.description = "As they hold their hands with thumbs touching and fingers spread, a thin sheet of flames shoots forth from outstretched fingertips towards"   

        if spell.name == "Magic Missile":                                            
            spell.school = spell_school.Evocation           
            spell.category = spell_category.Damage
            spell.min_spellslot_level = 1
            spell.max_spellslot_level = 9
            spell.instance = 3
            spell.casting_time = spell_casting_time.Action
            spell.range = 120
            spell.origin = origin_point.Self                    

            spell.verbal = True
            spell.somatic = True

            spell.damage_die = 4
            spell.damage_die_count = 1
            spell.flat_damage = 1

            spell.instance_per_spell_slot = 1

            spell.damage_type = damage_type.Force
            spell.player_classes().append(player_class.Wizard)
            spell.player_classes().append(player_class.Sorcerer)

            spell.description = "Magical darts spring into existence and fire towards"   

    #############
    ## Level 2 ##
    #############             
        if spell.name == "Enlarge":                    
            spell.school = spell_school.Transmutation
            spell.category = spell_category.Buff
            spell.min_spellslot_level = 2
            spell.max_spellslot_level = 9
                    
            spell.instance = 1
            spell.casting_time = spell_casting_time.Action
            spell.range = 30
            spell.origin = origin_point.Self                    
                                        
            spell.player_classes().append(player_class.Sorcerer)
            spell.player_classes().append(player_class.Wizard)
                    
            spell.condition = condition.Enlarged
            spell.condition_duration = 10
            spell.maximum_duration = spell.condition_duration

            spell.concentration = True      


        if spell.name == "Scorching Ray":                                            
            spell.school = spell_school.Evocation           
            spell.category = spell_category.Damage
            spell.min_spellslot_level = 2
            spell.max_spellslot_level = 9
            spell.spell_attack = True
            spell.instance = 3
            spell.casting_time = spell_casting_time.Action
            spell.range = 120
            spell.origin = origin_point.Self                    

            spell.verbal = True
            spell.somatic = True

            spell.damage_die = 6
            spell.damage_die_count = 2            

            spell.instance_per_spell_slot = 1

            spell.damage_type = damage_type.Fire
            spell.player_classes().append(player_class.Wizard)
            spell.player_classes().append(player_class.Sorcerer)

            spell.description = "Magical fire rays leap out and strike towards"   
 
            
        if spell.name == "Maximillian's Earthen Grasp":                                            
            spell.school = spell_school.Transmutation
            spell.category = spell_category.Debuff
            spell.min_spellslot_level = 2
            spell.max_spellslot_level = 2
            
            spell.instance = 1
            spell.casting_time = spell_casting_time.Action
            spell.range = 30
            spell.origin = origin_point.PointInRange
            spell.concentration = True

            spell.verbal = True
            spell.somatic = True
            spell.material = True

            spell.damage_die = 6
            spell.damage_die_count = 2            

            spell.condition = condition.Restrained
            spell.saving_throw_attribute = saving_throw.Strength            
            spell.saving_throw_damage_multiplier = 0.5

            spell.condition_duration = 10
            spell.maximum_duration = spell.condition_duration

            spell.repeat_save_action = True
            
            spell.damage_type = damage_type.Bludgeoning
            spell.player_classes().append(player_class.Wizard)
            spell.player_classes().append(player_class.Sorcerer)

            spell.description = "A hand of clay reaches out from the ground and grasps towards"   
        
    #############
    ## Level 3 ##
    #############             
        if spell.name == "Haste":                    
            spell.school = spell_school.Transmutation
            spell.category = spell_category.Buff
            spell.min_spellslot_level = 3
            spell.max_spellslot_level = 9
                    
            spell.instance = 1
            spell.casting_time = spell_casting_time.Action
            spell.range = 30
            spell.origin = origin_point.Self                    
                                        
            spell.player_classes().append(player_class.Sorcerer)
            spell.player_classes().append(player_class.Wizard)
                    
            spell.condition = condition.Hasted
            spell.condition_duration = 10
            spell.maximum_duration = spell.condition_duration

            spell.concentration = True                    

        if spell.name == "Slow":                    
            spell.school = spell_school.Transmutation
            spell.category = spell_category.AoE_Debuff
            spell.min_spellslot_level = 3
            spell.max_spellslot_level = 3
                    
            spell.instance = 1
            spell.casting_time = spell_casting_time.Action
            spell.range = 120
            spell.origin = origin_point.Self      
            spell.shape == area_of_effect_shape.Line
            spell.shape_width = 40
            spell.shape_length = 40
                                        
            spell.player_classes().append(player_class.Sorcerer)
            spell.player_classes().append(player_class.Wizard)
                   
            spell.saving_throw_attribute = saving_throw.Wisdom
            spell.condition = condition.Slowed
            spell.condition_duration = 10
            spell.maximum_duration = spell.condition_duration

            spell.concentration = True       
    