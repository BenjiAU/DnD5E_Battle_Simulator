from enum import Enum, auto

class area_of_effect_shape(Enum):
    def __str__(self):
        return str(self.value)    
    Point = auto()
    Line = auto()
    Circle = auto()
    Square = auto()
    Cone = auto()

class ability_check_block():
    str_adv = bool()
    dex_adv = bool()
    con_adv = bool()
    int_adv = bool()
    wis_adv = bool()
    cha_adv = bool()

class saving_throw_block():
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

class statistic_block():
    str = int()
    dex = int()
    con = int()
    intel = int()
    wis  = int()
    cha = int()

class player_class_block():
    player_class = int()
    player_class_level = int()
    player_subclass = int()
    
class player_class(Enum):
    def __str__(self):
        return str(self.value)    
    Barbarian = auto()
    Bard = auto()
    Cleric = auto()
    Druid = auto()
    Fighter = auto()    
    Rogue = auto()
    Ranger = auto()
    Sorcerer = auto()
    Paladin = auto()
    Warlock = auto()
    Wizard = auto()    
    
class player_subclass(Enum):
    def __str__(self):
        return str(self.value)    
    #Barbarian subclasses
    Beserker = auto()
    Zealot = auto()
    #Fighter subclasses
    Gunslinger = auto()
    #Paladin subclasses
    Oathbreaker = auto()   
    Vengeance = auto()    
    #Rogue subclasses
    Thief = auto()
    Assassin = auto()    
    #Ranger subclasses
    Beastmaster = auto()    

class cardinal_direction(Enum):
    #integers matter for this one
    def __str__(self):
        return str(self.value)    
    Stay = 0
    SouthWest = 1
    South = 2
    SouthEast = 3
    East = 4
    NorthEast = 5
    North = 6
    NorthWest = 7
    West = 8
    Random = 9        

class saving_throw(Enum):
    def __str__(self):
        return str(self.value)    
    Strength = auto()
    Dexterity = auto()
    Constitution = auto()
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

class creature_type(Enum):
    def __str__(self):
        return str(self.value)    
    Player = auto()
    Monster = auto()
    
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

class monster_type(Enum):
    def __str__(self):
        return str(self.value)        
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
    Lucky = auto()
    Sentinel = auto()

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
    BladeReturn = auto()

class spell_school(Enum):
    def __str__(self):
        return str(self.value)
    Divination = auto()
    Transmutation = auto()
    Necromancy = auto()
    Evocation = auto()
    
#Spell slots
# Generic object for tracking min/max spells and level
class spellslot():
    level = int()
    count = int()
    max = int()    

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
   min_spellslot_level = int()
   
   #Maximum spell slot to be expended with additional effect 
   #(i.e. divine smite at 8th level has 5th level properties)
   max_spellslot_level = int()

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
    was_thrown = bool()
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
    battling = bool()

# Generic class for players and monster entities (called creature to be consistent with rulebook)
class creature():
    #Notes - brief description of current status of character
    notes = ""

    #Creature type - broadly defines monster vs player behaviour
    creature_type = int()

    #Monster type - narrows down monster list for specific abilities
    monster_type = int()

    # Team used to track allies/enemies (and not target the wrong one)
    team = team()
    # Core properties, common across creatures
    fullname = ""
    name = ""
    race = int()
    subrace = int()    
    
    max_health = int()
    current_health = int()        
        
    speed = int()   
    movement = int() #Distinct from speed, reflects movement per round and is consumed/reset at start of round

    stats = statistic_block()
    saves = saving_throw_block()
    checks = ability_check_block()    

    current_weapon = weapon()

    armour_class = int()
    armour_type = armour_type()
    
    #Extensible properties (1 to many)    
    def player_classes(self):
        if not hasattr(self, "_player_classes"):
            self._player_classes = []
        return self._player_classes

    def spell_list(self):
        if not hasattr(self, "_spell_list"):
            self._spell_list = []
        return self._spell_list           

    def spellslots(self):
        if not hasattr(self, "_spellslots"):
            self._spellslots = []
        return self._spellslots        

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
    
    proficiency = int() # Determined by taking the PC's 'primary' class, based on the level - see initgrog for example
    
    #Combat/class/race/feat properties - variety of fields used to track whether abilities can be used, the count remaining for abilities, and other combat info
    # Class
    ## Generic
    extra_attack = int()            

    # Feat
    sharpshooter = bool()    
    use_sharpshooter = bool()    
    
    great_weapon_master = bool()
    use_great_weapon_master = bool()
    
    luck_uses = int()
    
    ### Barbarian ###
    canrage = bool()
    ragedamage = int()
    raging = bool()    
    rage_duration = int()
    max_rage_duration = int()
    reckless = bool()
    use_reckless = bool()

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
    sneak_attack_used = bool() #Only one sneak attack per round

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
    channel_divinity = bool()
    divine_smite = bool()
    divine_health = bool()
    aura_of_protection = bool()
    aura_of_courage = bool()
    improved_divine_smite = bool()
    cleansing_touch = bool()

    ## Vengeance
    vow_of_enmity = bool()
    vow_of_enmity_target = None

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
    
    starting_xpos = int()
    starting_ypos = int()
    xpos = int() # x co-ordinate
    ypos = int() # y co-ordinate
    zpos = int() # z co-ordinate (flying/vertical)
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
    disengaged = bool() #Has taken the Disengage action and does not provoke opportunity attacks
    dodging = bool() # Has taken the Dodge action and imparts disadvantage on inbound attacks
    
    # Tracks persistent advantage/disadvantage properties
    has_advantage = bool()
    has_disadvantage = bool() 

    # Tracks other miscellaneous conditoins
    head_shotted = bool() #Victim of Gunslinger Head Shot Trick Shot

    # Generic target object, linked to another creature in the find_target function
    target = None

    #Summary fields - for output at end of simulation    
    attacks_hit = int()
    attacks_missed = int()
    total_damage_dealt = int()    
    rounds_fought = int()    

    #Tracks damage built up over an attack action (including weapon damage, bonus damage, crit damage)
    def pending_damage(self):
        if not hasattr(self, "_pending_damage"):
            self._pending_damage = [] 
        return self._pending_damage

class pending_damage():
    pending_damage_type = int()
    pending_damage = int()