import random
import math
import operator
from operator import itemgetter, attrgetter, methodcaller

import os,sys
import subprocess
import glob
from os import path    
from enum import Enum, auto

#blocks for containing useful stats/saves
class checkblock():
    str_adv = bool()
    dex_adv = bool()
    con_adv = bool()
    int_adv = bool()
    wis_adv = bool()
    cha_adv = bool()

class saveblock():
    str = int()
    str_adv = bool()
    dex = int()
    dex_adv = bool()
    con = int()
    con_adv = bool()
    intel = int()
    int_adv = bool()
    wis  = int()
    wis_adv = bool()
    cha = int()
    cha_adv = bool()

class statblock():
    str = int()
    dex = int()
    con = int()
    intel = int()
    wis  = int()
    cha = int()

#enumerable creature attributes
class race(Enum):
    def __str__(self):
        return str(self.value)    
    Human = auto()
    Half_Elf = auto()
    Gnome = auto()
    Goliath = auto()
    Dragon = auto()

class creature_class(Enum):
    def __str__(self):
        return str(self.value)    
    Fighter = auto()
    Barbarian = auto()
    Rogue = auto()
    Ranger = auto()
    Monster = auto()
    
class creature_subclass(Enum):
    def __str__(self):
        return str(self.value)    
    #Fighter subclasses
    Gunslinger = auto()
    #Barbarian subclasses
    Beserker = auto()
    #Rogue subclasses
    Thief = auto()
    #Ranger subclasses
    Beastmaster = auto()
    Ancient_Black_Dragon = auto()

class feat(Enum):
    def __str__(self):
        return str(self.value)    
    Sharpshooter = auto()
    Great_Weapon_Master = auto()

#enumerable weapon attributes
class weapon_type(Enum):
    def __str__(self):
        return str(self.value)
    Firearm = auto()
    Axe = auto()
    Sword = auto()
    Natural = auto()

class fighting_style(Enum):
    def __str__(self):
        return str(self.value)
    Archery = auto()
    Defense = auto()
    Dueling = auto()
    Great_Weapon_Fighting = auto()
    Protection = auto()
    Two_Weapon_Fighting = auto()

#enumerable spells (undecided if this is the best way to handle spells)
class spells(Enum):
    def __str__(self):
        return str(self.value)
    CabalsRuin = auto()
    Enlarge = auto()
    Leap = auto()

#various damage types
class damage_type(Enum):
    def __str__(self):
        return str(self.value)
    Piercing = auto()
    Slashing = auto()
    Bludgeoning = auto()
    Fire = auto()
    Cold = auto()
    Lightning = auto()
    Necrotic = auto()
    Radiant = auto()
    Poison = auto()
    Psychic = auto()
    Acid = auto()

# Generic equipment class - used to track item-granted spells and feats
class equipment():
    name = ""
    grants_spell = int()
    max_charges = int()
    current_charges = int()
    damage_die= int()
    damage_type = int()

#Weapon class - used to track weapon damage stats and other properties
class weapon():
    #Core attributes
    name = ""
    weapon_type = int()  
    magic = bool() # Determines if weapon is magic for purposes of damage resistance

    # Properties from handbook 
    martial = bool()
    finesse = bool()
    ammunition = bool()
    heavy = bool()
    light = bool()
    loading = bool()
    range = int()
    reach = int()
    thrown = bool()
    two_handed = bool()
    versatile = bool()
    silvered = bool()

    # Main weapon damage 
    damage_die = int()
    damage_die_count = int()
    weapon_damage_type = int()
    
    # Bonus damage (i.e. 1d6 Necrotic on Blood Axe)
    bonus_damage_die = int()
    bonus_damage_die_count = int()
    bonus_damage_type = int()
    # Special targetted effects (i.e. Dragonslayer Longsword gets 3d6 only against Dragon type)
    bonus_damage_target = int()

    # Magic modifiers (i.e. 2 for +2 weapon)
    magic_to_hit_modifier = int() #also use this on monster attacks (i.e. dragon gets +15 on claw, +8 of which comes from str mod - the rest has no source)
    magic_damage_modifier = int()

    # Firearm-specific properties
    reload = int()
    currentammo = int()
    misfire = int()
    broken = bool()
    ruined = bool()

# Generic class for players and monster entities (called creature to be consistent with rulebook)
class creature():
    # Core properties, common across creatures
    fullname = ""
    name = ""
    race = int()
    creature_class = int()
    creature_subclass = int()
    
    max_health = int()
    current_health = int()    
    armor_class = int()
        
    speed = int()   

    stats = statblock()
    saves = saveblock()
    checks = checkblock()
    
    current_weapon = weapon()

    #Extensible properties (1 to many)
    def creature_feats(self):
        if not hasattr(self, "_creature_feats"):
            self._creature_feats = []
        return self._creature_feats    
       
    def weapon_inventory(self):
        if not hasattr(self, "_weapon_inventory"):
            self._weapon_inventory = [] 
        return self._weapon_inventory

    def weapon_proficiency(self):
        if not hasattr(self, "_weapon_proficiency"):
            self._weapon_proficiency = []
        return self._weapon_proficiency    

    def equipment_inventory(self):
        if not hasattr(self, "_equipment_inventory"):
            self._equipment_inventory = []
        return self._equipment_inventory

    # PC specific - levels in various classes, used to determine which abilities are available
    barbarian_level = int()
    fighter_level = int()    
    fighting_style = int()
    rogue_level = int()
    ranger_level = int()    
    proficiency = int() # Determined by taking the PC's 'primary' class, based on the level - see initgrog for example
    
    #Combat/class/race/feat properties - variety of fields used to track whether abilities can be used, the count remaining for abilities, and other combat info
    # Class
    ## Generic
    extra_attack = int()
    
    ## Fighter
    action_surge = int()
    second_wind = bool()
    
    ## Gunslinger 
    max_grit = int()
    current_grit = int()
    sharpshooter = bool()    
    use_sharpshooter = bool()    

    quickdraw = bool()
    lighting_reload = bool()
    vicious_intent = bool()
    hemorrhaging_critical = bool()
    hemo_damage = int()
    hemo_damage_type = int()
    
    ## Barbarian
    canrage = bool()
    ragedamage = int()
    raging = bool()
    frenzy = bool()
    reckless = bool()        
    great_weapon_master = bool()
    use_great_weapon_master = bool()

    brutal_critical = bool()
    brutal_critical_dice = int()
    relentless_rage = bool()
    relentless_rage_DC = int()
    retaliation = bool()
    feral_instinct = bool()

    # Race
    ## Goliath #    
    stones_endurance = bool()
    stones_endurance_used = bool()

    # NPC properties - specific abilities that are NPC only and require different logic (i.e. multiattack as opposed to Extra Attack)
    multiattack = []
    breath_attack = bool()
    breath_range = int()
    breath_damage_die = int()

    # In-combat properties, reflect status of creature within battle attempt #
    
    position = int() # This flat int is all that's used for tracking distance/position at the moment - needs to be converted to x,y co-ordinate system
    initiative_roll = int() # Used to sort combatants in initiative order
    movement_used = bool() # Tracks if Movement step of turn has been used
    action_used = bool() # Tracks if Action step of turn has been used
    bonus_action_used = bool() # Tracks if Bonus Action step of turn has been used
    reaction_used = bool() # Tracks if Reaction step of turn has been used

    prone = bool() # Tracks if creature is prone (requires half movement to stand)
    alive = bool() # Tracks if creature is still alive

    # Extra-combat properties, reflect status of creature across battle attempts
    no_of_wins = int()

