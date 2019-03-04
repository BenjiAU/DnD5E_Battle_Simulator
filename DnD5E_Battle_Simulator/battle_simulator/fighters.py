#Implicit imports
from battle_simulator import settings
from battle_simulator.classes import *
import random

def initialise_combatants(init_combatants):
    # Vox machina
    init_percy(init_combatants)
    init_grog(init_combatants)
    init_vax(init_combatants)    
    init_vex(init_combatants)
    init_trinket(init_combatants)
    #init_scanlan(init_combatants)
    init_keyleth(init_combatants)
    #init_pike(init_combatants)
    #init_tary(init_combatants)                     
    #init_doty(init_combatants)
        
    init_arkhan(init_combatants)
    init_umbrasyl(init_combatants)
    
    #init_kiri(init_combatants)
    init_fjord(init_combatants)
    init_beau(init_combatants)
    init_caleb(init_combatants)
    init_nott(init_combatants)
    init_jester(init_combatants)
    init_clay(init_combatants)
    init_molly(init_combatants)
    init_yasha(init_combatants)    
        
    init_hill_giant(init_combatants)
    init_venom_troll(init_combatants)
    #init_clockwork_warden(init_combatants)    
    init_hydra(init_combatants)
    init_fire_giant(init_combatants)
    init_fire_giant_dreadnought(init_combatants)

    init_lorenzo(init_combatants)
    init_wohn(init_combatants)
    init_protto(init_combatants)
    #init_ruzza(init_combatants)
    #init_dwelma(init_combatants)

def initialise_teams(combatants,teams):
    vm = team()
    vm.name = "Vox Machina"    
    teams.append(vm)

    m9 = team()
    m9.name = "The Mighty Nein"
    teams.append(m9)

    iron = team()
    iron.name = "The Iron Shepherds"
    teams.append(iron)

    monster = team()
    monster.name = "Monsters"
    teams.append(monster)
  
    blue = team()
    blue.name = "The Blue Team"
    teams.append(blue)

    red = team()
    red.name = "The Red Team"
    teams.append(red)

    green = team()
    green.name = "The Green Team"
    teams.append(green)

    yellow = team()
    yellow.name = "The Yellow Team"
    teams.append(yellow)

    vmnames = ["Grog","Vax","Vex","Percy","Scanlan","Keyleth","Pike","Doty","Trinket"]
    m9names = ["Fjord","Beau","Caleb","Nott","Jester","Molly","Yasha","Kiri","Caduceus"]
    monsternames = ["Umbrasyl","Hill Giant","Arkhan","Venom Troll","Hydra"]
    ironnames = ["Lorenzo","Wohn","Protto"]
    #Iterate through all combatants and initially assign them to team
    for combatant in combatants:
        if combatant.name in vmnames:
            combatant.team = vm      
        elif combatant.name in m9names:
            combatant.team = m9
        elif combatant.name in monsternames:
            combatant.team = monster
        elif combatant.name in ironnames:
            combatant.team = iron
        else:
            combatant.team = blue

# Randomise starting positions
def randomise_starting_positions(combatants):
    for combatant in combatants:
        random.seed
        combatant.starting_xpos = round_to_integer(random.randint(-50,50),5)
        combatant.starting_ypos = round_to_integer(random.randint(-50,50),5)

def init_percy(init_combatants):
#Percival    
    percy = creature()
    
    percy.notes = "Sophist of Native Ingenuity"

    percy.creature_type = creature_type.Player
    percy.fullname = "Lord Percival Fredrickstein Von Musel Klossowski De Rolo III"
    percy.name = "Percy"
    percy.race = race.Human
    
    fighter_class = player_class_block()
    fighter_class.player_class = player_class.Fighter
    fighter_class.player_subclass = player_subclass.Gunslinger
    fighter_class.player_class_level = 20
    percy.player_classes().append(fighter_class)

    percy.fighting_style = fighting_style.Archery

    percy.max_health = 149
    percy.armour_class = 18
    percy.base_speed = 30
    percy.proficiency = calc_proficiency(percy)
    percy.weapon_proficiency().append(weapon_type.Firearm)
    percy.weapon_proficiency().append(weapon_type.Longsword)
        
    percy.creature_feats().append(feat.Sharpshooter)
    
    #Stats
    percystats = statistic_block()    
    percystats.str = 12
    percystats.dex = 22
    percystats.con = 14
    percystats.intel = 20
    percystats.wis = 16
    percystats.cha = 14

    percy.stats = percystats

    #Saves
    percysaves = saving_throw_block()
    percysaves.str = 7
    percysaves.dex = 6
    percysaves.con = 8
    percysaves.intel = 5
    percysaves.wis = 3
    percysaves.cha = 2
    
    percy.saves = percysaves

    #Ability checks
    percychecks = ability_check_block()
    
    percy.checks = percychecks

    #Percy's weapons
    #Bad News
    badnews = weapon()
    badnews.name = "Bad News"
    badnews.weapon_type = weapon_type.Firearm;
    badnews.range = 1200
    badnews.ranged_weapon = True

    badnews.damage_die = 12
    badnews.damage_die_count = 2
    badnews.weapon_damage_type = damage_type.Piercing

    badnews.reload = 1
    badnews.currentammo = 1
    badnews.misfire = 3
    
    badnews.two_handed = True
    badnews.finesse = True
    badnews.magic = False

    percy.weapon_inventory().append(badnews)

    #Animus
    animus = weapon()
    animus.name = "Animus"
    animus.weapon_type = weapon_type.Firearm
    animus.range = 600
    animus.ranged_weapon = True

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
    dragonslayer_longsword.weapon_type = weapon_type.Longsword
    
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
    cabalsruin.grants_equipment_spell = equipment_spells.CabalsRuin
    cabalsruin.max_charges = 9
    cabalsruin.current_charges = 0
    cabalsruin.damage_die = 6
    cabalsruin.damage_type = damage_type.Lightning    

    percy.equipment_inventory().append(cabalsruin)

    # add combatants to array
    init_combatants.append(percy)

def init_grog(init_combatants):

    #GROG
    grog = creature()
    
    grog.notes = "The Grand Poobah de Doink of All This and That, Beserker Barbarian"

    grog.creature_type = creature_type.Player
    grog.fullname = "Grog Strongjaw"
    grog.name = "Grog"
    grog.race = race.Goliath
    
    barbarian_class = player_class_block()
    barbarian_class.player_class = player_class.Barbarian
    barbarian_class.player_subclass = player_subclass.PathOfTheBeserker
    barbarian_class.player_class_level = 17
    grog.player_classes().append(barbarian_class)

    fighter_class = player_class_block()
    fighter_class.player_class = player_class.Fighter
    fighter_class.player_class_level = 3
    grog.player_classes().append(fighter_class)
        
    grog.fighting_style = fighting_style.Great_Weapon_Fighting
    grog.max_health = 248
    grog.armour_class = 17
    grog.base_speed = 50
    grog.proficiency = calc_proficiency(grog)
    grog.weapon_proficiency().append(weapon_type.Greataxe)

    grog.creature_feats().append(feat.Great_Weapon_Master)

    #Stats
    grogstats = statistic_block()
    grogstats.str = 26
    grogstats.dex = 15
    grogstats.con = 20
    grogstats.intel = 6
    grogstats.wis = 10
    grogstats.cha = 13

    grog.stats = grogstats
    
    #Saves
    grogsaves = saving_throw_block()    
    grogsaves.str = 14
    grogsaves.dex = 2
    grogsaves.con = 11
    grogsaves.intel = -2
    grogsaves.wis = 0
    grogsaves.cha = 1
    
    grog.saves = grogsaves

    #Ability Checks
    grogchecks = ability_check_block()
    
    grog.checks = grogchecks    

    #Grog's weapons
    bloodaxe = weapon()
    bloodaxe.name = "Blood Axe"
    bloodaxe.weapon_type = weapon_type.Greataxe;
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
    titanstoneknuckles.grants_equipment_spell = equipment_spells.Enlarge    

    grog.equipment_inventory().append(titanstoneknuckles)

    bootsofferalleaping = equipment()
    bootsofferalleaping.name = "Boots of Feral Leaping"
    bootsofferalleaping.grans_spell = equipment_spells.Leap

    grog.equipment_inventory().append(bootsofferalleaping)

    # combat stats # 

    init_combatants.append(grog)    

