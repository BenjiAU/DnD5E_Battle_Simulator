from enum import Enum, auto

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

class saving_throw(Enum):
    def __str__(self):
        return str(self.value)    
    Strength = auto()
    Dexterity = auto()
    Consitution = auto()
    Intelligence = auto()
    Wisdom = auto()
    Charisma = auto()

class ability_check(Enum):
    def __str__(self):
        return str(self.value)    
    Strength = auto()
    Dexterity = auto()
    Consitution = auto()
    Intelligence = auto()
    Wisdom = auto()
    Charisma = auto()


#enumerable creature attributes
class race(Enum):
    def __str__(self):
        return str(self.value)    
    #PC Races
    Human = auto()
    Half_Elf = auto()
    Gnome = auto()
    Goliath = auto()
    Aasamir = auto()
    Dragonborn = auto()
    #Monster races
    Dragon = auto()
    Undead = auto()
    Construct = auto()
    Giant = auto()
    Beast = auto()

class subrace(Enum):
    def __str__(self):
        return str(self.value)    
    Revenant = auto()

class creature_class(Enum):
    def __str__(self):
        return str(self.value)    
    Fighter = auto()
    Barbarian = auto()
    Rogue = auto()
    Ranger = auto()
    Paladin = auto()
    Monster = auto()
    
class creature_subclass(Enum):
    def __str__(self):
        return str(self.value)    
    #Fighter subclasses
    Gunslinger = auto()
    #Barbarian subclasses
    Beserker = auto()
    Zealot = auto()
    #Rogue subclasses
    Thief = auto()
    Assassin = auto()
    #Ranger subclasses
    Beastmaster = auto()
    #Paladin subclasses
    Oathbreaker = auto()   
    #Constructs
    Doty = auto()
    #Giants
    Hill = auto()
    #Beasts
    Bear = auto()
    #Dragons
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
    Dagger = auto()
    Crossbow = auto()
    Axe = auto()
    Greataxe = auto()
    Sword = auto()
    Greatsword = auto()
    Natural = auto()

#Armour Type
class armour_type():
    def __str__(self):
        return str(self.value)
    Light = auto()
    Medium = auto()
    Heavy = auto()
    Shield = auto()

class fighting_style(Enum):
    def __str__(self):
        return str(self.value)
    Archery = auto()
    Defense = auto()
    Dueling = auto()
    Great_Weapon_Fighting = auto()
    Protection = auto()
    Two_Weapon_Fighting = auto()

#enumerable spells (undecided if this is the best way to handle spells, maybe only for item-granted ones)
class equipment_spells(Enum):
    def __str__(self):
        return str(self.value)
    CabalsRuin = auto()
    Enlarge = auto()
    Leap = auto()
    HandOfVecna = auto()
    Haste = auto()

class spell_school(Enum):
    def __str__(self):
        return str(self.value)
    Divination = auto()
    Transmutation = auto()
    Necromancy = auto()
    Evocation = auto()

#Spells version 2
class spell():
   name = str()
   
   #Spell school
   school = int()
   
   # Castable range of spell to origin (i..e fireball = 150ft)
   range = int()
   # Spells' origin (point at which spell originates (i.e. fireball erupts from point you choose in range)
   origin = int()
   # Shape enumeration (shape that spell affects, i.e. fireball = 20 ft radius sphere)
   shape = int()
   shape_size = int()

   #Components
   verbal = bool()
   somatic = bool()
   material = bool()
   # Cost in GP for material (as if we'll ever get to that point)
   material_cost = int()

   #Minimum spell slot to be expended to cast spell (0 = cantrip)
   min_spell_slot = int()
   
   #Maximum spell slot to be expended with additional effect 
   #(i.e. divine smite at 8th level has 5th level properties)
   max_spell_slot = int()

   damage_die = int()
   damage_die_count = int()
   damage_type = int()

   #Additional damage to deal per spell slot gap between min_spell_slot (up to max)
   damage_die_per_spell_slot = int()
   damage_die_count_per_spell_slot = int()

   #Bonus damage based on target
   bonus_damage_die = int()
   bonus_damage_die_count = int()
   bonus_damage_target = int()

   saving_throw = int()
   saving_throw_dc = int()