### Core Round functions ###

def movement(combatant):
    # Only move if a target exists
    if combatant.target:
        # movement #
        movement = combatant.speed
        if combatant.prone:
            # Spend half movement to get up #
            movement = math.floor(movement/2)
            print(combatant.name + ' spends ' + repr(movement) + ' feet of movement to stand up from prone ', file=f)            
            combatant.prone = False

        if combatant.current_weapon.range == 0:        
            # melee weapon #            
            if combatant.position > combatant.target.position:  
                # melee target out of range #
                if combatant.position - movement <= combatant.target.position:  
                    # movement can close gap to target # 
                    print(combatant.name + ' uses their movement to engage in melee with ' + combatant.target.name + '!', file=f)            
                    combatant.position = combatant.target.position
                else:
                    # movement cannot close gap to target #
                    print(combatant.name + ' uses their movement to travel ' + repr(movement) + ' feet towards ' + combatant.target.name, file=f)            
                    combatant.position -= movement
        else:
            # range weapon #
            if combatant.position < combatant.target.position and getdistance(combatant.position,combatant.target.position) <= combatant.current_weapon.range:  
                # distance between target, kite #
                if getdistance(combatant.position - movement,combatant.target.position) < combatant.current_weapon.range:  
                    print(combatant.name + ' uses their movement to travel ' + repr(movement) + ' feet away from ' + combatant.target.name, file=f)            
                    combatant.position -= movement
                else:
                    movement = combatant.current_weapon.range - getdistance(combatant.position,combatant.target.position)
                    if movement != 0:
                        print(combatant.name + ' uses part of their movement to travel ' + repr(movement) + ' feet away from ' + combatant.target.name, file=f)            
                        combatant.position -= movement
                    else:
                        print(combatant.name + ' stays where they are.', file=f)
            else:
                print(combatant.name + ' stays where they are.', file=f)            

    combatant.movement_used = True

def action(combatant):
    # Only perform an action if target exists
    if combatant.target:
        # Iterate through equipment and use any available spells (if possible)
        for eq in combatant.equipment_inventory():
            if eq.grants_spell == spells.Enlarge:
                if not combatant.enlarged:
                    print(combatant.name + ' smashes the ' + eq.name + ' together and grows in size!', file=f)            
                    combatant.enlarged = True
                    combatant.action_used = True
        if not combatant.action_used:
            if combatant.current_weapon.range == 0:
                # melee weapon #
                if combatant.position > combatant.target.position:  
                    # melee target out of range - using Action to Dash #
                    movement = combatant.speed
                    print(combatant.name + ' uses the Dash action, travelling towards ' + combatant.target.name, file=f)
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
                # Swap to a different weapon if it makes sense due to range                    
                current_range = getdistance(combatant.position,combatant.target.position)
                # Attempt a weapon swap - change weapons depending on range
                # This will prefer to swap a non-broken or ruined weapon in
                weapon_swap(combatant,current_range)

                # If the weapon is Ruined, and we could not swap to a non-ruined weapon, we're out of luck
                if combatant.current_weapon.ruined:
                    print(combatant.name + ' can\'t do anything with ' + combatant.current_weapon.name + ', it is damaged beyond repair!', file=f)
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
                print(combatant.name + '...would like...to ---RAGE---', file=f)
                combatant.raging = True;
                combatant.bonus_action_used = True

        #Second Wind
        if not combatant.bonus_action_used:
            if combatant.second_wind:
                #Don't use Second Wind unless current HP is more than 10+fighter level less than max
                if combatant.current_health + 10 + combatant.fighter_level < combatant.max_health:
                    second_wind_heal = roll_weapon_die(10) + combatant.fighter_level
                    combatant.current_health += second_wind_heal
                    print(combatant.name + ' uses their Bonus Action to gain a Second Wind, and restores ' + repr(second_wind_heal) + ' hit points!', file=f)
                    combatant.second_wind = False
                    combatant.bonus_action_used = True

        #Frenzy
        if not combatant.bonus_action_used:
            if combatant.raging:
                if combatant.frenzy:            
                    if combatant.position == combatant.target.position:
                        print(combatant.name + ' uses their Bonus Action to make a frenzied weapon attack against ' + combatant.target.name, file=f)
                        attack(combatant)            
                        combatant.bonus_action_used = True
                        
        #Boots of Feral Leaping        
        if not combatant.bonus_action_used:
            for item in combatant.equipment_inventory():
                if item.grants_spell == spells.Leap:
                    if combatant.position != combatant.target.position:
                        print(combatant.name + ' is taking a flying leap using his ' + item.name + ' as a Bonus Action!', file=f)
                        if abilitycheck(combatant,"Strength",strmod(combatant),combatant.checks.str_adv,16):
                            print(combatant.name + ' leaps forward 20 feet', file=f)
                            if combatant.position - 20 <= combatant.target.position:
                                #movement can close gap to target # 
                                combatant.position = combatant.target.position
                            else:
                                #movement cannot close gap to target #
                                combatant.position -= 20
                        else:
                            print(combatant.name + ' fell over where he stands!', file=f)
                            combatant.prone = True
                        combatant.bonus_action_used = True

        #Lightning Reload
        if not combatant.bonus_action_used:
            if combatant.current_weapon.weapon_type == weapon_type.Firearm:
                if combatant.lighting_reload:
                    if combatant.current_weapon.currentammo == 0:
                        combatant.current_weapon.currentammo = combatant.current_weapon.reload
                        print(combatant.name + ' used a bonus action to reload.', file=f)
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
                # prefer melee weapon for melee range
            (weap.range == 0 and current_range == 0)):         
                # Don't swap if we're already using this weapon
                if combatant.current_weapon != weap:
                    # Draw ruined and cry if current weapon is ruined - making it here means there are no better options
                    if weap.ruined and (combatant.current_weapon.ruined):
                        print(combatant.name + ' sadly puts away ' + combatant.current_weapon.name + ' and draws out the ruined ' + weap.name,file=f)                        
                        combatant.current_weapon = weap                    
                        return True
                    # Draw broken if we have to (i.e. current weapon is broken/ruined, and we need to repair the better one)                    
                    if weap.broken and (combatant.current_weapon.broken or combatant.current_weapon.ruined):  
                        print('Frustrated, ' + combatant.name + ' stows ' + combatant.current_weapon.name + ' and draws out the broken ' + weap.name,file=f)                        
                        combatant.current_weapon = weap                    
                        return True
                    # If the weapon is neither broken nor ruined, and it makes it here, it's the best choice
                    if not weap.ruined and not weap.broken:
                        print('With a flourish, ' + combatant.name + ' stows ' + combatant.current_weapon.name + ' and draws out ' + weap.name,file=f)                        
                        combatant.current_weapon = weap                    
                        return True                                            
    # No weapon is equipped; draw one
    else:
        for weap in combatant.weapon_inventory():    
            print(combatant.name + ' draws ' + weap.name + ' and prepares for battle!',file=f)
            combatant.current_weapon = weap                    
            return True
    return False