def init_vax(init_combatants):

    #vax
    vax = creature()

    vax.notes = "Champion of the Raven Queen, Assasin Rogue/Vengeance Paladin"

    vax.creature_type = creature_type.Player
    vax.fullname = "Vax'ildan"
    vax.name = "Vax"
    vax.race = race.Half_Elf
    vax.subrace = subrace.Revenant

    rogue_class = player_class_block()
    rogue_class.player_class = player_class.Rogue
    rogue_class.player_subclass = player_subclass.Assassin
    rogue_class.player_class_level = 13
    vax.player_classes().append(rogue_class)

    paladin_class = player_class_block()
    paladin_class.player_class = player_class.Paladin
    paladin_class.player_subclass = player_subclass.Vengeance
    paladin_class.player_class_level = 8
    vax.player_classes().append(paladin_class)

    druid_class = player_class_block()
    druid_class.player_class = player_class.Druid    
    druid_class.player_class_level = 1
    vax.player_classes().append(druid_class)

    vax.max_health = 127
    vax.armour_class = 20
    vax.base_speed = 30
    vax.proficiency = calc_proficiency(vax)
    vax.weapon_proficiency().append(weapon_type.Dagger)

    vax.creature_feats().append(feat.Sharpshooter)
    vax.creature_feats().append(feat.Lucky)

    #Stats
    vaxstats = statistic_block()
    vaxstats.str = 14
    vaxstats.dex = 20
    vaxstats.con = 12
    vaxstats.intel = 16
    vaxstats.wis = 14
    vaxstats.cha = 14

    vax.stats = vaxstats
    
    #Saves
    vaxsaves = saving_throw_block()    
    vaxsaves.str = 2
    vaxsaves.dex = 11
    vaxsaves.con = 7
    vaxsaves.intel = 9
    vaxsaves.wis = 2
    vaxsaves.cha = 2
    
    vax.saves = vaxsaves

    #Ability Checks
    vaxchecks = ability_check_block()
    
    vax.checks = vaxchecks        


    #vax's weapons
    whisper = weapon()
    whisper.name = "Whisper"
    whisper.weapon_type = weapon_type.Dagger;
    whisper.range = 60
    
    whisper.damage_die = 4
    whisper.damage_die_count = 1
    whisper.weapon_damage_type = damage_type.Piercing
    
    whisper.bonus_damage_die = 8
    whisper.bonus_damage_die_count = 1
    whisper.bonus_damage_type = damage_type.Psychic
    
    whisper.magic_to_hit_modifier = 3
    whisper.magic_damage_modifier = 3

    whisper.finesse = True    
    whisper.magic = True
    whisper.thrown = True

    vax.weapon_inventory().append(whisper)

    daggerofvenom = weapon()
    daggerofvenom.name = "Dagger of Venom"
    daggerofvenom.weapon_type = weapon_type.Dagger;
    daggerofvenom.range = 60
    
    daggerofvenom.damage_die = 4
    daggerofvenom.damage_die_count = 1
    daggerofvenom.weapon_damage_type = damage_type.Piercing
    
    daggerofvenom.magic_to_hit_modifier = 1
    daggerofvenom.magic_damage_modifier = 1

    daggerofvenom.finesse = True    
    daggerofvenom.magic = True
    daggerofvenom.thrown = True

    vax.weapon_inventory().append(daggerofvenom)

    flametonguedagger = weapon()
    flametonguedagger.name = "Flametongue Dagger"
    flametonguedagger.weapon_type = weapon_type.Dagger;
    flametonguedagger.range = 60
    
    flametonguedagger.damage_die = 4
    flametonguedagger.damage_die_count = 1
    flametonguedagger.weapon_damage_type = damage_type.Piercing
    
    flametonguedagger.magic_to_hit_modifier = 1
    flametonguedagger.magic_damage_modifier = 1

    flametonguedagger.finesse = True    
    flametonguedagger.magic = True
    flametonguedagger.thrown = True

    vax.weapon_inventory().append(flametonguedagger)

    #vax's gear
    
    bootsofhaste = equipment()
    bootsofhaste.name = "Boots of Haste"
    bootsofhaste.grants_equipment_spell = equipment_spells.Haste

    vax.equipment_inventory().append(bootsofhaste)

    beltofbladereturning = equipment()
    beltofbladereturning.name = "Belt of Blade Returning"
    beltofbladereturning.grants_equipment_spell = equipment_spells.BladeReturn

    vax.equipment_inventory().append(beltofbladereturning)
    
    # combat stats # 
    divine_smite = spell()
    divine_smite.name = "Divine Smite"
    vax.spell_list().append(divine_smite)

    init_combatants.append(vax)    

def init_vex(init_combatants):

    #vex
    vex = creature()

    vex.notes = "Baroness of the Third House of Whitestone and Grand Mistress of the Grey Hunt"

    vex.creature_type = creature_type.Player
    vex.fullname = "Lady Vex'ahlia"
    vex.name = "Vex"
    vex.race = race.Half_Elf    

    ranger_class = player_class_block()
    ranger_class.player_class = player_class.Ranger
    ranger_class.player_subclass = player_subclass.Beastmaster
    ranger_class.player_class_level = 13
    vex.player_classes().append(ranger_class)

    rogue_class = player_class_block()
    rogue_class.player_class = player_class.Rogue
    rogue_class.player_subclass = player_subclass.Assassin
    rogue_class.player_class_level = 7
    vex.player_classes().append(rogue_class)

    vex.fighting_style = fighting_style.Archery

    vex.max_health = 142
    vex.armour_class = 21
    vex.base_speed = 30
    vex.proficiency = calc_proficiency(vex)
    vex.weapon_proficiency().append(weapon_type.Longbow)
    vex.weapon_proficiency().append(weapon_type.Dagger)

    vex.creature_feats().append(feat.Sharpshooter)

    #Stats
    vexstats = statistic_block()
    vexstats.str = 7
    vexstats.dex = 20
    vexstats.con = 10
    vexstats.intel = 14
    vexstats.wis = 16
    vexstats.cha = 17

    vex.stats = vexstats
    
    #Saves
    vexsaves = saving_throw_block()    
    vexsaves.str = 6
    vexsaves.dex = 13
    vexsaves.con = 2
    vexsaves.intel = 4
    vexsaves.wis = 5
    vexsaves.cha = 5
    
    vex.saves = vexsaves

    #Ability Checks
    vexchecks = ability_check_block()
    
    vex.checks = vexchecks        


    #vex's weapons
    fenthras = weapon()
    fenthras.name = "Fenthras"
    fenthras.weapon_type = weapon_type.Longbow;
    fenthras.ranged_weapon = True
    fenthras.range = 60
   
    fenthras.damage_die = 8
    fenthras.damage_die_count = 1
    fenthras.weapon_damage_type = damage_type.Piercing
    
    fenthras.bonus_damage_die = 4
    fenthras.bonus_damage_die_count = 1
    fenthras.bonus_damage_type = damage_type.Lightning
    
    fenthras.magic_to_hit_modifier = 3
    fenthras.magic_damage_modifier = 5 # includes Bracers of Archery bonus as well as +3

    fenthras.finesse = True    
    fenthras.magic = True    
    
    bramble_shot = spell()
    bramble_shot.name = "Bramble Shot"
    fenthras.spell_on_hit = bramble_shot
    vex.spell_list().append(bramble_shot)
    fenthras.spell_charges = 2

    vex.weapon_inventory().append(fenthras)

    #vex's gear
        
    hunters_mark = spell()
    hunters_mark.name = "Hunter's Mark"
    vex.spell_list().append(hunters_mark)

    lightning_arrow = spell()
    lightning_arrow .name = "Lightning Arrow"
    vex.spell_list().append(lightning_arrow )

    init_combatants.append(vex)    

def init_keyleth(init_combatants):

    #keyleth
    keyleth = creature()

    keyleth.notes = "Archdruid Keyleth"

    keyleth.creature_type = creature_type.Player
    keyleth.fullname = "Lady Keyleth"
    keyleth.name = "Keyleth"
    keyleth.race = race.Half_Elf    

    druid_class = player_class_block()
    druid_class.player_class = player_class.Druid
    druid_class.player_subclass = player_subclass.CircleOfTheMoon
    druid_class.player_class_level = 20
    keyleth.player_classes().append(druid_class)

    keyleth.max_health = 147
    keyleth.armour_class = 17
    keyleth.base_speed = 30
    keyleth.proficiency = calc_proficiency(keyleth)    

    #Stats
    keylethstats = statistic_block()
    keylethstats.str = 14
    keylethstats.dex = 15
    keylethstats.con = 14
    keylethstats.intel = 15
    keylethstats.wis = 22
    keylethstats.cha = 10

    keyleth.stats = keylethstats
    
    #Saves
    keylethsaves = saving_throw_block()    
    keylethsaves.str = 5
    keylethsaves.dex = 5
    keylethsaves.con = 5
    keylethsaves.intel = 8
    keylethsaves.wis = 15
    keylethsaves.cha = 3
    
    keyleth.saves = keylethsaves

    #Ability Checks
    keylethchecks = ability_check_block()
    
    keyleth.checks = keylethchecks        


    #keyleth's weapons

    #keyleth's gear
        
    #keyleth's spells
    
    #keyleth's wild shapes  
    giant_eagle = creature()

    giant_eagle.creature_type = creature_type.Monster
    giant_eagle.challenge_rating = 1
    giant_eagle.fullname = "Giant Eagle"
    giant_eagle.name = "Giant Eagle"
    giant_eagle.race = race.Beast
    giant_eagle.monster_type = monster_type.Eagle  
    giant_eagle.max_health = 26
    giant_eagle.armour_class = 13
    giant_eagle.base_speed = 80
        
    #Stats
    giant_eaglestats = statistic_block()
    giant_eaglestats.str = 16
    giant_eaglestats.dex = 17
    giant_eaglestats.con = 13
    giant_eaglestats.intel = 8
    giant_eaglestats.wis = 14
    giant_eaglestats.cha = 10

    giant_eagle.stats = giant_eaglestats

    #giant_eagle's weapons
    beak = weapon()
    beak.name = "Beak"
    beak.weapon_type = weapon_type.Natural;
    beak.range = 0
    
    beak.damage_die = 6
    beak.damage_die_count = 1
    beak.weapon_damage_type = damage_type.Piercing
    
    giant_eagle.weapon_inventory().append(beak)
        
    talon = weapon()
    talon.name = "Talon"
    talon.weapon_type = weapon_type.Natural;
    talon.range = 0
    
    talon.damage_die = 6
    talon.damage_die_count = 2
    talon.weapon_damage_type = damage_type.Slashing
    
    giant_eagle.weapon_inventory().append(talon)

    giant_eagle.druid_form = keyleth.name

    #Appends an instance of this creature to the combatant's list of potential wild shapes, to allow selection of different creatures 
    keyleth.potential_wild_shapes().append(giant_eagle)                            

    init_combatants.append(keyleth)    

