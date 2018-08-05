from enum import Enum, auto

import math
import random

class area_of_effect_shape(Enum):
    def __str__(self):
        return str(self.value)    
    Point = auto()
    Line = auto()
    Circle = auto()
    Square = auto()
    Cone = auto()

class origin_point(Enum):
    def __str__(self):
        return str(self.value)    
    Self = auto()
    Target = auto()
    PointInRange = auto()

class attribute(Enum):
   def __str__(self):
       return str(self.value)   
   Strength = auto()
   Dexterity = auto()
   Constitution = auto()
   Intelligence = auto()
   Wisdom = auto()
   Charisma = auto()

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

class creature_condition():
    condition = int()
    source = None
    limited_duration = bool()
    duration = int()
    attribute = int() #Attribute that the condition affects (i.e. Hex grants disadvantage on _attribute_ saving throws)
    grants_action = bool() #Does this condition grant an additional Action (i.e. Haste)
    granted_action_used = int() #Tracks if the extra action granted by this condition has been used 
    grants_advantage = bool()
    grants_disadvantage = bool()
    # Saving throw information
    save_action = bool() # Can save against this condition by spending an action
    save_end_of_turn = bool() # Can save against this condition for free at end of turn
    saving_throw_attribute = int() # Saving throw attribute
    saving_throw_DC = int() # DC of save

class condition(Enum):
    def __str__(self):
        return str(self.value)    
    #Conditions (as per player handbook
    Blinded = auto()
    Charmed = auto()
    Deafened = auto()
    Fatigued = auto()
    Frightened = auto()
    Grappled = auto()
    Incapacitated = auto()
    Invisible = auto()
    Paralyzed = auto()
    Posioned = auto()
    Prone = auto()
    Restrained = auto()
    Stunned = auto()
    Unconscious = auto()
    Exhaustion = auto()

    # Buffs
    Enlarged = auto() #Enlarge/Reduce spell
    Hasted = auto() # Haste spell
    Disengaged = auto() # Disengage action (does not provoke Attacks of Opportunity)
    Dodging = auto() # Dodge action (attacks against are made with disadvantage)
    Raging = auto() #Barbarian Rage
    Reckless = auto() #Barbarian Reckless Attack
    Shielded = auto() # Wizard Shield spell

    # Debuffs
    Hexed = auto() # Hex spell
    Cursed = auto() # Warlock hexblades curse
    Slowed = auto()   # Slow spell
    Reduced = auto() # Enlarge/Reduce spell
    Headshot = auto() # Gunslinger head shot
    Marked = auto() # Affected by Ranger Hunter's Mark

    #Special Concentrating condition
    Concentrating = auto()


class player_class_block():
    player_class = int()
    player_class_level = int()
    player_subclass = int()
    spellcasting_attribute = int()
    
class player_class(Enum):
    def __str__(self):
        return str(self.value)    
    Barbarian = auto()
    Bard = auto()
    BloodHunter = auto()
    Cleric = auto()
    Druid = auto()
    Fighter = auto()    
    Monk = auto()
    Rogue = auto()
    Ranger = auto()
    Sorcerer = auto()
    Paladin = auto()
    Warlock = auto()
    Wizard = auto()    
    
class player_subclass(Enum):
    def __str__(self):
        return str(self.value)    
    #Barbarian subclasses (Paths)
    PathOfTheBeserker = auto()
    PathOfTheZealot = auto()
    #BloodHunter subclasses
    OrderOfTheGhostslayer = auto()
    OrderOfTheProfaneSoul = auto()
    OrderOfTheLycan = auto()
    #Cleric subclasses (Domains)
    LifeDomain = auto()
    TrickeryDomain = auto()    
    #Fighter subclasses
    Battlemaster = auto()
    Gunslinger = auto()
    #Monk subclasses (Ways)
    WayOfTheCobaltSoul = auto()
    WayOfTheOpenHand = auto()
    #Paladin subclasses
    Oathbreaker = auto()   
    Vengeance = auto()    
    #Rogue subclasses
    ArcaneTrickster = auto()
    Assassin = auto()    
    Thief = auto()    
    #Ranger subclasses
    Beastmaster = auto()    
    #Warlock subclasses (Pacts)
    PactOfTheBlade = auto()
    PactOfTheChain = auto()
    #Wizard subclasses (Schools)
    Divination = auto()
    Evocation = auto() 
    Necromancy = auto()
    Transmutation = auto()