#Attack action
def attack_action(combatant):
    #one set of rules for monsters
    if combatant.creature_class == creature_class.Monster:
        if combatant.breath_attack and (combatant.breath_range >= getdistance(combatant.position,combatant.target.position)):
            print(combatant.name + ' rears back and unleashes a devastating breath attack!', file=f)                
            breath_attack(combatant)
        else:
            if combatant.multiattack:
                print(combatant.name + ' unleashes a Multiattack against ' + combatant.target.name, file=f)                
                for ma in combatant.multiattack:
                    for weap in combatant.weapon_inventory():
                        if ma == weap.name:                        
                            combatant.current_weapon = weap
                            attack(combatant)
            else:
                print(combatant.name + ' uses the Attack action against ' + combatant.target.name, file=f)                
                attack(combatant)    
    else:
        print(combatant.name + ' uses the Attack action against ' + combatant.target.name, file=f)                
        attack(combatant)

        if combatant.extra_attack > 0:
            for x in range(0,combatant.extra_attack):
                #Can't attack if weapon is broken, must spend next action to fix it
                if not combatant.current_weapon.broken:
                    print(combatant.name + ' uses an Extra Attack.', file=f)
                    attack(combatant)  

def breath_attack(combatant):
    breath_damage = 0
    breath_damage_type = 0
    die_damage = 0
    if combatant.creature_subclass == creature_subclass.Ancient_Black_Dragon:
        breath_damage_type = damage_type.Acid
        i = 1
        for i in range(1,15):
            die_damage = roll_weapon_die(combatant.breath_damage_die)
            print(combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.breath_damage_die) + ' (Breath Damage)', file=f)
            breath_damage += die_damage
    if savingthrow(combatant.target,"Dexterity",dexmod(combatant.target),combatant.target.saves.dex_adv,23):
        deal_damage(combatant.target,breath_damage/2,breath_damage_type,True)
    else:
        deal_damage(combatant.target,breath_damage,breath_damage_type,True)

    combatant.breath_attack = False

    #See if the damage droped target below 0 hp
    resolve_fatality(combatant.target)

def breath_recharge(combatant):    
    die = roll_weapon_die(6)
    if die >= 5:
        print(combatant.name + ' rolled a ' + repr(die) + ' on a d6 and recharged their Breath Attack!', file=f)
        combatant.breath_attack = True
    else:
        print(combatant.name + ' rolled a ' + repr(die) + ' on a d6 and did not recharge their Breath Attack.', file=f)