def init_kiri(init_combatants):
    kiri = creature()

    kiri.notes = "The newest member of the Mighty Nein"

    kiri.creature_type = creature_type.Player
    kiri.fullname = "Kiri the Kenku"
    kiri.name = "Kiri"
    kiri.race = race.Kenku    

    rogue_class = player_class_block()
    rogue_class.player_class = player_class.Rogue
    rogue_class.player_subclass = player_subclass.Assassin
    rogue_class.player_class_level = 1
    kiri.player_classes().append(rogue_class)

    kiri.max_health = 99999
    kiri.armour_class = 50
    kiri.base_speed = 1000
    kiri.proficiency = 999
    kiri.weapon_proficiency().append(weapon_type.Dagger)

    kiri.creature_feats().append(feat.Sharpshooter)
    kiri.creature_feats().append(feat.Lucky)

    #Stats
    kiristats = statistic_block()
    kiristats.str = 99
    kiristats.dex = 99
    kiristats.con = 99
    kiristats.intel = 99
    kiristats.wis = 99
    kiristats.cha = 99

    kiri.stats = kiristats
    
    #Saves
    kirisaves = saving_throw_block()    
    kirisaves.str = 99
    kirisaves.dex = 99
    kirisaves.con = 99
    kirisaves.intel = 99
    kirisaves.wis = 99
    kirisaves.cha = 99
    
    kiri.saves = kirisaves

    #Ability Checks
    kirichecks = ability_check_block()
    
    kiri.checks = kirichecks        


    #kiri's weapons
    dagger = weapon()
    dagger.name = "Dagger"
    dagger.weapon_type = weapon_type.Dagger;
    dagger.range = 60
    
    dagger.damage_die = 4
    dagger.damage_die_count = 1
    dagger.weapon_damage_type = damage_type.Piercing
    
    dagger.magic_to_hit_modifier = 3
    dagger.magic_damage_modifier = 3

    dagger.finesse = True    
    dagger.magic = True

    kiri.weapon_inventory().append(dagger)

    init_combatants.append(kiri)    

# The Mighty Nein
def init_fjord(init_combatants):
    fjord = creature()

    fjord.notes = "Pact of the Blade Warlock"

    fjord.fullname = "Fjord"
    fjord.name = "Fjord"
    fjord.race = race.Half_Orc
    fjord.creature_type = creature_type.Player

    warlock_class = player_class_block()
    warlock_class.player_class = player_class.Warlock
    warlock_class.player_subclass = player_subclass.PactOfTheBlade
    warlock_class.player_class_level = 8
    warlock_class.spellcasting_attribute = attribute.Charisma
    fjord.player_classes().append(warlock_class)
    
    fjord.max_health = 82
    fjord.armour_class = 17 #Shield?
    fjord.base_speed = 30
    fjord.proficiency = calc_proficiency(fjord)
    fjord.weapon_proficiency().append(weapon_type.Longsword)       
    fjord.spellcaster = True
    
    #Stats
    fjordstats = statistic_block()
    fjordstats.str = 11
    fjordstats.dex = 11
    fjordstats.con = 18
    fjordstats.intel = 14
    fjordstats.wis = 7
    fjordstats.cha = 18

    fjord.stats = fjordstats
    
    #Saves
    fjordsaves = saving_throw_block()    
    fjordsaves.str = 1
    fjordsaves.dex = 1
    fjordsaves.con = 5
    fjordsaves.intel = 3
    fjordsaves.wis = 2
    fjordsaves.cha = 9
    
    fjord.saves = fjordsaves

    #Ability Checks
    fjordchecks = ability_check_block()
    
    fjord.checks = fjordchecks    

    #fjord's weapons
    wastehunter_falchion = weapon()
    wastehunter_falchion.name = "Wastehunter Falchion"
    wastehunter_falchion.weapon_type = weapon_type.Longsword;
    wastehunter_falchion.range = 0    
    
    wastehunter_falchion.damage_die = 8
    wastehunter_falchion.damage_die_count = 1
    wastehunter_falchion.weapon_damage_type = damage_type.Slashing
    
    wastehunter_falchion.bonus_damage_die = 6
    wastehunter_falchion.bonus_damage_die_count = 1
    wastehunter_falchion.bonus_damage_type = damage_type.Necrotic
    wastehunter_falchion.bonus_damage_target = race.Monstrosity
    
    wastehunter_falchion.versatile = True
    wastehunter_falchion.magic = True
    wastehunter_falchion.pact_weapon = True
    
    fjord.weapon_inventory().append(wastehunter_falchion)
    
    # Fjord's spells - spells are initialised/damage dice calculated during initialisation 
    eldritch_blast = spell()
    eldritch_blast.name = "Eldritch Blast"
    fjord.spell_list().append(eldritch_blast)
    
    fjord.eldritch_invocations().append(eldritch_invocation.Agonising_Blast)
    init_combatants.append(fjord)    

def init_beau(init_combatants):
    beau = creature()

    beau.notes = "Monk of the Cobalt Soul"

    beau.fullname = "Beauregard"
    beau.name = "Beau"
    beau.race = race.Human
    beau.creature_type = creature_type.Player

    monk_class = player_class_block()
    monk_class.player_class = player_class.Monk
    monk_class.player_subclass = player_subclass.WayOfTheCobaltSoul
    monk_class.player_class_level = 8
    beau.player_classes().append(monk_class)

    #beau.fighting_style = fighting_style.Great_Weapon_Fighting
    beau.max_health = 68
    beau.armour_class = 20
    beau.base_speed = 40
    beau.proficiency = calc_proficiency(beau)
    beau.weapon_proficiency().append(weapon_type.Unarmed)
    beau.weapon_proficiency().append(weapon_type.Quarterstaff)
    
    beau.creature_feats().append(feat.Sentinel)

    #Stats
    beaustats = statistic_block()
    beaustats.str = 10
    beaustats.dex = 20
    beaustats.con = 16
    beaustats.intel = 14
    beaustats.wis = 16
    beaustats.cha = 12

    beau.stats = beaustats
    
    #Saves
    beausaves = saving_throw_block()    
    beausaves.str = 3
    beausaves.dex = 8
    beausaves.con = 3
    beausaves.intel = 2
    beausaves.wis = 3
    beausaves.cha = 1
    
    beau.saves = beausaves

    #Ability Checks
    beauchecks = ability_check_block()
    
    beau.checks = beauchecks    

    #beau's weapons
    # note that unarmed strikes are a property of the Monk class, and Flurry of Blows will kick in automagically
    bostaff = weapon()
    bostaff.name = "Bo Staff"
    bostaff.weapon_type = weapon_type.Quarterstaff;
    bostaff.range = 0
    
    bostaff.damage_die = 6
    bostaff.damage_die_count = 1
    bostaff.weapon_damage_type = damage_type.Bludgeoning
    
    bostaff.two_handed = True
    bostaff.monk_weapon = True

    beau.weapon_inventory().append(bostaff)

    #beau's gear
    # combat stats # 

    init_combatants.append(beau)    