class crimson_rite():
    name = str()    
    damage_type = int()
    primal = bool() #True if Primal Rite, False if Esoteric
    activation_damage = int() #Normally = characterlevel, ghostslayer has it halved
    bonus_damage = int()
    bonus_damage_target = int()
    colour = str() #Colour text for flavour

class blood_curse():
    name = str()
    uses_bonus_action = bool()
    uses_reaction = bool()
    amplify_hit_die_cost = int()
    duration = int() #(0 = reaction/instant, 1=until beginning of next turn, other values determined by wis mod etc)

class eldritch_invocation(Enum):
    def __str__(self):
        return str(self.value)    
    Agonising_Blast = auto()
    Thirsting_Blade = auto()

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
    Aasamir = auto()
    Dragonborn = auto()
    Dwarf = auto()
    Human = auto()
    Half_Elf = auto()
    Half_Orc = auto()
    Halfling = auto()
    Gnome = auto()
    Goblin = auto()
    Goliath = auto() 
    Tiefling = auto()
    Kenku = auto()
    #Monster races
    Dragon = auto()
    Undead = auto()
    Construct = auto()
    Giant = auto()
    Troll = auto()
    Beast = auto()
    Monstrosity = auto()

class subrace(Enum):
    def __str__(self):
        return str(self.value)    
    # Player subraces
    Revenant = auto()
    # Monster subraces
    VenomTroll = auto()

class monster_type(Enum):
    def __str__(self):
        return str(self.value)        
    #Constructs
    Doty = auto()
    Automaton = auto()
    #Giants
    Hill = auto()
    Oni = auto()
    #Beasts
    Bear = auto()
    #Dragons
    Ancient_Black_Dragon = auto()
    #Trolls
    Venom = auto()
    

class feat(Enum):
    def __str__(self):
        return str(self.value)    
    Sharpshooter = auto()
    Great_Weapon_Master = auto()
    Lucky = auto()
    Sentinel = auto()
    Crossbow_Expert = auto()

#enumerable weapon attributes
class weapon_type(Enum):
    def __str__(self):
        return str(self.value)
    Firearm = auto()
    Shortbow = auto()
    Longbow = auto()    
    Crossbow = auto()

    Dagger = auto()
    Handaxe = auto()
    Shortsword = auto()
    Longsword = auto()
    Scimitar = auto()

    Greataxe = auto()
    Greatsword = auto()
    Quarterstaff = auto()

    Natural = auto()
    Unarmed = auto()

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
    Abjuration = auto()

class spell_category(Enum):
    def __str__(self):
        return str(self.value)
    Healing = auto()
    AoE_Healing = auto()
    Buff = auto()
    AoE_Buff = auto()
    Debuff = auto()
    AoE_Debuff = auto()
    Damage = auto()
    AoE_Damage = auto()
    
class spell_casting_time(Enum):
    def __str__(self):
        return str(self.value)    
    Action = auto()
    Bonus_Action = auto()
    Reaction = auto()
    Instant = auto() # Instant spells apply basically automatically, i.e. Divine Smite
    
#Spell slots
# Generic object for tracking min/max spells and level
class spellslot():
    level = int()
    count = int()
    max = int()    