#Attack resolution
def attack(combatant):    
    #Only attack with a weapon
    if combatant.current_weapon.name != "":
    
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
                        print(combatant.name + ' can\'t do anything with ' + combatant.current_weapon.name + ', it is damaged beyond repair!', file=f)
                        attackcomplete = True
            
                if not attackcomplete:
                    if combatant.current_weapon.currentammo == 0:
                        # reload weapon # 
                        if combatant.bonus_action_used:
                            print(combatant.name + ' used their attack to reload ' + combatant.current_weapon.name, file=f)
                            combatant.current_weapon.currentammo = combatant.current_weapon.reload
                            attackcomplete = True
                        else:
                            #Use Lightning Reflexes to bonus action reload
                            print(combatant.name + ' used their Bonus Action to reload ' + combatant.current_weapon.name, file=f)
                            combatant.current_weapon.currentammo = combatant.current_weapon.reload
                            combatant.bonus_action_used = True

                if not attackcomplete:
                    # check to spend grit for trick shot if available #
                    if combatant.current_grit > 0:
                        # legs trick shot #
                        # don't bother if target is already prone #
                        if combatant.target.prone:
                            #print(combatant.target.name + ' is prone on the ground - ' + combatant.name + ' is saving his Grit for later', file=f)
                            disadvantage = True
                        else:
                            print(combatant.name + ' spends 1 Grit Point to perform a Leg Trick Shot. Current Grit: ' + repr(combatant.current_grit-1), file=f)
                            combatant.current_grit -= 1
                            calledshot = True

                #Check condition of target
                if not attackcomplete:
                    if combatant.target.prone:
                        print(combatant.target.name + ' is prone on the ground, giving ' + combatant.name + ' disadvantage on the attack!', file=f)
                        disadvantage = True

                if not attackcomplete:
                    #Modifier conditions (i.e. GWM, sharpshooter)        
                    if combatant.sharpshooter:
                        if (combatant.target.armor_class < to_hit_modifier+5) and not disadvantage:
                            print(combatant.name + ' uses Sharpshooter, taking a penalty to the attack', file=f)
                            combatant.use_sharpshooter = True           
                        else:
                            combatant.use_sharpshooter = False
        
            #Great Weapon Master
            if combatant.current_weapon.heavy and combatant.great_weapon_master:
                if (combatant.target.armor_class < to_hit_modifier+5) and not disadvantage:
                    print(combatant.name + ' uses Great Weapon Master, taking a penalty to the attack', file=f)
                    combatant.use_great_weapon_master = True
            
            #Advnatage/disadvnatage conditions (not weapon specific)
            if combatant.reckless:
                print(combatant.name + ' uses Reckless Attack, gaining advantage on the strike', file=f)
                advantage = True

            if combatant.target.reckless and combatant.current_weapon.range == 0:
                advantage = True

            # Make attack roll # 
            if not attackcomplete:
                initroll = roll_d20()
                if advantage and disadvantage:
                    atkroll = initroll
                if advantage and not disadvantage:
                    #print(combatant.name + ' has advantage on the attack', file=f)
                    advroll = roll_d20()
                    atkroll = max(initroll,advroll)
                if disadvantage and not advantage:
                    #print(combatant.name + ' has disadvantage on the attack', file=f)
                    disadvroll = roll_d20()
                    atkroll = min(initroll,disadvroll)
                if not advantage and not disadvantage:
                    atkroll = initroll
            
                print(combatant.name + ' rolled a ' + repr(atkroll) + ' on a d20 (attack)', file=f)

                # After-roll weapon features
                if combatant.current_weapon.weapon_type == weapon_type.Firearm:
                    if combatant.current_weapon.misfire >= atkroll:
                        # weapon misfire, attack fail #
                        print(combatant.name + 's attack misfired with a natural ' + repr(atkroll) + '! ' + combatant.current_weapon.name + ' is now broken!', file=f)
                        combatant.current_weapon.broken = True
                        attackcomplete = True


            # Resolve attack
            if not attackcomplete:
                totalatk = atkroll + to_hit_modifier;

                crit = False
                track_hemo = False
                if atkroll >= calc_min_crit(combatant):
                    crit = True
                    print('************************', file=f)
                    print('It\'s a CRITICAL ROLE!!!', file=f)
                    print('************************', file=f)

                dice_damage = 0
                weapon_damage_type = damage_type.Bludgeoning
                bonus_dice_damage = 0
                bonus_damage_type = damage_type.Bludgeoning
                equipment_damage = 0
                equipment_damage_type = 0

                #Resolve sharpshooter/great weapon master
                if combatant.use_sharpshooter:                
                    totalatk = totalatk-5

                if combatant.use_great_weapon_master:
                    totalatk = totalatk-5

                if totalatk >= combatant.target.armor_class:
                    print(combatant.name + '\'s attack with ' + combatant.current_weapon.name + ' on ' + combatant.target.name + ' hit! (' + repr(totalatk) + ' versus AC ' + repr(combatant.target.armor_class) + ')', file=f)            
                    # resolve trick shot #
                    if calledshot:
                        # logic to choose the right kind of called shot? lol #
                        print('Resolving called shot...', file=f)
                        if savingthrow(combatant.target,"Strength",strmod(combatant.target),combatant.target.saves.str_adv,8+combatant.proficiency + dexmod(combatant)):
                            print(combatant.target.name + ' succeeded on the Leg Shot save, and remains standing', file=f)
                        else:
                            print(combatant.target.name + ' failed the Leg Shot save - they are now prone!', file=f)
                            combatant.target.prone = True

                    print('Rolling damage...', file=f)

                    #Great Weapon Fighting (reroll 1s and 2s)
                    greatweaponfighting = False
                    if combatant.fighting_style == fighting_style.Great_Weapon_Fighting and combatant.current_weapon.heavy:
                        greatweaponfighting = True

                    weapon_damage_type = damage_type(combatant.current_weapon.weapon_damage_type)
                    for x in range(0,combatant.current_weapon.damage_die_count):                                    
                        die_damage = roll_weapon_die(combatant.current_weapon.damage_die)   
                        print(combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.current_weapon.damage_die) + ' (Weapon Damage)', file=f)
                        if greatweaponfighting and die_damage <= 2:
                            print(combatant.name + ' rerolled a weapon die due to Great Weapon Fighting!', file=f)
                            die_damage = roll_weapon_die(combatant.current_weapon.damage_die)   
                            print(combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.current_weapon.damage_die) + ' (Weapon Damage)', file=f)    
                        dice_damage += die_damage                    
                     
                    if crit:
                        dice_damage = dice_damage * 2
                        # restore grit on critical # 
                        if combatant.current_grit < combatant.max_grit:
                            print(combatant.name + ' regained 1 grit point for scoring a critical hit!', file=f)
                            combatant.current_grit = combatant.current_grit + 1;
                    
                        #Brutal Critical feature
                        if combatant.brutal_critical:
                            print(combatant.name + ' scored a Brutal Critical! Rolling an additional ' + repr(combatant.brutal_critical_dice) + ' d' + repr(combatant.current_weapon.damage_die), file=f)
                            for x in range(0,combatant.brutal_critical_dice):                            
                                die_damage = roll_weapon_die(combatant.current_weapon.damage_die)            
                                print(combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.current_weapon.damage_die) + ' (Brutal Critical damage)', file=f)
                                if greatweaponfighting and die_damage <= 2:
                                    print(combatant.name + ' rerolled a weapon die due to Great Weapon Fighting!', file=f)                                           
                                    die_damage = roll_weapon_die(combatant.current_weapon.damage_die)            
                                dice_damage += die_damage              
                            
                        #Hemorraghing Critical feature
                        if combatant.hemorrhaging_critical and combatant.current_weapon.weapon_type == weapon_type.Firearm:
                            print(combatant.name + ' scored a Hemorraghing Critical!', file=f)
                            #Set boolean to track and increase hemo damage (possible multiple crits per round)
                            track_hemo = True                        

                    damage_modifier = calc_damage_modifier(combatant)
                
                    if combatant.use_sharpshooter:
                        damage_modifier = damage_modifier + 10
                        print(combatant.name + ' dealt extra damage because of Sharpshooter', file=f)

                    if combatant.use_great_weapon_master:
                        damage_modifier = damage_modifier + 10
                        print(combatant.name + ' dealt extra damage because of Great Weapon Master', file=f)
                
                    totaldamage = dice_damage + damage_modifier             
                    print(combatant.name + ' dealt a total of ' + repr(totaldamage) + ' points of ' + weapon_damage_type.name + ' damage (dice damage: ' + repr(dice_damage) + ' modifier: ' + repr(damage_modifier) + ')', file=f)
                    deal_damage(combatant.target,totaldamage,weapon_damage_type,combatant.current_weapon.magic)
                
                    if track_hemo:
                        print(combatant.name + ' adds an extra ' + repr(int(totaldamage/2)) + ' damage via Hemorrhaging Critical, which will be dealt at the end of ' + combatant.target.name + '\'s turn.',file=f)
                        combatant.target.hemo_damage += int(totaldamage/2)
                        combatant.hemo_damage_type = weapon_damage_type
                        track_hemo = False

                    if combatant.current_weapon.bonus_damage_die > 0:
                        # Apply bonus damage selectively 
                        if (combatant.current_weapon.bonus_damage_target == 0) or (combatant.current_weapon.bonus_damage_target == combatant.target.race):
                            bonus_damage_type = damage_type(combatant.current_weapon.bonus_damage_type)
                            for x in range(0,combatant.current_weapon.bonus_damage_die_count):
                                die_damage = roll_weapon_die(combatant.current_weapon.bonus_damage_die)
                                print(combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.current_weapon.bonus_damage_die) + ' (Bonus Damage)', file=f)
                                if greatweaponfighting and die_damage <= 2:
                                    print(combatant.name + ' rerolled a weapon die due to Great Weapon Fighting!', file=f)
                                    die_damage = roll_weapon_die(combatant.current_weapon.bonus_damage_die)
                                    print(combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(combatant.current_weapon.bonus_damage_die) + ' (Bonus Damage)', file=f)
                                bonus_dice_damage += die_damage
                                if crit:
                                    bonus_dice_damage = bonus_dice_damage * 2
                        
                        print(combatant.name + ' dealt an additional ' + repr(bonus_dice_damage) + ' points of ' + bonus_damage_type.name + ' damage with ' + combatant.current_weapon.name, file=f)
                        deal_damage(combatant.target,bonus_dice_damage,bonus_damage_type,combatant.current_weapon.magic)

                    #Cabal's Ruin
                    #Only use cabal's on a crit, dump all charges
                    if crit:
                        for eq in combatant.equipment_inventory():
                            if eq.grants_spell == spells.CabalsRuin:                              
                                equipment_damage_type = eq.damage_type
                                if eq.current_charges > 0:
                                    print(combatant.name + ' activates ' + eq.name + ', pouring ' +  repr(eq.current_charges) + ' charges into ' + combatant.target.name + '!', file=f)
                                    for x in range(0,eq.current_charges):
                                        die_damage = roll_weapon_die(eq.damage_die)                                
                                        equipment_damage += die_damage * 2         
                                        print(combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(eq.damage_die) + ' (Cabal\'s Ruin damage)', file=f)
                                    eq.current_charges = 0                
                                    print(combatant.name + ' dealt an additional ' + repr(equipment_damage) + ' points of ' + equipment_damage_type.name + ' damage with ' + eq.name, file=f)
                                    deal_damage(combatant.target,equipment_damage,equipment_damage_type,True)
                
                    #See if the damage droped target below 0 hp
                    resolve_fatality(combatant.target)
                else:
                    print(combatant.name + '\'s attack on ' + combatant.target.name + ' MISSED! (' + repr(totalatk) + ' versus AC ' + repr(combatant.target.armor_class) + ')', file=f)            

                # consume ammo after shot #
                if combatant.current_weapon.reload > 0:
                    combatant.current_weapon.currentammo = combatant.current_weapon.currentammo - 1            

                attackcomplete = True
        else:
            print(combatant.target.name + ' is unconscious!', file=f)