def init_caleb(init_combatants):
    caleb = creature()

    caleb.notes = "Transmutation Wizard"

    caleb.fullname = "Caleb Widogast"
    caleb.name = "Caleb"
    caleb.race = race.Human
    caleb.creature_type = creature_type.Player

    wizard_class = player_class_block()
    wizard_class.player_class = player_class.Wizard
    wizard_class.player_subclass = player_subclass.Transmutation
    wizard_class.player_class_level = 8
    wizard_class.spellcasting_attribute = attribute.Intelligence
    caleb.player_classes().append(wizard_class)

    #caleb.fighting_style = fighting_style.Great_Weapon_Fighting
    caleb.max_health = 49
    caleb.armour_class = 11
    caleb.base_speed = 30
    caleb.proficiency = calc_proficiency(caleb)
    caleb.spellcaster = True
    #Stats
    calebstats = statistic_block()
    calebstats.str = 10
    calebstats.dex = 12
    calebstats.con = 14
    calebstats.intel = 20
    calebstats.wis = 16
    calebstats.cha = 16

    caleb.stats = calebstats
    
    #Saves
    calebsaves = saving_throw_block()    
    calebsaves.str = 0
    calebsaves.dex = 1
    calebsaves.con = 2
    calebsaves.intel = 8
    calebsaves.wis = 6
    calebsaves.cha = 3
    
    caleb.saves = calebsaves

    #Ability Checks
    calebchecks = ability_check_block()
    
    caleb.checks = calebchecks    
    
    #caleb's gear
    # combat stats # 
    # Calebs's spells - spells are initialised/damage dice calculated during initialisation 
    # Cantrips
    for spellname in ["Firebolt","Dancing Lights","Friends"]:
        new_spell = spell()
        new_spell.name = spellname
        caleb.spell_list().append(new_spell)

    # Level 1 spells
    for spellname in ["Shield","Detect Magic","Find Familiar","Chromatic Orb","Disguise Self","Alarm","Comprehend Languages","Burning Hands","Identify","Unseen Servant","Sleep","Mage armour","Magic Missiles"]:
        new_spell = spell()
        new_spell.name = spellname
        caleb.spell_list().append(new_spell)

    # Level 2 spells
    for spellname in ["Blur","Scorching Ray","Maximillian's Earthen Grasp","Enlarge","Reduce","Suggestion"]:
        new_spell = spell()
        new_spell.name = spellname
        caleb.spell_list().append(new_spell)

    # Level 3 spells
    for spellname in ["Haste","Slow"]:
        new_spell = spell()
        new_spell.name = spellname
        caleb.spell_list().append(new_spell)

    init_combatants.append(caleb)    

def init_nott(init_combatants):   
    nott = creature()

    nott.notes = "Arcane Trickster Rogue"

    nott.fullname = "Nott the Brave"
    nott.name = "Nott"
    nott.race = race.Goblin
    nott.creature_type = creature_type.Player

    rogue_class = player_class_block()
    rogue_class.player_class = player_class.Rogue
    rogue_class.player_subclass = player_subclass.ArcaneTrickster
    rogue_class.spellcasting_attribute = attribute.Intelligence
    rogue_class.player_class_level = 8
    nott.player_classes().append(rogue_class)
    nott.creature_feats().append(feat.Crossbow_Expert)
    #nott.fighting_style = fighting_style.Great_Weapon_Fighting
    nott.max_health = 65
    nott.armour_class = 18
    nott.base_speed = 30
    nott.proficiency = calc_proficiency(nott)
    nott.weapon_proficiency().append(weapon_type.Crossbow)    
    nott.weapon_proficiency().append(weapon_type.Shortsword)    

    #Stats
    nottstats = statistic_block()
    nottstats.str = 11
    nottstats.dex = 20
    nottstats.con = 14
    nottstats.intel = 16
    nottstats.wis = 11
    nottstats.cha = 5

    nott.stats = nottstats
    
    #Saves
    nottsaves = saving_throw_block()    
    nottsaves.str = 0
    nottsaves.dex = 8
    nottsaves.con = 2
    nottsaves.intel = 6
    nottsaves.wis = 0
    nottsaves.cha = -3
    
    nott.saves = nottsaves

    #Ability Checks
    nottchecks = ability_check_block()
    
    nott.checks = nottchecks    

    #nott's weapons
    tinkertop = weapon()
    tinkertop.name = "Tinkertop Bolt-Blaster-1000"
    tinkertop.weapon_type = weapon_type.Crossbow;
    tinkertop.range = 30
    tinkertop.long_range = 120
    tinkertop.ranged_weapon = True
    
    tinkertop.damage_die = 6
    tinkertop.damage_die_count = 1
    tinkertop.weapon_damage_type = damage_type.Piercing
    
    tinkertop.light = True
    tinkertop.loading = True 
    
    tinkertop.magic_to_hit_modifier = 1
    tinkertop.magic_damage_modifier = 1

    nott.weapon_inventory().append(tinkertop)

    #nott's gear
    # combat stats # 

    init_combatants.append(nott)    

def init_jester(init_combatants):
    jester = creature()

    jester.notes = "Trickery Domain Cleric"

    jester.fullname = "Jester"
    jester.name = "Jester"
    jester.race = race.Tiefling
    jester.creature_type = creature_type.Player

    cleric_class = player_class_block()
    cleric_class.player_class = player_class.Cleric
    cleric_class.player_subclass = player_subclass.TrickeryDomain
    cleric_class.spellcasting_attribute = attribute.Wisdom
    cleric_class.player_class_level = 8
    jester.player_classes().append(cleric_class)

    #jester.fighting_style = fighting_style.Great_Weapon_Fighting
    jester.max_health = 67
    jester.armour_class = 18
    jester.base_speed = 30
    jester.proficiency = calc_proficiency(jester)
    jester.weapon_proficiency().append(weapon_type.Handaxe)        
    jester.spellcaster = True
    #Stats
    jesterstats = statistic_block()
    jesterstats.str = 16
    jesterstats.dex = 18
    jesterstats.con = 15
    jesterstats.intel = 12
    jesterstats.wis = 20
    jesterstats.cha = 12

    jester.stats = jesterstats
    
    #Saves
    jestersaves = saving_throw_block()    
    jestersaves.str = 3
    jestersaves.dex = 4
    jestersaves.con = 2
    jestersaves.intel = 1
    jestersaves.wis = 8
    jestersaves.cha = 4
    
    jester.saves = jestersaves

    #Ability Checks
    jesterchecks = ability_check_block()
    
    jester.checks = jesterchecks    

    #jester's weapons
    handaxe = weapon()
    handaxe.name = "Handaxe"
    handaxe.weapon_type = weapon_type.Handaxe;
    handaxe.range = 0
    
    handaxe.damage_die = 6
    handaxe.damage_die_count = 1
    handaxe.weapon_damage_type = damage_type.Piercing
    
    handaxe.light = True    
    
    jester.weapon_inventory().append(handaxe)

    #jester's gear
    # combat stats # 

    healingword = spell()
    healingword.name = "Healing Word"
    jester.spell_list().append(healingword)

    curewounds = spell()
    curewounds.name = "Cure Wounds"
    jester.spell_list().append(curewounds)

    sacredflame = spell()
    sacredflame.name = "Sacred Flame"
    jester.spell_list().append(sacredflame)        

    init_combatants.append(jester)    

def init_clay(init_combatants):
    caduceus = creature()

    caduceus.notes = "Grave Domain Cleric"

    caduceus.fullname = "Caduceus Clay"
    caduceus.name = "Caduceus"
    caduceus.race = race.Firbolg
    caduceus.creature_type = creature_type.Player

    cleric_class = player_class_block()
    cleric_class.player_class = player_class.Cleric
    cleric_class.player_subclass = player_subclass.GraveDomain
    cleric_class.spellcasting_attribute = attribute.Wisdom
    cleric_class.player_class_level = 8
    caduceus.player_classes().append(cleric_class)

    #caduceus.fighting_style = fighting_style.Great_Weapon_Fighting
    caduceus.max_health = 69
    caduceus.armour_class = 17
    caduceus.base_speed = 30
    caduceus.proficiency = calc_proficiency(caduceus)
     
    caduceus.spellcaster = True
    #Stats
    claystats = statistic_block()
    claystats.str = 10
    claystats.dex = 12
    claystats.con = 16
    claystats.intel = 9
    claystats.wis = 20
    claystats.cha = 16

    caduceus.stats = claystats
    
    #Saves
    claysaves = saving_throw_block()    
    claysaves.str = 0
    claysaves.dex = 1
    claysaves.con = 2
    claysaves.intel = 3
    claysaves.wis = 8
    claysaves.cha = 6
    
    caduceus.saves = claysaves

    #Ability Checks
    claychecks = ability_check_block()
    
    caduceus.checks = claychecks    

    #clay's weapons    

    #clay's gear
    # combat stats # 

    healingword = spell()
    healingword.name = "Healing Word"
    caduceus.spell_list().append(healingword)

    curewounds = spell()
    curewounds.name = "Cure Wounds"
    caduceus.spell_list().append(curewounds)

    sacredflame = spell()
    sacredflame.name = "Sacred Flame"
    caduceus.spell_list().append(sacredflame)        

    init_combatants.append(caduceus)    