#Spells version 2
class spell():
   name = str()   
   description = str()   
   category = int() #Internal Spell category, to make spell selection logic easier

   school = int() #Spell school
      
   concentration = bool() #True if this spell is a Concentrating spell (inflicts a Concentrating condition on caster)
   maximum_duration = int() # Maximum duration of the spell   

   cantrip = bool() #True if a cantrip, spellslots do not apply
   min_spellslot_level = int() #Minimum spell slot to be expended to cast spell (0 = cantrip)   
   max_spellslot_level = int() #Maximum spell slot to be expended with additional effect (i.e. divine smite at 8th level has 5th level properties)
   
   casting_time = int()# Casting Time - normally action/bonus action
   
   range = int() # Castable range of spell to origin (i..e fireball = 150ft)   
   origin = int() # Spells' origin (point at which spell originates (i.e. fireball erupts from point you choose in range)
   shape = int() # Shape enumeration (shape that spell affects, i.e. fireball = 20 ft radius sphere)
   shape_width = int()
   shape_length = int()
   
   condition = int() # The condition inflicted by the skill (if any- this could be a buff or debuff, or an additional affect of a damaging spell)
   condition_duration = int() # Duration for the inflicted condition

   spell_attack = bool()   # True if this spell is a spell attack, false if it's a DC save (range attribute determines range or touch) or buff
   saving_throw_attribute = int() #Saving throw information, defined if a save is required, otherwise blank (i.e. for buffs/spell attacks)   
   saving_throw_damage_multiplier = int() # Damage multiplier if save is successful (0 = no damage, .5 = half damage on successful save)    
   repeat_save_action = bool()
   repeat_save_end_of_turn = bool()   

   instance = int() # Instances of damage; i.e. Eldritch blast gains additional beams at 5th, 11th, 17th level     
   
   flat_damage = int() # Flat damage added to die damage of spell

   damage_die = int()
   damage_die_count = int()
   damage_type = int()
   
   damage_die_per_spell_slot = int() # Additional damage die per spell slot
   damage_die_count_per_spell_slot = int() # Count of additional damage die per spell slot
   instance_per_spell_slot = int() #Additional spell instances per spell slot

   bonus_damage_die = int() 
   bonus_damage_die_count = int()
   bonus_damage_target = int() #Bonus damage inflicted if race = target
   
   healing_die = int()
   healing_die_count = int()
   healing_die_per_spell_slot = int() # Additional healing die per spell slot
   healing_die_count_per_spell_slot = int() # Count of additional healing die per spell slot   

   # Errata   
   verbal = bool() #Has Verbal Components
   somatic = bool() #Has Somatic Components
   material = bool() #Has Material Components   
   material_cost = int() # Cost in GP for material (as if we'll ever get to that point)
   
   #Player Class types that can cast this spell
   def player_classes(self):
        if not hasattr(self, "_player_classes"):
            self._player_classes = []
        return self._player_classes
   