def repair_weapon(combatant):
    print(combatant.name + ' attempts to repair ' + combatant.current_weapon.name, file=f)    
    if abilitycheck(combatant,"Dexterity",dexmod(combatant)+combatant.proficiency,False,10+combatant.current_weapon.misfire):  
        print(combatant.name + ' successfully repaired ' + combatant.current_weapon.name, file=f)
        combatant.current_weapon.broken = False
    else:
        combatant.current_weapon.broken = True
        combatant.current_weapon.ruined = True
        print(combatant.current_weapon.name + ' has been ruined in the repair attempt! ' + combatant.name + ' needs to go back to their workshop to fix it! ', file=f)

def deal_damage(combatant,damage,weapon_damage_type,magical):    
    #Reduce bludgeoning/piercing/slashing if raging
    if combatant.raging:            
        if weapon_damage_type in (damage_type.Piercing,damage_type.Bludgeoning,damage_type.Slashing):
            damage = int(damage/2)              
            print(combatant.name + ' shrugs off ' + repr(damage) + ' points of damage in his rage!', file=f)
    if combatant.enlarged:
        if weapon_damage_type in (damage_type.Fire,damage_type.Cold,damage_type.Lightning):
            damage = int(damage/2)              
            print(combatant.name + ' shrugs off ' + repr(damage) + ' points of damage due to the effects of Enlarge!', file=f)

    #Reduce bludgeoning/piercing/slashing if dealt by non-magical weapon
    if combatant.creature_subclass == creature_subclass.Ancient_Black_Dragon:            
        if weapon_damage_type in (damage_type.Piercing,damage_type.Bludgeoning,damage_type.Slashing) and not magical:
            damage = int(damage/2)              
            print(combatant.name + ' shrugs off ' + repr(damage) + ' points of damage from the non-magical attack!', file=f)

    #Use Reaction if it can do anything
    if not combatant.reaction_used:
        if combatant.stones_endurance:
            if not combatant.stones_endurance_used:
                #Don't waste stones endurance on small hits
                if damage > conmod(combatant)+12:
                    reduction = conmod(combatant) + roll_weapon_die(12)
                    damage = int(damage - reduction)
                    print(combatant.name + ' uses their reaction, and uses Stones Endurance to reduce the damage by ' + repr(reduction) + '! ', file=f)
                    combatant.stones_endurance_used = True
                    combatant.reaction_used = True

    if damage > 0:
        combatant.current_health = combatant.current_health - damage
        print(combatant.name + ' suffers a total of ' + repr(int(damage)) + ' points of ' + weapon_damage_type.name + ' damage. Current HP: ' + repr(int(combatant.current_health)) + '/' + repr(combatant.max_health), file=f)    
 