def init_yasha(init_combatants):
    yasha = creature()

    yasha.notes = "Path of the Zealot Barbarian"

    yasha.fullname = "Yasha"
    yasha.name = "Yasha"
    yasha.race = race.Aasamir
    yasha.creature_type = creature_type.Player

    barbarian_class = player_class_block()
    barbarian_class.player_class = player_class.Barbarian
    barbarian_class.player_subclass = player_subclass.PathOfTheZealot
    barbarian_class.player_class_level = 8
    yasha.player_classes().append(barbarian_class)

    #yasha.fighting_style = fighting_style.Great_Weapon_Fighting
    yasha.max_health = 91
    yasha.armour_class = 14
    yasha.base_speed = 40
    yasha.proficiency = calc_proficiency(yasha)
    yasha.weapon_proficiency().append(weapon_type.Greatsword)
    yasha.creature_feats().append(feat.Sentinel)

    #Stats
    yashastats = statistic_block()
    yashastats.str = 17
    yashastats.dex = 15
    yashastats.con = 14
    yashastats.intel = 12
    yashastats.wis = 9
    yashastats.cha = 7

    yasha.stats = yashastats
    
    #Saves
    yashasaves = saving_throw_block()    
    yashasaves.str = 6
    yashasaves.dex = 2
    yashasaves.con = 5
    yashasaves.intel = 1
    yashasaves.wis = -1
    yashasaves.cha = -2
    
    yasha.saves = yashasaves

    #Ability Checks
    yashachecks = ability_check_block()
    
    yasha.checks = yashachecks    

    #yasha's weapons
    magiciansjudge = weapon()
    magiciansjudge.name = "Magician\'s Judge"
    magiciansjudge.weapon_type = weapon_type.Greatsword;
    magiciansjudge.range = 0
    
    magiciansjudge.damage_die = 6
    magiciansjudge.damage_die_count = 2
    magiciansjudge.weapon_damage_type = damage_type.Slashing
    
    magiciansjudge.bonus_damage_die = 0
    magiciansjudge.bonus_damage_die_count = 0
    magiciansjudge.bonus_damage_type = damage_type.Necrotic
    
    #magiciansjudge.magic_to_hit_modifier = 1
    #magiciansjudge.magic_damage_modifier = 1

    magiciansjudge.heavy = True
    magiciansjudge.two_handed = True
    magiciansjudge.magic = True

    yasha.weapon_inventory().append(magiciansjudge)

    #yasha's gear
    # combat stats # 

    init_combatants.append(yasha)    

# RIP
def init_molly(init_combatants):
    molly = creature()

    molly.notes = "Ghostslayer Blood Hunter"

    molly.fullname = "Mollymauk Tealeaf"
    molly.name = "Molly"
    molly.race = race.Tiefling
    molly.creature_type = creature_type.Player

    blood_hunter_class = player_class_block()
    blood_hunter_class.player_class = player_class.BloodHunter
    blood_hunter_class.player_subclass = player_subclass.OrderOfTheGhostslayer
    blood_hunter_class.player_class_level = 5
    molly.player_classes().append(blood_hunter_class)
    
    molly.fighting_style = fighting_style.Two_Weapon_Fighting
    molly.max_health = 59
    molly.armour_class = 15
    molly.base_speed = 30
    molly.proficiency = calc_proficiency(molly)
    molly.weapon_proficiency().append(weapon_type.Shortsword)    

    #Stats
    mollystats = statistic_block()
    mollystats.str = 10
    mollystats.dex = 17
    mollystats.con = 14
    mollystats.intel = 11
    mollystats.wis = 16
    mollystats.cha = 11

    molly.stats = mollystats
    
    #Saves
    mollysaves = saving_throw_block()    
    mollysaves.str = 3
    mollysaves.dex = 3
    mollysaves.con = 2
    mollysaves.intel = 0
    mollysaves.wis = 6
    mollysaves.cha = 0
    
    molly.saves = mollysaves

    #Ability Checks
    mollychecks = ability_check_block()
    
    molly.checks = mollychecks    

    #molly's weapons
    # note that crimson rites are a property of the blood_hunter class and will be applied to weapons during combat
    summersdance = weapon()
    summersdance.name = "Summer's Dance"
    summersdance.weapon_type = weapon_type.Scimitar;
    summersdance.range = 0
    
    summersdance.damage_die = 6
    summersdance.damage_die_count = 1
    summersdance.weapon_damage_type = damage_type.Slashing
    
    summersdance.magic_to_hit_modifier = 1
    summersdance.magic_damage_modifier = 1

    summersdance.magic = True
    summersdance.finesse = True
    summersdance.light = True

    molly.weapon_inventory().append(summersdance)

    scimitar = weapon()
    scimitar.name = "Scimitar"
    scimitar.weapon_type = weapon_type.Scimitar;
    scimitar.range = 0
    
    scimitar.damage_die = 6
    scimitar.damage_die_count = 1
    scimitar.weapon_damage_type = damage_type.Slashing
    
    scimitar.finesse = True
    scimitar.light = True
    molly.weapon_inventory().append(scimitar)        
    
    #molly's gear
    # combat stats # 

    init_combatants.append(molly)   

#Monsters    
def init_arkhan(init_combatants):

    #Arkhan
    arkhan = creature()

    arkhan.notes = "Oathbreaker Paladin/Beserker Barbarian, wielding the Hand of Vecna"

    arkhan.creature_type = creature_type.Player
    arkhan.fullname = "Highlord Arkhan the Cruel"
    arkhan.name = "Arkhan"
    arkhan.race = race.Dragonborn
    
    paladin_class = player_class_block()
    paladin_class.player_class = player_class.Paladin
    paladin_class.player_subclass = player_subclass.Oathbreaker
    paladin_class.player_class_level = 14
    arkhan.player_classes().append(paladin_class)

    barbarian_class = player_class_block()
    barbarian_class.player_class = player_class.Barbarian
    barbarian_class.player_subclass = player_subclass.PathOfTheBeserker
    barbarian_class.player_class_level = 3
    arkhan.player_classes().append(barbarian_class)

    arkhan.fighting_style = fighting_style.Great_Weapon_Fighting
    arkhan.max_health = 191
    arkhan.armour_class = 24
    
    #Arkhan is wearing Heavy plate armour
    arkhan.armour_type = armour_type.Heavy

    arkhan.base_speed = 40
    arkhan.proficiency = calc_proficiency(arkhan)
    arkhan.weapon_proficiency().append(weapon_type.Greataxe)

    #arkhan.creature_feats().append(feat.Great_Weapon_Master)

    #Stats
    arkhanstats = statistic_block()
    arkhanstats.str = 20
    arkhanstats.dex = 14
    arkhanstats.con = 14
    arkhanstats.intel = 10
    arkhanstats.wis = 12
    arkhanstats.cha = 18

    arkhan.stats = arkhanstats
    
    #Saves
    arkhansaves = saving_throw_block()    
    arkhansaves.str = 5    
    arkhansaves.dex = 2
    arkhansaves.con = 2   
    arkhansaves.intel = 0    
    arkhansaves.wis = 7    
    arkhansaves.cha = 10    
    
    arkhan.saves = arkhansaves

    #Ability Checks
    arkhanchecks = ability_check_block()    

    arkhan.checks = arkhanchecks    

    #arkhan's weapons
    fane_eater = weapon()
    fane_eater.name = "Fane-Eater Battleaxe"
    fane_eater.weapon_type = weapon_type.Greataxe;
    fane_eater.range = 0
    
    fane_eater.damage_die = 8
    fane_eater.damage_die_count = 2
    fane_eater.weapon_damage_type = damage_type.Slashing
    
    fane_eater.crit_bonus_damage_die = 8
    fane_eater.crit_bonus_damage_die_count = 2 
    fane_eater.crit_bonus_damage_type = damage_type.Necrotic
    
    fane_eater.magic_to_hit_modifier = 3
    fane_eater.magic_damage_modifier = 3

    fane_eater.heavy = True
    fane_eater.two_handed = True
    fane_eater.magic = True

    arkhan.weapon_inventory().append(fane_eater)

    #arkhan's gear    
    handofvecna = equipment()
    handofvecna.name = "Hand of Vecna"
    handofvecna.grants_equipment_spell = equipment_spells.HandOfVecna
    handofvecna.damage_die = 8
    handofvecna.damage_die_count = 2
    handofvecna.damage_type = damage_type.Cold
    arkhan.equipment_inventory().append(handofvecna)
       
    # combat stats # 

    divine_smite = spell()
    divine_smite.name = "Divine Smite"
    arkhan.spell_list().append(divine_smite)

    init_combatants.append(arkhan)    