#Spell slots
class spellslots():
    FirstLevel = int()
    SecondLevel = int()
    ThirdLevel = int()
    FourthLevel = int()
    FifthLevel = int()
    SixthLevel = int()
    SeventhLevel = int()
    EigthLevel = int()
    NinthLevel = int()

    FirstLevelMax = int()
    SecondLevelMax = int()
    ThirdLevelMax = int()
    FourthLevelMax = int()
    FifthLevelMax = int()
    SixthLevelMax = int()
    SeventhLevelMax = int()
    EigthLevelMax = int()
    NinthLevelMax = int()

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
    grants_equipment_spell = int()
    max_charges = int()
    current_charges = int()
    damage_die= int()
    damage_die_count = int()
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
    
    # Crit bonus damage (i.e. 2d8 Necrotic on Fane Eater)
    crit_bonus_damage_die = int()
    crit_bonus_damage_die_count = int()
    crit_bonus_damage_type = int()

    # Magic modifiers (i.e. 2 for +2 weapon)
    magic_to_hit_modifier = int() #also use this on monster attacks (i.e. dragon gets +15 on claw, +8 of which comes from str mod - the rest has no source)
    magic_damage_modifier = int()

    # Firearm-specific properties
    reload = int()
    currentammo = int()
    misfire = int()
    broken = bool()
    ruined = bool()

class team():
    name = ""
    no_of_wins = int()

# Generic class for players and monster entities (called creature to be consistent with rulebook)
class creature():
    # Team used to track allies/enemies (and not target the wrong one)
    team = team()
    # Core properties, common across creatures
    fullname = ""
    name = ""
    race = int()
    subrace = int()
    creature_class = int()
    creature_subclass = int()
    
    max_health = int()
    current_health = int()        
        
    speed = int()   

    stats = statblock()
    saves = saveblock()
    checks = checkblock()
    
    current_weapon = weapon()

    armour_class = int()
    armour_type = armour_type()

    creature_spellslots = spellslots()      

    #Extensible properties (1 to many)
    def creature_spells(self):
        if not hasattr(self, "_creature_spells"):
            self._creature_spells = []
        return self._creature_spells           

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
    bard_level = int()
    cleric_level = int()
    druid_level = int()
    fighter_level = int()
    monk_level = int()
    paladin_level = int()
    rogue_level = int()
    ranger_level = int()
    sorcerer_level = int()
    warlock_level = int()
    wizard_level = int()
    
    proficiency = int() # Determined by taking the PC's 'primary' class, based on the level - see initgrog for example
    
    #Combat/class/race/feat properties - variety of fields used to track whether abilities can be used, the count remaining for abilities, and other combat info
    # Class
    ## Generic
    extra_attack = int()        
    
    ### Barbarian ###
    canrage = bool()
    ragedamage = int()
    raging = bool()    
    rage_duration = int()
    max_rage_duration = int()
    reckless = bool()
    use_reckless = bool()
    great_weapon_master = bool()
    use_great_weapon_master = bool()

    brutal_critical = bool()
    brutal_critical_dice = int()
    relentless_rage = bool()
    relentless_rage_DC = int()
    feral_instinct = bool()

    # Beserker
    frenzy = bool()
    retaliation = bool()
    
    # Zealot
    divine_fury = bool()
    divine_fury_used = bool()
    divine_fury_damage_type = int()
    fanatical_focus = bool()
    zealous_presence = bool()
    rage_beyond_death = bool()
    
    ### Fighter ###
    action_surge = int()
    second_wind = bool()
    fighting_style = int()
    
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
    
    ### Rogue ###
    sneak_attack = bool()    
    sneak_attack_damage_die = int()
    sneak_attack_damage_die_count = int()
    cunning_action = bool()
    uncanny_dodge = bool()    
    evasion = bool()
    blindsense = bool()
    slippery_mind = bool()
    elusive = bool()
    stroke_of_luck = bool()

    ## Assassin

    assassinate = bool()
    can_assassinate_target = bool()

    ### Paladin ###
    divine_smite = bool()
    divine_health = bool()
    aura_of_protection = bool()
    aura_of_courage = bool()
    improved_divine_smite = bool()
    cleansing_touch = bool()

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
    conscious = bool() # Tracks if creature is conscious
    death_saving_throw_success = int() # Tracks succesful Death Saving Throws
    death_saving_throw_failure = int() # Tracks failed Death Saving Throws
    stabilised = bool() # Tracks stabilisation (i.e. 3 successes)
    alive = bool() # Tracks if creature is still alive

    enlarged = bool() # Tracks whether creature is affected by the Enlarge equipment spell
    hasted = bool() # Tracks whether creature is affected by the Haste equipment spell 
    hasted_bonus_armour = int() # Tracks the bonus armour granted by Haste
    hasted_action = bool() # Tracks whether the creature has a Hasted action
    hasted_action_used = bool() # Tracks whether the creature used their Hasted action

    target = None

    #Tracks damage built up over an attack action (including weapon damage, bonus damage, crit damage)
    def pending_damage(self):
        if not hasattr(self, "_pending_damage"):
            self._pending_damage = [] 
        return self._pending_damage

class pending_damage():
    pending_damage_type = int()
    pending_damage = int()