def resolve_fatality(combatant):
    if combatant.current_health <= 0:
        #Relentless rage
        if combatant.relentless_rage:
            if savingthrow(combatant,"Constitution",combatant.saves.con,False,combatant.relentless_rage_DC):
                print(combatant.name + ' was dropped below 0 hit points, but recovers to 1 hit point due to his Relentless Rage!', file=f)
                combatant.alive = True
                combatant.current_health = 1
                combatant.relentless_rage_DC += 5
            else:                
                print('The relentless fury within ' + combatant.name + '\'s eyes fades, and he slumps to the ground, unconscious.', file=f)
                combatant.alive = False      
                combatant.relentless_rage = False
        else:            
            combatant.alive = False                    
    if not combatant.alive:
        print('HOW DO YOU WANT TO DO THIS??', file=f)        

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
    if combatant.raging:
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
    #print(savetype + ' save: Natural roll: ' + repr(roll) + ', modifier: ' + repr(modifier), file=f)
    if savingthrow >= DC:
        print(combatant.name + ' made a ' + savetype + ' save against a DC of ' + repr(DC) + ' with a saving throw of ' + repr(savingthrow), file = f)
        return True
    if adv:
        #print(combatant.name + ' failed the save, but has advantage on ' + savetype + ' saving throws!', file=f)
        roll = roll_d20()
        savingthrow = roll + modifier
        #print(savetype + ' save: Natural roll: ' + repr(roll) + ', modifier: ' + repr(modifier), file=f)        
        if savingthrow >= DC:
            print(combatant.name + ' made a ' + savetype + ' save against a DC of ' + repr(DC) + ' with a saving throw of ' + repr(savingthrow), file = f)
            return True
    print(combatant.name + ' failed the ' + savetype + ' save with a saving throw of ' + repr(savingthrow) + ' versus DC ' + repr(DC), file=f)
    return False

# check functions #
def abilitycheck(combatant,checktype,modifier,adv,DC):
    roll = roll_d20()
    check = roll + modifier
    if DC == 0:
        return(check)

    #print(checktype + ' check: Natural roll: ' + repr(roll) + ', modifier: ' + repr(modifier), file=f)    
    if check >= DC:
        print(combatant.name + ' succeeded on a DC ' + repr(DC) + ' ' + checktype + ' check with a total of ' + repr(check), file = f)
        return True
    if adv:
        #print(combatant.name + ' failed the check, but has advantage on ' + checktype + ' checks!', file=f)
        roll = roll_d20()
        check = roll + modifier
        #print(checktype + ' check: Natural roll: ' + repr(roll) + ', modifier: ' + repr(modifier), file=f)    
        if check >= DC:
            print(combatant.name + ' succeeded on a DC ' + repr(DC) + ' ' + checktype + ' check with a total of ' + repr(check), file = f)
            return True
    print(combatant.name + ' FAILED on a DC ' + repr(DC) + ' ' + checktype + ' check with a total of ' + repr(check), file = f)
    return False


#combat initialisation

def initialise_combatants(init_combatants):
    initpercy(init_combatants)
    #initgrog(init_combatants)
    initumbrasyl(init_combatants)

def initialise_combat_round(init_combatants):
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
            combatant.extra_attack += 1
        # Extra Attack (+1 at 11th level)
        if combatant.fighter_level >= 11:
            combatant.extra_attack += 1
        # Extra Attack (+1 at 20th level)
        if combatant.fighter_level >= 20:
            combatant.extra_attack += 1
        
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
        # Danger Sense (2nd level)
        if combatant.barbarian_level >= 2:
            combatant.saves.dex_adv = True                
        # Extra Attack (+1 at 5th level)
        if combatant.barbarian_level >= 5:
            combatant.extra_attack += 1
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
        
            
        # Specific abilities (primary class/subclass must be defined)
        #Gunslinger (examine profiencies for Firearm proficiency, use fighter levels to determine abilities)
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

def initialise_position(combatants):
    for combatant in combatants:
        if combatant.name == "Grog":
            combatant.position = 1200
        if combatant.name == "Percy":
            combatant.position = 1000
        if combatant.name == "Umbrasyl":
            combatant.position = 1400

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

# helper functions #

def initpercy(init_combatants):
#Percival
    percy = creature()
    percy.fullname = "Percival Fredrickstein Von Musel Klossowski De Rolo III"
    percy.name = "Percy"
    percy.race = race.Human
    percy.creature_class = creature_class.Fighter
    percy.creature_subclass = creature_subclass.Gunslinger
    percy.fighter_level = 20
    percy.fighting_style = fighting_style.Archery
    percy.max_health = 149
    percy.armor_class = 18
    percy.speed = 30
    percy.proficiency = math.floor((7+percy.fighter_level)/4)
    percy.weapon_proficiency().append(weapon_type.Firearm)
    percy.weapon_proficiency().append(weapon_type.Sword)
        
    percy.creature_feats().append(feat.Sharpshooter)
    

    #Stats
    percystats = statblock()    
    percystats.str = 12
    percystats.dex = 22
    percystats.con = 14
    percystats.intel = 20
    percystats.wis = 16
    percystats.cha = 14

    percy.stats = percystats

    #Saves
    percysaves = saveblock()
    
    percy.saves = percysaves

    #Ability checks
    percychecks = checkblock()
    
    percy.checks = percychecks

    #Percy's weapons
    #Bad News
    badnews = weapon()
    badnews.name = "Bad News"
    badnews.weapon_type = weapon_type.Firearm;
    badnews.range = 1200

    badnews.damage_die = 12
    badnews.damage_die_count = 2
    badnews.weapon_damage_type = damage_type.Piercing

    badnews.reload = 1
    badnews.currentammo = 1
    badnews.misfire = 3
    
    badnews.finesse = True
    badnews.magic = False

    percy.weapon_inventory().append(badnews)

    #Animus
    animus = weapon()
    animus.name = "Animus"
    animus.weapon_type = weapon_type.Firearm
    animus.range = 600

    animus.damage_die = 10
    animus.damage_die_count = 1
    animus.weapon_damage_type = damage_type.Piercing

    animus.bonus_damage_die = 6
    animus.bonus_damage_die_count = 1
    animus.bonus_damage_type = damage_type.Psychic
    
    animus.magic_to_hit_modifier = 0
    animus.magic_damage_modifier = 6

    animus.reload = 6
    animus.currentammo = 6
    animus.misfire = 2
    
    animus.finesse = True
    animus.magic = True

    percy.weapon_inventory().append(animus)    

    #dragonslayer longsword
    dragonslayer_longsword = weapon()

    dragonslayer_longsword.name = "Dragonslayer Longsword"
    dragonslayer_longsword.weapon_type = weapon_type.Sword
    
    dragonslayer_longsword.range = 0
    dragonslayer_longsword.damage_die = 8
    dragonslayer_longsword.damage_die_count = 1
    dragonslayer_longsword.weapon_damage_type = damage_type.Slashing

    dragonslayer_longsword.bonus_damage_die = 6
    dragonslayer_longsword.bonus_damage_die_count = 3
    dragonslayer_longsword.bonus_damage_type = damage_type.Slashing
    dragonslayer_longsword.bonus_damage_target = race.Dragon

    dragonslayer_longsword.magic_to_hit_modifier = 1
    dragonslayer_longsword.magic_damage_modifier = 1

    dragonslayer_longsword.light = True
    dragonslayer_longsword.finesse = True
    dragonslayer_longsword.magic = True

    percy.weapon_inventory().append(dragonslayer_longsword)

    #Percy's gear
    cabalsruin = equipment()
    cabalsruin.name = "Cabal\'s Ruin"
    cabalsruin.grants_spell = spells.CabalsRuin
    cabalsruin.max_charges = 9
    cabalsruin.current_charges = 0
    cabalsruin.damage_die = 6
    cabalsruin.damage_type = damage_type.Lightning    

    percy.equipment_inventory().append(cabalsruin)

    # add combatants to array
    init_combatants.append(percy)