def init_umbrasyl(init_combatants):

    umbrasyl = creature()

    umbrasyl.notes = "Ancient Black Dragon"

    umbrasyl.creature_type = creature_type.Monster
    umbrasyl.challenge_rating = 21
    umbrasyl.fullname = "Umbrasyl"
    umbrasyl.name = "Umbrasyl"
    umbrasyl.race = race.Dragon    
    umbrasyl.monster_type = monster_type.Ancient_Black_Dragon
    umbrasyl.max_health = 640
    umbrasyl.armour_class = 22
    umbrasyl.base_speed = 40
        
    #Stats
    umbrasylstats = statistic_block()
    umbrasylstats.str = 27
    umbrasylstats.dex = 14
    umbrasylstats.con = 25
    umbrasylstats.intel = 16
    umbrasylstats.wis = 15
    umbrasylstats.cha = 19

    umbrasyl.stats = umbrasylstats
    
    #Saves
    umbrasylsaves = saving_throw_block()    
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
    umbrasylchecks = ability_check_block()
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

def init_doty(init_combatants):

    doty = creature()

    doty.notes = "Automaton of Taryon Darrington"

    doty.creature_type = creature_type.Monster
    doty.challenge_rating = 2
    doty.fullname = "Doty 2.0"
    doty.name = "Doty"
    doty.race = race.Construct
    doty.monster_type = monster_type.Doty    
    doty.max_health = 42
    doty.armour_class = 12
    doty.base_speed = 40
        
    #Stats
    dotystats = statistic_block()
    dotystats.str = 19
    dotystats.dex = 10
    dotystats.con = 16
    dotystats.intel = 10
    dotystats.wis = 12
    dotystats.cha = 7

    doty.stats = dotystats
    
    #Saves
    dotysaves = saving_throw_block()       
    doty.saves = dotysaves

    #Ability Checks
    dotychecks = ability_check_block()

    doty.checks = dotychecks

    #doty's weapons
    armcannon = weapon()
    armcannon.name = "Arm Cannon"
    armcannon.weapon_type = weapon_type.Firearm;
    armcannon.range = 300
    
    armcannon.damage_die = 12
    armcannon.damage_die_count = 2
    armcannon.weapon_damage_type = damage_type.Piercing

    armcannon.reach = 0
    
    armcannon.magic_to_hit_modifier = 3
    armcannon.magic_damage_modifier = 0

    armcannon.reload = 1
    armcannon.current_ammo = 1
    armcannon.misfire = 2
    
    doty.weapon_inventory().append(armcannon)

    bash = weapon()
    bash.name = "Bash"
    bash.weapon_type = weapon_type.Natural;
    bash.range = 0
    
    bash.damage_die = 6
    bash.damage_die_count = 2
    bash.weapon_damage_type = damage_type.Bludgeoning

    bash.reach = 0
    
    bash.magic_to_hit_modifier = 3
    bash.magic_damage_modifier = 1

    doty.weapon_inventory().append(bash)   

    headbutt = weapon()
    headbutt.name = "Headbutt"
    headbutt.weapon_type = weapon_type.Natural;
    headbutt.range = 0
    
    headbutt.damage_die = 8
    headbutt.damage_die_count = 1
    headbutt.weapon_damage_type = damage_type.Bludgeoning

    headbutt.reach = 0
    
    headbutt.magic_to_hit_modifier = 3
    headbutt.magic_damage_modifier = 1

    doty.weapon_inventory().append(headbutt) 

    init_combatants.append(doty)    

def init_hill_giant(init_combatants):

    hillgiant = creature()

    hillgiant.notes = "The formidable Hill Giant from C2E18"

    hillgiant.creature_type = creature_type.Monster
    hillgiant.challenge_rating = 5
    hillgiant.fullname = "Hill Giant"
    hillgiant.name = "Hill Giant"
    hillgiant.race = race.Giant
    hillgiant.monster_type = monster_type.Hill    
    hillgiant.max_health = 105
    hillgiant.armour_class = 13
    hillgiant.base_speed = 40
        
    #Stats
    hillgiantstats = statistic_block()
    hillgiantstats.str = 21
    hillgiantstats.dex = 8
    hillgiantstats.con = 19
    hillgiantstats.intel = 5
    hillgiantstats.wis = 9
    hillgiantstats.cha = 6

    hillgiant.stats = hillgiantstats
    
    #Saves
    hillgiantsaves = saving_throw_block()    
    
    hillgiant.saves = hillgiantsaves

    #Ability Checks
    hillgiantchecks = ability_check_block()    

    hillgiant.checks = hillgiantchecks

    #hillgiant's weapons
    greatclub = weapon()
    greatclub.name = "Greatclub"
    greatclub.weapon_type = weapon_type.Natural;
    greatclub.range = 0
    
    greatclub.damage_die = 8
    greatclub.damage_die_count = 3
    greatclub.weapon_damage_type = damage_type.Bludgeoning
    
    greatclub.magic_to_hit_modifier = 3

    hillgiant.weapon_inventory().append(greatclub)

    init_combatants.append(hillgiant)    

def init_venom_troll(init_combatants):

    venomtroll = creature()

    venomtroll.notes = "The grotesque venom troll from C2E21-E23"

    venomtroll.creature_type = creature_type.Monster
    venomtroll.challenge_rating = 6
    venomtroll.fullname = "Venom Troll"
    venomtroll.name = "Venom Troll"
    venomtroll.race = race.Troll
    venomtroll.monster_type = monster_type.Venom
    venomtroll.max_health = 140
    venomtroll.armour_class = 15
    venomtroll.base_speed = 30
        
    #Stats
    venomtrollstats = statistic_block()
    venomtrollstats.str = 21
    venomtrollstats.dex = 8
    venomtrollstats.con = 19
    venomtrollstats.intel = 5
    venomtrollstats.wis = 9
    venomtrollstats.cha = 6

    venomtroll.stats = venomtrollstats
    
    #Saves
    venomtrollsaves = saving_throw_block()    
    
    venomtroll.saves = venomtrollsaves

    #Ability Checks
    venomtrollchecks = ability_check_block()    

    venomtroll.checks = venomtrollchecks

    #venomtroll's weapons
    claw = weapon()
    claw.name = "Claw"
    claw.weapon_type = weapon_type.Natural;
    claw.range = 0
    
    claw.damage_die = 8
    claw.damage_die_count = 2
    claw.weapon_damage_type = damage_type.Slashing
    
    claw.bonus_damage_die = 8
    claw.bonus_damage_die_count = 2
    claw.bonus_damage_type = damage_type.Poison
    
    claw.magic_to_hit_modifier = 3

    venomtroll.weapon_inventory().append(claw)

    bite = weapon()
    bite.name = "Bite"
    bite.weapon_type = weapon_type.Natural;
    bite.range = 0
    
    bite.damage_die = 8
    bite.damage_die_count = 2
    bite.weapon_damage_type = damage_type.Slashing
    
    bite.bonus_damage_die = 8
    bite.bonus_damage_die_count = 2
    bite.bonus_damage_type = damage_type.Poison
    
    bite.magic_to_hit_modifier = 3

    venomtroll.weapon_inventory().append(bite)

    new_spell = spell()
    new_spell.name = "Venom Burst"
    venomtroll.spell_list().append(new_spell)

    new_event = event()
    new_event.trigger = event_trigger.OnSufferDamage
    new_event.requirements = [dt for dt in damage_type if dt != damage_type.Psychic]
    new_event.invoke = event_invoke.Spell
    new_event.spell = new_spell
    venomtroll.events().append(new_event)

    regeneration = event()
    regeneration.trigger = event_trigger.OnBeginTurn    
    regeneration .invoke = event_invoke.Feature
    regeneration.self_heal = 10
    venomtroll.events().append(regeneration)

    init_combatants.append(venomtroll)    

