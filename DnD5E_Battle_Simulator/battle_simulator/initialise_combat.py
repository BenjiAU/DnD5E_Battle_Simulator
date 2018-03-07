#Explicit imports

#Implicit imports
from .classes import *

#Other imports


def reset_combatants(init_combatants):
    #Initialise Battle
    for combatant in init_combatants:                   

        # Reset creature values #
        combatant.alive = True
        combatant.current_health = combatant.max_health
        combatant.enlarged = False        # Need a better wayto handle this        
        combatant.action_surge = 0
        combatant.extra_attack = 0

        # Reset weapons
        for weap in combatant.weapon_inventory():
            weap.ruined = False
            weap.broken = False
            weap.current_ammo = weap.ammunition
                
        # Reset equipment
        for eq in combatant.equipment_inventory():
            eq.current_charges = eq.max_charges

        # Reset spell slots
        
        combatant.creature_spellslots.FirstLevel = combatant.creature_spellslots.FirstLevelMax
        combatant.creature_spellslots.SecondLevel = combatant.creature_spellslots.SecondLevelMax
        combatant.creature_spellslots.ThirdLevel = combatant.creature_spellslots.ThirdLevelMax
        combatant.creature_spellslots.FourthLevel = combatant.creature_spellslots.FourthLevelMax
        combatant.creature_spellslots.FifthLevel = combatant.creature_spellslots.FifthLevelMax
        combatant.creature_spellslots.SixthLevel = combatant.creature_spellslots.SixthLevelMax
        combatant.creature_spellslots.SeventhLevel = combatant.creature_spellslots.SeventhLevelMax
        combatant.creature_spellslots.EigthLevel = combatant.creature_spellslots.EigthLevelMax
        combatant.creature_spellslots.NinthLevel = combatant.creature_spellslots.NinthLevelMax
        # Hemorraging Critical tracking
        combatant.hemo_damage = 0        
        combatant.hemo_damage_type = 0

        #Setup feats
        for ft in combatant.creature_feats():
            if ft == feat.Sharpshooter:
                combatant.sharpshooter = True
                combatant.use_sharpshooter = False
            if ft == feat.Great_Weapon_Master:
                combatant.great_weapon_master = True
                combatant.use_great_weapon_master = False
                
        # Generic abilities (primary class need not be this to get benefit)
        # Fighter 
        # Action surge (1 at 2nd level
        if combatant.fighter_level >= 2:
            combatant.action_surge += 1
        # Action surge (2 at 17th level)
        if combatant.fighter_level >= 17:
            combatant.action_surge += 1

        # Extra Attack (+1 at 5th level)
        if combatant.fighter_level >= 5:
            combatant.extra_attack = 1
        # Extra Attack (+1 at 11th level)
        if combatant.fighter_level >= 11:
            combatant.extra_attack = 2
        # Extra Attack (+1 at 20th level)
        if combatant.fighter_level >= 20:
            combatant.extra_attack = 3
        
        # Second Wind (1 use at 1st level)
        if combatant.fighter_level >= 1:
            combatant.second_wind = True        
        
        # Barbarian
        # Rage (1st level)
        if combatant.barbarian_level >= 1:
            combatant.canrage = True
            combatant.raging = False
        # Reckless Attack (2nd level)
        if combatant.barbarian_level >= 2:
            combatant.reckless = True        
            combatant.use_reckless = False
        # Danger Sense (2nd level)
        if combatant.barbarian_level >= 2:
            combatant.saves.dex_adv = True                
        # Extra Attack (+1 at 5th level)
        if combatant.barbarian_level >= 5:
            if combatant.extra_attack == 0:
                combatant.extra_attack = 1
        # Feral Instinct (7th level)
        if combatant.barbarian_level >= 7:
            combatant.feral_instinct = True
        # Brutal Critical (1 die, 9th level)
        if combatant.barbarian_level >= 9:
            combatant.brutal_critical = True
            combatant.brutal_critical_dice = 1
        # Relentless (11th level)
        if combatant.barbarian_level >= 11:
            combatant.relentless_rage = True
            combatant.relentless_rage_DC = 10        
        # Brutal Critical (2 die, 13th level)
        if combatant.barbarian_level >= 13:
            combatant.brutal_critical_dice = 2
        # Brutal Critical (3 die, 17th level)
        if combatant.barbarian_level >= 17:
            combatant.brutal_critical_dice = 3
        
        # Paladin
        # Divine Smite (2nd level)
        if combatant.paladin_level >= 2:
            combatant.divine_smite = True
            # Add Divine Smite to combatants spell-book
            add_divine_smite = True
            for existing_spell in combatant.creature_spells():
                if existing_spell.name == "Divine Smite":
                    add_divine_smite = False
            if add_divine_smite: 
                divine_smite = spell()
                init_spell(divine_smite,"Divine Smite",1,6,8,2,damage_type.Radiant,8,1,8,1,race.Undead)
                combatant.creature_spells().append(divine_smite)

        # Extra Attack (5th level)
        if combatant.paladin_level >= 5:
            # Extra attacks from multiclassing do not stack, only give one attack
            if combatant.extra_attack == 0:
                combatant.extra_attack = 1

        # Improved Divine Smite (14th level)
        if combatant.paladin_level >= 14:
            combatant.improved_divine_smite = True
        # Specific abilities (primary class/subclass must be defined)
        # Gunslinger (examine profiencies for Firearm proficiency, use fighter levels to determine abilities)
        if combatant.creature_class == creature_class.Fighter:
            if combatant.creature_subclass == creature_subclass.Gunslinger:
                # Grit (3rd level)
                combatant.max_grit = wismod(combatant) #Some debate as to whether this should be Int or Wis (Int was used by Percy in some fights)
                combatant.current_grit = combatant.max_grit

                #Quickdraw (7th level)
                if combatant.fighter_level >= 7:
                    combatant.quickdraw = True
                #Lightning Reload (15th level)
                if combatant.fighter_level >= 15:
                    combatant.lighting_reload = True        
                #Vicious Intent (18th level)
                if combatant.fighter_level >= 18:
                    combatant.vicious_intent = True       
                #Hemorrhaging Critical (20th level)
                if combatant.fighter_level >= 20:
                    combatant.hemorrhaging_critical = True

        if combatant.creature_class == creature_class.Barbarian:
            # Path of the Beserker
            if combatant.creature_subclass == creature_subclass.Beserker:
                # Frenzy (3rd level)
                if combatant.barbarian_level >= 3:
                    combatant.frenzy = True
                # Retaliation (14th level)
                if combatant.barbarian_level >= 14:
                    combatant.retaliation = True
                
        # Racial Features
        # Goliath
        if combatant.race == race.Goliath:        
            combatant.stones_endurance = True
            combatant.stones_endurance_used = False    

        ### monsters###
        if combatant.creature_class == creature_class.Monster:
            if combatant.creature_subclass == creature_subclass.Ancient_Black_Dragon:
                combatant.multiattack = ["Bite","Claw","Claw"]
                combatant.breath_attack = True
                combatant.breath_damage_die = 8
                combatant.breath_range = 90               



def initialise_targets(combatants):
    i = 0
    for i in range(0,len(combatants)):        
        if i > 0:
            prev_combatant = combatants[i-1]
            if combatants[i].name != prev_combatant.name:
                combatants[i].target = prev_combatant
        if i < len(combatants)-1:
            next_combatant = combatants[i+1]
            if combatants[i].name != next_combatant.name:
                combatants[i].target = next_combatant              
    return(combatants)

def init_spell(new_spell,name,min_ss,max_ss,dd,ddc,dt,ddpss,ddcpss,bdd,bddc,bdt):
    new_spell.name = name
    new_spell.min_spell_slot = min_ss
    new_spell.max_spell_slot = max_ss   
    new_spell.damage_die = dd
    new_spell.damage_die_count = ddc
    new_spell.damage_type = dt
    new_spell.damage_die_per_spell_slot = ddpss
    new_spell.damage_die_count_per_spell_slot = ddcpss
    new_spell.bonus_damage_die = bdd
    new_spell.bonus_damage_die_count = bddc
    new_spell.bonus_damage_target = bdt

def characterlevel(combatant):
    return(combatant.barbarian_level + 
           combatant.fighter_level + 
           combatant.rogue_level + 
           combatant.ranger_level +
           combatant.paladin_level)