def initgrog(init_combatants):

    #GROG
    grog = creature()
    grog.fullname = "Grog Strongjaw"
    grog.name = "Grog"
    grog.race = race.Goliath
    grog.creature_class = creature_class.Barbarian
    grog.creature_subclass = creature_subclass.Beserker    
    grog.barbarian_level = 17
    grog.fighter_level = 3
    grog.fighting_style = fighting_style.Great_Weapon_Fighting
    grog.max_health = 248
    grog.armor_class = 17
    grog.speed = 50
    grog.proficiency = math.floor((7+grog.barbarian_level)/4)
    grog.weapon_proficiency().append(weapon_type.Axe)

    grog.creature_feats().append(feat.Great_Weapon_Master)

    #Stats
    grogstats = statblock()
    grogstats.str = 26
    grogstats.dex = 15
    grogstats.con = 20
    grogstats.intel = 6
    grogstats.wis = 10
    grogstats.cha = 8

    grog.stats = grogstats
    
    #Saves
    grogsaves = saveblock()    
    grogsaves.str = 14
    grogsaves.str_adv = True
    grogsaves.dex = 2
    grogsaves.dex_adv = False
    grogsaves.con = 11
    grogsaves.con_adv = False
    grogsaves.intel = -2
    grogsaves.int_adv = False
    grogsaves.wis = 0
    grogsaves.wis_adv = False
    grogsaves.cha = 1
    grogsaves.cha_adv = False
    
    grog.saves = grogsaves

    #Ability Checks
    grogchecks = checkblock()
    grogchecks.str_adv = True

    grog.checks = grogchecks    

    #Grog's weapons
    bloodaxe = weapon()
    bloodaxe.name = "Blood Axe"
    bloodaxe.weapon_type = weapon_type.Axe;
    bloodaxe.range = 0
    
    bloodaxe.damage_die = 12
    bloodaxe.damage_die_count = 1
    bloodaxe.weapon_damage_type = damage_type.Slashing
    
    bloodaxe.bonus_damage_die = 6
    bloodaxe.bonus_damage_die_count = 1
    bloodaxe.bonus_damage_type = damage_type.Necrotic
    
    bloodaxe.magic_to_hit_modifier = 2
    bloodaxe.magic_damage_modifier = 2

    bloodaxe.heavy = True
    bloodaxe.two_handed = True
    bloodaxe.magic = True

    grog.weapon_inventory().append(bloodaxe)

    #Grog's gear
    
    titanstoneknuckles = equipment()
    titanstoneknuckles.name = "Titanstone Knuckles"
    titanstoneknuckles.grants_spell = spells.Enlarge    

    grog.equipment_inventory().append(titanstoneknuckles)

    bootsofferalleaping = equipment()
    bootsofferalleaping.name = "Boots of Feral Leaping"
    bootsofferalleaping.grans_spell = spells.Leap

    grog.equipment_inventory().append(bootsofferalleaping)

    # combat stats # 

    init_combatants.append(grog)    

def initumbrasyl(init_combatants):

    umbrasyl = creature()
    umbrasyl.fullname = "Umbrasyl"
    umbrasyl.name = "Umbrasyl"
    umbrasyl.race = race.Dragon
    umbrasyl.creature_class = creature_class.Monster
    umbrasyl.creature_subclass = creature_subclass.Ancient_Black_Dragon
    umbrasyl.max_health = 640
    umbrasyl.armor_class = 22
    umbrasyl.speed = 40
        
    #Stats
    umbrasylstats = statblock()
    umbrasylstats.str = 27
    umbrasylstats.dex = 14
    umbrasylstats.con = 25
    umbrasylstats.intel = 16
    umbrasylstats.wis = 15
    umbrasylstats.cha = 19

    umbrasyl.stats = umbrasylstats
    
    #Saves
    umbrasylsaves = saveblock()    
    umbrasylsaves.str = 14
    umbrasylsaves.str_adv = True
    umbrasylsaves.dex = 9
    umbrasylsaves.dex_adv = False
    umbrasylsaves.con = 14
    umbrasylsaves.con_adv = False
    umbrasylsaves.intel = 0
    umbrasylsaves.int_adv = False
    umbrasylsaves.wis = 9
    umbrasylsaves.wis_adv = False
    umbrasylsaves.cha = 11
    umbrasylsaves.cha_adv = False
    
    umbrasyl.saves = umbrasylsaves

    #Ability Checks
    umbrasylchecks = checkblock()
    umbrasylchecks.str_adv = True

    umbrasyl.checks = umbrasylchecks

    #Umbrasyl's weapons
    bite = weapon()
    bite.name = "Bite"
    bite.weapon_type = weapon_type.Natural;
    bite.range = 0
    
    bite.damage_die = 10
    bite.damage_die_count = 2
    bite.weapon_damage_type = damage_type.Piercing
    
    bite.bonus_damage_die = 8
    bite.bonus_damage_die_count = 2
    bite.bonus_damage_type = damage_type.Acid   

    bite.reach = 15
    
    bite.magic_to_hit_modifier = 7

    umbrasyl.weapon_inventory().append(bite)
    
    claw = weapon()
    claw.name = "Claw"
    claw.weapon_type = weapon_type.Natural;
    claw.range = 0
    
    claw.damage_die = 6
    claw.damage_die_count = 2
    claw.weapon_damage_type = damage_type.Slashing
        
    claw.reach = 10
    
    claw.magic_to_hit_modifier = 7

    umbrasyl.weapon_inventory().append(claw)

    tail = weapon()
    tail.name = "Tail"
    tail.weapon_type = weapon_type.Natural;
    tail.range = 0
    
    tail.damage_die = 8
    tail.damage_die_count = 2
    tail.weapon_damage_type = damage_type.Bludgeoning
        
    tail.reach = 20

    umbrasyl.weapon_inventory().append(tail)

    init_combatants.append(umbrasyl)    


def getdistance(combatantpos,targetpos):
    return int(math.fabs(combatantpos-targetpos))