#various damage types
class damage_type(Enum):
    def __str__(self):
        return str(self.value)
    Piercing = auto()
    Slashing = auto()
    Bludgeoning = auto()
    Force = auto()
    Fire = auto()
    Cold = auto()
    Lightning = auto()
    Necrotic = auto()
    Radiant = auto()
    Poison = auto()
    Psychic = auto()
    Acid = auto()
    Generic = auto() # Damage that is typeless and should never be subject to resistance/immunity/vulnerability, i.e. damage suffered by blood hunter for activating a crimson rite 

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
    long_range = int()
    reach = int()
    thrown = bool()
    was_thrown = bool()
    two_handed = bool()
    versatile = bool()
    silvered = bool()

    # Special property to track wheter weapon is a "Monk Weapon", and can thus be used with Flurry of Blows
    monk_weapon = bool()

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

    # Crimson Rite - when activated, the weapon inherits the crimson rite object off the player for damage calculation and to persist between turns
    active_crimson_rite = None

    # Warlock Pact of the Blade weapon toggle (flavour mainly)
    pact_weapon = bool()
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
    challenge_rating = int() # CR, used only for proficiency calcs and display
    innate_spellcasting_attribute = int() # Defines innate spellcasting attribute for monster spells

    # Team used to track allies/enemies (and not target the wrong one)
    team = team()
    # Core properties, common across creatures
    fullname = ""
    name = ""
    race = int()
    subrace = int()    
    
    max_health = int()
    current_health = int()        
        
    base_speed = int() # Base speed
    current_speed = int() # Current speed, reset to base speed at the start of each round
    movement = int() #Available feet of movement, manipulated through the flow of battle as the combatants want to move closer or farther up to their current speed
    desired_range = int() # Set by movement functions, determines the desired range that the combatant wants tok eep between them and target

    stats = statistic_block()
    saves = saving_throw_block()
    checks = ability_check_block()    

    main_hand_weapon = None # Weapon object
    offhand_weapon = None # Only populated if combatant is dual wielding and holding a different weapon in the off hand
    spellcaster = bool() #Simple boolean value to describe whether this character should focus on casting spells, or using weapons

    armour_class = int()
    armour_type = armour_type()
    
    #Extensible properties (1 to many)    
    def player_classes(self):
        if not hasattr(self, "_player_classes"):
            self._player_classes = []
        return self._player_classes

    def creature_conditions(self):
        if not hasattr(self, "_creature_conditions"):
            self._creature_conditions = []
        return self._creature_conditions

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
    
    # Events are out of turn 'things' that can occur with a trigger and a reactionary spell (i.e. venom troll venom spray on suffering damage)
    def events(self):
        if not hasattr(self, "_events"):
            self._events = []
        return self._events

    proficiency = int() # Determined by taking the PC's 'primary' class, based on the level - see initgrog for example
    
    #Combat/class/race/feat properties - variety of fields used to track whether abilities can be used, the count remaining for abilities, and other combat info
    # Class
    ## Generic
    extra_attack = int()            
    
    evasion = bool() # Can come from either Rogue or Monk class

    # Feat
    sharpshooter = bool()    
    use_sharpshooter = bool()    
    
    great_weapon_master = bool()
    use_great_weapon_master = bool()
    
    luck_uses = int()
    
    #############
    # Barbarian #
    #############
    barbarian_unarmored_defense = bool()
    canrage = bool()
    ragedamage = int()
    max_rage_duration = int()
    reckless = bool()    

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

    #############
    #Blood Hunter
    #############    

    # Structures for maintaining the selected crimson rites/blood curses for the creature
    def crimson_rites(self):
        if not hasattr(self, "_crimson_rites"):
            self._crimson_rites = []
        return self._crimson_rites

    def blood_curses(self):
        if not hasattr(self, "_blood_curses"):
            self._blood_curses = []
        return self._blood_curses

    crimson_rite = bool()
    crimson_rite_damage_die = int()
    blood_maledict = bool()
    blood_maledict_uses = int()
    dark_velocity = bool()
    hardened_soul = bool()
    enduring_form = bool()
    sanguine_mastery = bool()

    ## Ghostslayer
    hallowed_veins = bool()
    supernal_flurry = bool()
    vengeful_spirit = bool()

    #############
    ## Fighter ##
    #############

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

    #############
    #### Monk ###
    #############
    monk_unarmored_defense = bool()
    martial_arts = bool()
    martial_arts_die = int()

    ki = bool()
    ki_points = int()
    max_ki_points = int()
    flurry_of_blows = bool()
    patient_defense = bool()
    step_of_the_wind = bool()
    unarmored_movement = bool()
    unarmored_movement_bonus = int()

    deflect_missiles = bool()

    slow_fall = bool()

    stunning_strike = bool()

    ki_empowered_strikes = bool()

    stillness_of_mind = bool()

    purity_of_body = bool()

    diamond_soul = bool()
    ## Open Hand

    ## Cobalt Soul

    #############
    ## Paladin ##
    #############
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
      
    #############
    ### Rogue ###
    #############
    sneak_attack = bool()    
    sneak_attack_damage_die = int()
    sneak_attack_damage_die_count = int()    
    sneak_attack_used = bool() #Only one sneak attack per round

    cunning_action = bool()
    uncanny_dodge = bool()    

    blindsense = bool()
    slippery_mind = bool()
    elusive = bool()
    stroke_of_luck = bool()

    ## Assassin

    assassinate = bool()
    can_assassinate_target = bool()

    #############
    ## Warlock ##
    #############
    # Structures for managing Eldritch Invocations
    def eldritch_invocations(self):
        if not hasattr(self, "_eldritch_invocations"):
            self._eldritch_invocations = []
        return self._eldritch_invocations

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

    bonus_action_spell_casted = bool() # Stops you casting anything but a cantrip if you use BA to cast a spell

    death_saving_throw_success = int() # Tracks succesful Death Saving Throws
    death_saving_throw_failure = int() # Tracks failed Death Saving Throws
    stabilised = bool() # Tracks stabilisation (i.e. 3 successes)
    alive = bool() # Tracks if creature is still alive
       
    # Tracks persistent advantage/disadvantage properties
    has_advantage = bool()
    has_disadvantage = bool() 

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
    crit = bool() #Marks whether this damage is from a critical strike