def init_clockwork_warden(init_combatants):

    clockworkwarden = creature()

    clockworkwarden.notes = "The whirling sphere of blades from C2E25"

    clockworkwarden.creature_type = creature_type.Monster
    clockworkwarden.fullname = "Klef Tinkertop's Clockwork Warden"
    clockworkwarden.name = "Clockwork Warden"
    clockworkwarden.race = race.Construct
    clockworkwarden.monster_type = monster_type.Automaton
    clockworkwarden.max_health = 150
    clockworkwarden.armour_class = 20
    clockworkwarden.base_speed = 40
        
    #Stats
    clockworkwardenstats = statistic_block()
    clockworkwardenstats.str = 21
    clockworkwardenstats.dex = 8
    clockworkwardenstats.con = 19
    clockworkwardenstats.intel = 5
    clockworkwardenstats.wis = 9
    clockworkwardenstats.cha = 6

    clockworkwarden.stats = clockworkwardenstats
    
    #Saves
    clockworkwardensaves = saving_throw_block()    
    
    clockworkwarden.saves = clockworkwardensaves

    #Ability Checks
    clockworkwardenchecks = ability_check_block()    

    clockworkwarden.checks = clockworkwardenchecks

    #clockworkwarden's weapons
    claw = weapon()
    claw.name = "Claw"
    claw.weapon_type = weapon_type.Natural;
    claw.range = 0
    
    claw.damage_die = 8
    claw.damage_die_count = 2
    claw.weapon_damage_type = damage_type.Slashing
    
    claw.bonus_damage_die = 8
    claw.bonus_damage_die_count = 2
    claw.bonus_damage_type = damage_type.Poison
    
    claw.magic_to_hit_modifier = 3

    clockworkwarden.weapon_inventory().append(claw)

    bite = weapon()
    bite.name = "Bite"
    bite.weapon_type = weapon_type.Natural;
    bite.range = 0
    
    bite.damage_die = 8
    bite.damage_die_count = 2
    bite.weapon_damage_type = damage_type.Slashing
    
    bite.bonus_damage_die = 8
    bite.bonus_damage_die_count = 2
    bite.bonus_damage_type = damage_type.Poison
    
    bite.magic_to_hit_modifier = 3

    clockworkwarden.weapon_inventory().append(bite)

    new_spell = spell()
    new_spell.name = "Shrapnel Blast"
    clockworkwarden.spell_list().append(new_spell)

    shed_armour = spell()
    shed_armour.name = "Shed Armour"
    clockworkwarden.spell_list().append(shed_armour)

    new_event = event()
    new_event.trigger = event_trigger.OnSufferDamage    
    new_event.invoke = event_invoke.Spell
    new_event.spell = shed_armour
    clockworkwarden.events().append(new_event)

    regeneration = event()
    regeneration.trigger = event_trigger.OnBeginTurn    
    regeneration.invoke = event_invoke.Feature
    regeneration.self_heal = 10
    clockworkwarden.events().append(regeneration)

    init_combatants.append(clockworkwarden)    

def init_hydra(init_combatants):

    hydra = creature()

    hydra.notes = "The Warden of U'kutoa's Temple (C2E39)"

    hydra.creature_type = creature_type.Monster
    hydra.fullname = "A monstrous Hydra, the Warden of the False Serpent"
    hydra.name = "Hydra"
    hydra.race = race.Monstrosity
    hydra.monster_type = monster_type.Hydra
    hydra.challenge_rating = 8
    hydra.max_health = 172
    hydra.armour_class = 15
    hydra.base_speed = 30
        
    #Stats
    hydrastats = statistic_block()
    hydrastats.str = 20
    hydrastats.dex = 12
    hydrastats.con = 20
    hydrastats.intel = 2
    hydrastats.wis = 10
    hydrastats.cha = 7

    hydra.stats = hydrastats
    
    #Saves
    hydrasaves = saving_throw_block()    
    hydrasaves.str = 5
    hydrasaves.dex = 1
    hydrasaves.con = 5
    hydrasaves.int = -4
    hydrasaves.cha = -2
    hydra.saves = hydrasaves

    #Ability Checks
    hydrachecks = ability_check_block()    

    hydra.checks = hydrachecks

    #hydra's weapons are a bit different - append one weapon for each 'head', remove weapons as heads are destroyed, modify multiattack to be number of heads 
    bite = weapon()
    bite.name = "Bite"
    bite.weapon_type = weapon_type.Natural;
    bite.range = 0
    
    bite.damage_die = 10
    bite.damage_die_count = 1
    bite.weapon_damage_type = damage_type.Piercing
        
    bite.magic_to_hit_modifier = 3

    #Initialise with five heads
    hydra.weapon_inventory().append(bite)
    hydra.current_head_count = 5
    hydra.last_turn_head_count = 5

    #Lose head if > 25 damage taken in a turn    
    new_event = event()
    new_event.trigger = event_trigger.OnSufferDamageThreshold
    new_event.requirements = 25 #More than 25 damage suffered in a round (cumulative)
    new_event.invoke = event_invoke.Feature
    hydra.events().append(new_event)

    #Regrow a head and regain HP
    new_event = event()
    new_event.trigger = event_trigger.OnEndTurn    
    new_event.invoke = event_invoke.Feature    
    new_event.self_heal = 10    
    hydra.events().append(new_event)
    
    cauterise = spell()
    cauterise.name = 'Cauterise'
    hydra.spell_list().append(cauterise)

    new_event = event()
    new_event.trigger = event_trigger.OnSufferDamageType  
    new_event.invoke = event_invoke.Spell
    new_event.requirements = [dt for dt in damage_type if dt == damage_type.Fire]
    new_event.spell = cauterise
    hydra.events().append(new_event)
    
    init_combatants.append(hydra)    

def init_fire_giant(init_combatants):

    firegiant = creature()

    firegiant.notes = "The massive fire Giant from C2E50, slayer of Spurt"

    firegiant.creature_type = creature_type.Monster
    firegiant.challenge_rating = 9
    firegiant.fullname = "Fire Giant"
    firegiant.name = "Fire Giant"
    firegiant.race = race.Giant
    firegiant.monster_type = monster_type.FireGiant    
    firegiant.max_health = 234
    firegiant.armour_class = 18
    firegiant.base_speed = 30
        
    #Stats
    firegiantstats = statistic_block()
    firegiantstats.str = 25
    firegiantstats.dex = 8
    firegiantstats.con = 23
    firegiantstats.intel = 10
    firegiantstats.wis = 14
    firegiantstats.cha = 13

    firegiant.stats = firegiantstats
    
    #Saves
    firegiantsaves = saving_throw_block()    
    firegiantsaves.dex = 3
    firegiantsaves.con = 10
    firegiantsaves.cha = 5
    firegiant.saves = firegiantsaves

    #Ability Checks
    firegiantchecks = ability_check_block()    

    firegiant.checks = firegiantchecks

    #firegiant's weapons
    greatsword = weapon()
    greatsword.name = "Greatsword"
    greatsword.weapon_type = weapon_type.Natural;
    greatsword.range = 0
    
    greatsword.damage_die = 6
    greatsword.damage_die_count = 6
    greatsword.weapon_damage_type = damage_type.Slashing
    
    greatsword.magic_to_hit_modifier = 3

    firegiant.weapon_inventory().append(greatsword)
    
    rock = weapon()
    rock.name = "Rock"
    rock.weapon_type = weapon_type.Natural;
    rock.range = 60
    rock.long_range = 240
    
    rock.damage_die = 10
    rock.damage_die_count = 4
    rock.weapon_damage_type = damage_type.Bludgeoning
    
    rock.magic_to_hit_modifier = 3

    firegiant.weapon_inventory().append(rock)
    init_combatants.append(firegiant)    

def init_fire_giant_dreadnought(init_combatants):

    firegiantdreadnought = creature()

    firegiantdreadnought.notes = "The shield-wielding fire Giant from C2E50 (can't handle more than two damage types, so shield does 6d6 bldg + 2d6 fire)"

    firegiantdreadnought.creature_type = creature_type.Monster
    firegiantdreadnought.challenge_rating = 14
    firegiantdreadnought.fullname = "Fire Giant"
    firegiantdreadnought.name = "Fire Giant"
    firegiantdreadnought.race = race.Giant
    firegiantdreadnought.monster_type = monster_type.FireGiant    
    firegiantdreadnought.max_health = 234
    firegiantdreadnought.armour_class = 18
    firegiantdreadnought.base_speed = 30
        
    #Stats
    firegiantdreadnoughtstats = statistic_block()
    firegiantdreadnoughtstats.str = 27
    firegiantdreadnoughtstats.dex = 9
    firegiantdreadnoughtstats.con = 23
    firegiantdreadnoughtstats.intel = 8
    firegiantdreadnoughtstats.wis = 10
    firegiantdreadnoughtstats.cha = 11

    firegiantdreadnought.stats = firegiantdreadnoughtstats
    
    #Saves
    firegiantdreadnoughtsaves = saving_throw_block()    
    firegiantdreadnoughtsaves.dex = 3
    firegiantdreadnoughtsaves.con = 10
    firegiantdreadnoughtsaves.cha = 5
    firegiantdreadnought.saves = firegiantdreadnoughtsaves

    #Ability Checks
    firegiantdreadnoughtchecks = ability_check_block()    

    firegiantdreadnought.checks = firegiantdreadnoughtchecks

    #firegiantdreadnought's weapons
    fireshield = weapon()
    fireshield.name = "Fireshield"
    fireshield.weapon_type = weapon_type.Natural;
    fireshield.range = 0
    
    fireshield.damage_die = 6
    fireshield.damage_die_count = 6
    fireshield.weapon_damage_type = damage_type.Bludgeoning
    
    fireshield.bonus_damage_die = 6
    fireshield.bonus_damage_die_count = 2
    fireshield.bonus_damage_type = damage_type.Fire

    fireshield.magic_to_hit_modifier = 3

    firegiantdreadnought.weapon_inventory().append(fireshield)
    
    rock = weapon()
    rock.name = "Rock"
    rock.weapon_type = weapon_type.Natural;
    rock.range = 60
    rock.long_range = 240
    
    rock.damage_die = 10
    rock.damage_die_count = 4
    rock.weapon_damage_type = damage_type.Bludgeoning
    
    rock.magic_to_hit_modifier = 3

    firegiantdreadnought.weapon_inventory().append(rock)
    init_combatants.append(firegiantdreadnought)    