def printdetails(combatant,position):
    print('Position: ' + repr(position), file=f) 
    print(' Name: '  + combatant.fullname, file=f)
    print(' Race: '  + combatant.race.name, file=f)
    print(' Class: '  + combatant.creature_class.name, file=f)
    print(' Sub-class: '  + combatant.creature_subclass.name, file=f)
    print(' --------------------------------' , file=f)
    print(' Stats: ',file=f)
    print(' Strength: ' + repr(combatant.stats.str),file=f)
    print(' Dexterity: ' + repr(combatant.stats.dex),file=f)
    print(' Constitution: ' + repr(combatant.stats.con),file=f)
    print(' Intelligence: ' + repr(combatant.stats.intel),file=f)
    print(' Wisdom: ' + repr(combatant.stats.wis),file=f)
    print(' Charisma: ' + repr(combatant.stats.cha),file=f)
    print('',file=f)            
    print(' Weapon Proficiencies: ',file=f)
    for item in combatant.weapon_proficiency():
        print(' Weapon Proficiency: ' + item.name,file=f)
    print('',file=f)
    print('',file=f)
    print(' Equipped Weapon: ' + combatant.current_weapon.name,file=f)
    print(' Other Weapons: ',file=f)
    for item in combatant.weapon_inventory():
        print(' Weapon: ' + item.name,file=f)
    print('',file=f)
    print(' Other Equipment: ',file=f)
    for item in combatant.equipment_inventory():                
        print(' Item: ' + item.name,file=f)
    print('',file=f)
    print('---------------------------------',file=f)
        
# start # 
import time
import datetime
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H%M%S')
filename = "C:\stuff\combatlog2"

with open(filename + st + ".txt", 'a') as f:
    
    # engage #
    init_combatants = []
    initialise_combatants(init_combatants)
    
    attempt=0
    while attempt < 100:
        
        print('_____________________________________________________________________________', file=f)
        attempt += 1
        print('Attempt number:' + repr(attempt),file=f)
        print(' ', file=f)      

        initialise_combat_round(init_combatants)

        # Hard-coded initialisation functions for Percy v Grog

        initialise_position(init_combatants)
        initialise_targets(init_combatants)          

        combatantdead = False

        # roll initiative #
        print('Rolling initiative...', file=f)
        for combatant in init_combatants:                        
            initiativeroll = abilitycheck(combatant,"Dexterity",dexmod(combatant),False,0)            
            if combatant.feral_instinct:
                initiativeroll_adv = abilitycheck(combatant,"Dexterity",dexmod(combatant),True,0)
                initiativeroll = max(initiativeroll,initiativeroll_adv)
            if combatant.quickdraw:
                initiativeroll += combatant.proficiency
            combatant.initiative_roll = initiativeroll
            
            print(combatant.name + ' rolled a total of ' + repr(combatant.initiative_roll) + '. They are located at co-ordinates: ' + repr(combatant.position), file=f)
            #If the combatant has a valid target, equip a weapon
            if combatant.target:
                weapon_swap(combatant,getdistance(combatant.position,combatant.target.position))
                    #print('ERROR: ' + combatant.name + ' has no valid weapons to draw. They will be unable to partake in combat.',file=f)


            initkey = operator.attrgetter("initiative_roll")

            combatants = sorted(init_combatants, key=initkey,reverse=True)
        
        #Print out combat order at top of attempt
        print('')
        print('Combat order: ', file=f)
        combatorder = 0
        for combatant in combatants:                     
            combatorder += 1
            printdetails(combatant,combatorder)
            
        #Begin combat rounds (up to a maximum to avoid overflow)
        round = 0        
        while not combatantdead and round < 1000:
            print('', file=f)
            round = round + 1
            print('Round: ' + repr(round), file=f)
    
            for combatant in combatants:        
                if not combatantdead:
                    if combatant.alive:
                        print('It is now ' + combatant.name + '\'s turn. Current HP: ' + repr(combatant.current_health) + '/' + repr(combatant.max_health), file=f)
                        combatant.movement_used = False
                        combatant.action_used = False
                        combatant.bonus_action_used = False
                        combatant.reaction_used = False

                        #print(combatant.name + ' starts the turn at position ' + repr(combatant.position), file=f)
                        if combatant.target:
                            print('Distance to target: ' + repr(getdistance(combatant.position,combatant.target.position)) + ' feet', file=f)

                        # use movement first #
                        movement(combatant)

                        # action #
                        action(combatant)              

                        # bonus action #        
                        bonus_action(combatant)            
                
                        # additional abilities (action surge etc.)
                        if combatant.action_surge > 0: 
                            print('********************',file = f)
                            print(combatant.name + ' summons all their might, and uses an Action Surge!', file=f)
                            print('********************',file = f)
                            combatant.action_surge -= 1
                            combatant.action_used = False;
                            action(combatant)

                        #print(combatant.name + "s new position: " + repr(combatant.position), file=f)
                        
                        #Apply Hemorraging Critical damage
                        if combatant.hemo_damage > 0:
                            print(combatant.name + ' bleeds profusely from an earlier gunshot wound, suffering ' + repr(combatant.hemo_damage) + ' points of damage from Hemorrhaging Critical!', file=f)
                            #hack
                            combatant.hemo_damage_type = combatant.target.current_weapon.weapon_damage_type
                            deal_damage(combatant,combatant.hemo_damage,combatant.hemo_damage_type,combatant.target.current_weapon.magic)
                            combatant.hemo_damage = 0
                            combatant.hemo_damage_type = 0

                        if combatant.creature_class == creature_class.Monster:
                            if combatant.creature_subclass == creature_subclass.Ancient_Black_Dragon:
                                if not breath_attack:
                                    breath_recharge(combatant)

                        print('That finishes ' + combatant.name + '\'s turn.', file=f)
                        print('', file=f)
                    elif combatant.alive and not combatant.target.alive:
                        combatantdead = True
                        print(combatant.target.name + ' is unconscious! ' + combatant.name + ' wins!', file=f)
                        combatant.no_of_wins += 1
                    else:
                        combatantdead = True
                        print(combatant.name + ' is unconscious! ' + combatant.target.name + ' wins!', file=f)
                        print('_____________________________________________________________________________', file=f)
                        combatant.target.no_of_wins += 1                    
        
        # After 1000 rounds, if no victor, declare stalemate
        if not combatantdead:
            print('Nobody wins - stalemate!',file=f)        

    print('',file= f)
    print('------------------------',file= f)
    print('Summary:',file= f)
    for combatant in combatants:
        print('Name: ' + combatant.name + ' ----- No. of wins: ' + repr(combatant.no_of_wins), file=f)