# Helper Functions
# Keep functions that need to be accessed from around the program here, as long as they don't require any outside knowledge (i.e. are constructed just from the nature of classes)

def melee_range():
    #Treating default melee weapon range as 5 feet, upped to 8 to avoid clipping issues on corners of grid
    return 8

# Check if Great Weapon Fighting is allowed - must have Fighting Style, and appopriate weapon with the correct properties in both hands
def greatweaponfighting(combatant):
    if (combatant.fighting_style == fighting_style.Great_Weapon_Fighting and 
    ((combatant.main_hand_weapon.two_handed or combatant.main_hand_weapon.versatile) and combatant.offhand_weapon == combatant.main_hand_weapon)) :
        return True
    return False

# Return the class level for a given class attached to the player
def get_combatant_class_level(combatant,combatant_class):
    for class_instance in combatant.player_classes():
        if class_instance.player_class == combatant_class:
            return class_instance.player_class_level

# Returns the total character level for all classes attached to the player (necessary for calculating proficiency and some class features)
def characterlevel(combatant):
    player_level = 0
    for class_instance in combatant.player_classes():
        player_level += class_instance.player_class_level
    return player_level

# Returns the proficiency bonus of the creature
def calc_proficiency(combatant):
    if combatant.creature_type == creature_type.Monster:
        if combatant.challenge_rating <= 4:
            prof_calc = 8
        else:
            prof_calc = 7+combatant.challenge_rating
    else:
        prof_calc = 7+characterlevel(combatant)
    return math.floor(prof_calc/4)

# Custom rounding function to ensure we can reliably round values to the nearest 5 feet (for grid calculations)
def round_to_integer(x, base):
    return int(base * round(float(x)/base))

# Return the weighted statistic modifiers 
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

def spellcasting_ability_modifier(combatant,spell):
    modifier = 0
    if combatant.creature_type == creature_type.Monster:
        player_spellcasting_attribute = combatant.innate_spellcasting_attribute        
    else:
        player_spellcasting_attribute = None
        for spell_player_class in spell.player_classes():
            for player_class_block in combatant.player_classes():            
                if spell_player_class == player_class_block.player_class:
                    player_spellcasting_attribute = player_class_block.spellcasting_attribute
    
    if player_spellcasting_attribute == attribute.Intelligence:
        modifier = intmod(combatant)
    elif player_spellcasting_attribute == attribute.Wisdom:
        modifier = wismod(combatant)
    elif player_spellcasting_attribute == attribute.Charisma:
        modifier = chamod(combatant)
    return modifier

def spell_save_DC(combatant,spell):
    modifier = spellcasting_ability_modifier(combatant,spell)
    return 8 + combatant.proficiency + modifier

# Rolls a dice (initiates a new random seed on each call) #
def roll_die(die):
    random.seed
    return random.randint(1,die)

class event():
    trigger = int() # event_triggers are littered through the code at appropriate points for the events module to intervene
    invoke = int() #describes what to do when trigger occurs
    requirements = [] # List of abstract conditions, at least one of which must match the calling trigger code
    spell = spell() # Spell object to be called if invoke = Spell
    self_heal = int() # Self heal from Regeneration?
    disabled = bool() # Disabled for one turn due to reasons

class event_trigger(Enum):
    def __str__(self):
        return str(self.value)    
    OnSufferDamage = auto()
    OnDealDamage = auto()
    OnBeginTurn = auto()
    OnEndTurn = auto()
    OnUnconscious = auto()
    OnDeath = auto()
    OnKill = auto()

class event_invoke(Enum):
    def __str__(self):
        return str(self.value)    
    Spell = auto()
    Action = auto()
    BonusAction = auto()
    Reaction = auto()
    Attack = auto()
    Feature = auto()