# The Iron Shepherds
def init_lorenzo(init_combatants):

    lorenzo = creature()

    lorenzo.notes = "C2E26 - Tealeaf's Bane, has the stats of an Oni until we hear otherwise"

    lorenzo.creature_type = creature_type.Monster
    lorenzo.challenge_rating = 7
    lorenzo.proficiency = calc_proficiency(lorenzo)
    lorenzo.fullname = "Lorenzo, Leader of the Iron Shepherds"
    lorenzo.name = "Lorenzo"    
    lorenzo.race = race.Giant
    lorenzo.monster_type = monster_type.Oni
    lorenzo.max_health = 110
    lorenzo.armour_class = 16
    lorenzo.base_speed = 30
    lorenzo.innate_spellcasting_attribute = attribute.Charisma
        
    #Stats
    lorenzostats = statistic_block()
    lorenzostats.str = 19
    lorenzostats.dex = 11
    lorenzostats.con = 16
    lorenzostats.intel = 14
    lorenzostats.wis = 12
    lorenzostats.cha = 15

    lorenzo.stats = lorenzostats
    
    #Saves
    lorenzosaves = saving_throw_block()    
    lorenzosaves.dex = 3
    lorenzosaves.con = 6
    lorenzosaves.wis = 4
    lorenzosaves.cha = 5
    lorenzo.saves = lorenzosaves

    #Ability Checks
    lorenzochecks = ability_check_block()    

    lorenzo.checks = lorenzochecks

    #lorenzo's weapons
    glaive = weapon()
    glaive.name = "Glaive"
    glaive.weapon_type = weapon_type.Greataxe;
    glaive.range = 0
    
    glaive.damage_die = 10
    glaive.damage_die_count = 1
    glaive.weapon_damage_type = damage_type.Slashing
        
    glaive.reach = True
    glaive.magic_to_hit_modifier = 3

    lorenzo.weapon_inventory().append(glaive)

    new_spell = spell()
    new_spell.name = "Cone of Cold"
    lorenzo.spell_list().append(new_spell)

    regeneration = event()
    regeneration.trigger = event_trigger.OnBeginTurn    
    regeneration .invoke = event_invoke.Feature
    regeneration.self_heal = 10
    lorenzo.events().append(regeneration)

    init_combatants.append(lorenzo)    

def init_wohn(init_combatants):
    wohn = creature()

    wohn.notes = "Path of the Beserker Barbarian"

    wohn.fullname = "Wohn"
    wohn.name = "Wohn"
    wohn.race = race.Human
    wohn.creature_type = creature_type.Player

    barbarian_class = player_class_block()
    barbarian_class.player_class = player_class.Barbarian
    barbarian_class.player_subclass = player_subclass.PathOfTheBeserker
    barbarian_class.player_class_level = 5
    wohn.player_classes().append(barbarian_class)

    #wohn.fighting_style = fighting_style.Great_Weapon_Fighting
    wohn.max_health = 55
    wohn.armour_class = 14
    wohn.base_speed = 40
    wohn.proficiency = calc_proficiency(wohn)
    wohn.weapon_proficiency().append(weapon_type.Greatsword)

    #Stats
    wohnstats = statistic_block()
    wohnstats.str = 17
    wohnstats.dex = 15
    wohnstats.con = 14
    wohnstats.intel = 12
    wohnstats.wis = 9
    wohnstats.cha = 7

    wohn.stats = wohnstats
    
    #Saves
    wohnsaves = saving_throw_block()    
    wohnsaves.str = 6
    wohnsaves.dex = 2
    wohnsaves.con = 5
    wohnsaves.intel = 1
    wohnsaves.wis = -1
    wohnsaves.cha = -2
    
    wohn.saves = wohnsaves

    #Ability Checks
    wohnchecks = ability_check_block()
    
    wohn.checks = wohnchecks    

    #wohn's weapons
    greatsword = weapon()
    greatsword.name = "Greatsword"
    greatsword.weapon_type = weapon_type.Greatsword;
    greatsword.range = 0
    
    greatsword.damage_die = 6
    greatsword.damage_die_count = 2
    greatsword.weapon_damage_type = damage_type.Slashing        

    greatsword.heavy = True
    greatsword.two_handed = True

    wohn.weapon_inventory().append(greatsword)

    #wohn's gear
    # combat stats # 

    init_combatants.append(wohn)    

def init_protto(init_combatants):   
    protto = creature()

    protto.notes = "Assassin Rogue"

    protto.fullname = "Protto"
    protto.name = "Protto"
    protto.race = race.Halfling
    protto.creature_type = creature_type.Player

    rogue_class = player_class_block()
    rogue_class.player_class = player_class.Rogue
    rogue_class.player_subclass = player_subclass.Assassin    
    rogue_class.player_class_level = 5
    protto.player_classes().append(rogue_class)

    #protto.fighting_style = fighting_style.Great_Weapon_Fighting
    protto.max_health = 40
    protto.armour_class = 16
    protto.base_speed = 30
    protto.proficiency = calc_proficiency(protto)
    protto.weapon_proficiency().append(weapon_type.Shortbow)    
    protto.weapon_proficiency().append(weapon_type.Shortsword)    

    #Stats
    prottostats = statistic_block()
    prottostats.str = 11
    prottostats.dex = 19
    prottostats.con = 14
    prottostats.intel = 16
    prottostats.wis = 11
    prottostats.cha = 5

    protto.stats = prottostats
    
    #Saves
    prottosaves = saving_throw_block()    
    prottosaves.str = 0
    prottosaves.dex = 7
    prottosaves.con = 2
    prottosaves.intel = 6
    prottosaves.wis = 0
    prottosaves.cha = -3
    
    protto.saves = prottosaves

    #Ability Checks
    prottochecks = ability_check_block()
    
    protto.checks = prottochecks    

    #protto's weapons
    shortbow = weapon()
    shortbow.name = "Shortbow"
    shortbow.weapon_type = weapon_type.Shortbow;
    shortbow.range = 30
    shortbow.long_range = 120
    
    shortbow.damage_die = 6
    shortbow.damage_die_count = 1
    shortbow.weapon_damage_type = damage_type.Piercing
    
    shortbow.light = True
    shortbow.loading = True 
    
    protto.weapon_inventory().append(shortbow)

    shortsword = weapon()
    shortsword.name = "Shortsword"
    shortsword.weapon_type = weapon_type.Shortsword
    shortsword.range = 0    
    
    shortsword.damage_die = 6
    shortsword.damage_die_count = 1
    shortsword.weapon_damage_type = damage_type.Piercing
    
    shortsword.finesse = True
    shortsword.light = True 

    protto.weapon_inventory().append(shortsword)

    #protto's gear
    # combat stats # 

    init_combatants.append(protto)    


def init_trinket(init_combatants):

    trinket = creature()

    trinket.notes = "Vex'ahlia's animal companion; keep them together mainly so Vex can Sneak Attack more reliably (although AI will alpha him down pretty quick)"

    trinket.creature_type = creature_type.Monster
    trinket.challenge_rating = 2
    trinket.fullname = "Trinket"
    trinket.name = "Trinket"
    trinket.race = race.Beast
    trinket.monster_type = monster_type.Bear    
    trinket.max_health = 64
    trinket.armour_class = 20
    trinket.base_speed = 40
        
    #Stats
    trinketstats = statistic_block()
    trinketstats.str = 19
    trinketstats.dex = 10
    trinketstats.con = 16
    trinketstats.intel = 4
    trinketstats.wis = 13
    trinketstats.cha = 7

    trinket.stats = trinketstats
    
    #Saves
    trinketsaves = saving_throw_block()    
    
    trinket.saves = trinketsaves

    #Ability Checks
    trinketchecks = ability_check_block()
    trinketchecks.str_adv = True

    trinket.checks = trinketchecks

    #trinket's weapons
    bite = weapon()
    bite.name = "Bite"
    bite.weapon_type = weapon_type.Natural;
    bite.range = 0
    
    bite.damage_die = 6
    bite.damage_die_count = 2
    bite.weapon_damage_type = damage_type.Slashing
    
    bite.magic_to_hit_modifier = 5

    trinket.weapon_inventory().append(bite)
        
    claw = weapon()
    claw.name = "Claw"
    claw.weapon_type = weapon_type.Natural;
    claw.range = 0
    
    claw.damage_die = 8
    claw.damage_die_count = 1
    claw.weapon_damage_type = damage_type.Piercing    
    
    claw.magic_to_hit_modifier = 5

    trinket.weapon_inventory().append(claw)

    init_combatants.append(trinket)    

# wild shapes for druids
