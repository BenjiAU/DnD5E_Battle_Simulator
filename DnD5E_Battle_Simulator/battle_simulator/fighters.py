#Explicit imports

#Implicit imports
from .classes import *

#Other imports
import math

def initialise_combatants(init_combatants):
    init_percy(init_combatants)
    init_grog(init_combatants)
    init_vax(init_combatants)

    init_yasha(init_combatants)
    init_nott(init_combatants)
    init_beau(init_combatants)
    init_molly(init_combatants)

    init_hill_giant(init_combatants)
    init_arkhan(init_combatants)
    init_umbrasyl(init_combatants)
    
    init_doty(init_combatants)
    init_trinket(init_combatants)

def initialise_teams(combatants,teams):
    vm = team()
    vm.name = "Vox Machina"    
    teams.append(vm)

    m9 = team()
    m9.name = "The Mighty Nein"
    teams.append(m9)

    monster = team()
    monster.name = "Monsters"
    teams.append(monster)

    beserker = team()
    beserker.name = "Path of the Beserker"
    teams.append(beserker)
    
    zealot = team()
    zealot.name = "Path of the Zealot"
    teams.append(zealot)

    assassin = team()
    assassin.name = "The Raven's Revenant"
    teams.append(assassin)

    gunslinger = team()
    gunslinger.name = "The Lord of Whitestone"
    teams.append(gunslinger)

    blue = team()
    blue.name = "The Blue Team"
    teams.append(blue)

    red = team()
    red.name = "The Red Team"
    teams.append(red)
    vmnames = ["Grog","Vax","Percy","Doty","Trinket"]
    m9names = ["Yasha","Beau","Nott"]
    monsternames = ["Umbrasyl","Hill Giant","Arkhan"]
    #Iterate through all combatants and initially assign them to team
    for combatant in combatants:
        if combatant.name in vmnames:
            combatant.team = vm      
        elif combatant.name in m9names:
            combatant.team = m9
        elif combatant.name in monsternames:
            combatant.team = monster
        else:
            combatant.team = blue

def initialise_starting_positions(combatants):
    for combatant in combatants:
        if combatant.name == "Grog":
            combatant.starting_xpos = 25
            combatant.starting_ypos = 25
        if combatant.name == "Vax":
            combatant.starting_xpos = 0
            combatant.starting_ypos = 10
        if combatant.name == "Percy":
            combatant.starting_xpos = 0
            combatant.starting_ypos = 15
        if combatant.name == "Arkhan":
            combatant.starting_xpos = 0
            combatant.starting_ypos = 20
        if combatant.name == "Umbrasyl":
            combatant.starting_xpos = 50
            combatant.starting_ypos = 50           
        if combatant.name == "Yasha":
            combatant.starting_xpos = 25
            combatant.starting_ypos = 25
        #if combatant.name == "Arkhan":
        #    combatant.position = 1410
        #if combatant.name == "Percy":
        #    combatant.position = 1400
        #if combatant.name == "Umbrasyl":
        #    combatant.position = 1450
        #if combatant.name == "Hill Giant":
        #    combatant.position = 1450
        #if combatant.name == "Doty":
        #    combatant.position = 1450
        #if combatant.name == "Trinket":
        #    combatant.position = 1500

def init_percy(init_combatants):
#Percival    
    percy = creature()
    
    percy.notes = "Burns Grit to Leg Shot opponents, will swap out broken weapons, dumps all Cabal's Ruin charges on crit"

    percy.creature_type = creature_type.Player
    percy.fullname = "Percival Fredrickstein Von Musel Klossowski De Rolo III"
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
    percy.speed = 30
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
    
    grog.notes = "Always Enlarges/Rages on first turn. Will Reckless/Great Weapon Master every chance he gets!"

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
    grog.speed = 50
    grog.proficiency = calc_proficiency(grog)
    grog.weapon_proficiency().append(weapon_type.Axe)

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

    vax.notes = "Missing Deathwalker's Ward. Prefers to throw his daggers from maximum range. Belt of Blade Returning triggers at start of turn"

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
    paladin_class.player_class_level = 6
    vax.player_classes().append(paladin_class)

    druid_class = player_class_block()
    druid_class.player_class = player_class.Druid    
    druid_class.player_class_level = 1
    vax.player_classes().append(druid_class)

    vax.max_health = 127
    vax.armour_class = 20
    vax.speed = 30
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

    init_combatants.append(vax)    

# The Mighty Nein
def init_beau(init_combatants):

    #yasha
    beau = creature()

    beau.notes = "Beauregard, Monk of the Cobalt Soul"

    beau.fullname = "Beauregard"
    beau.name = "Beau"
    beau.race = race.Human
    
    monk_class = player_class_block()
    monk_class.player_class = player_class.Monk
    monk_class.player_subclass = player_subclass.WayOfTheCobaltSoul
    monk_class.player_class_level = 5
    beau.player_classes().append(monk_class)

    #beau.fighting_style = fighting_style.Great_Weapon_Fighting
    beau.max_health = 44
    beau.armour_class = 17
    beau.speed = 40
    beau.proficiency = calc_proficiency(beau)
    beau.weapon_proficiency().append(weapon_type.Unarmed)
    beau.weapon_proficiency().append(weapon_type.Quarterstaff)

    #Stats
    beaustats = statistic_block()
    beaustats.str = 10
    beaustats.dex = 18
    beaustats.con = 16
    beaustats.intel = 14
    beaustats.wis = 16
    beaustats.cha = 12

    beau.stats = beaustats
    
    #Saves
    beausaves = saving_throw_block()    
    beausaves.str = 3
    beausaves.dex = 7
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

def init_molly(init_combatants):

    #yasha
    molly = creature()

    molly.notes = "Mollymauk, Ghostslayer Blood Hunter (based on version 2.1)"

    molly.fullname = "Mollymauk"
    molly.name = "Molly"
    molly.race = race.Tiefling
    
    blood_hunter_class = player_class_block()
    blood_hunter_class.player_class = player_class.BloodHunter
    blood_hunter_class.player_subclass = player_subclass.OrderOfTheGhostslayer
    blood_hunter_class.player_class_level = 5
    molly.player_classes().append(blood_hunter_class)
    
    molly.fighting_style = fighting_style.Two_Weapon_Fighting
    molly.max_health = 59
    molly.armour_class = 15
    molly.speed = 30
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
    # note that unarmed strikes are a property of the blood_hunter class, and Flurry of Blows will kick in automagically
    scimitar = weapon()
    scimitar.name = "Scimitar"
    scimitar.weapon_type = weapon_type.Shortsword;
    scimitar.range = 0
    
    scimitar.damage_die = 6
    scimitar.damage_die_count = 1
    scimitar.weapon_damage_type = damage_type.Bludgeoning
    
    scimitar.finesse = True

    molly.weapon_inventory().append(scimitar)

    scimitar = weapon()
    scimitar.name = "Scimitar"
    scimitar.weapon_type = weapon_type.Shortsword;
    scimitar.range = 0
    
    scimitar.damage_die = 6
    scimitar.damage_die_count = 1
    scimitar.weapon_damage_type = damage_type.Bludgeoning
    
    scimitar.finesse = True

    molly.weapon_inventory().append(scimitar)
    
    #molly's gear
    # combat stats # 

    init_combatants.append(molly)   

def init_nott(init_combatants):

    #yasha
    nott = creature()

    nott.notes = "There's no comma"

    nott.fullname = "Nott the Brave"
    nott.name = "Nott"
    nott.race = race.Human
    
    rogue_class = player_class_block()
    rogue_class.player_class = player_class.Rogue
    rogue_class.player_subclass = player_subclass.ArcaneTrickster
    rogue_class.player_class_level = 5
    nott.player_classes().append(rogue_class)

    #nott.fighting_style = fighting_style.Great_Weapon_Fighting
    nott.max_health = 40
    nott.armour_class = 16
    nott.speed = 30
    nott.proficiency = calc_proficiency(nott)
    nott.weapon_proficiency().append(weapon_type.Crossbow)    
    nott.weapon_proficiency().append(weapon_type.Shortsword)    

    #Stats
    nottstats = statistic_block()
    nottstats.str = 11
    nottstats.dex = 19
    nottstats.con = 14
    nottstats.intel = 16
    nottstats.wis = 11
    nottstats.cha = 5

    nott.stats = nottstats
    
    #Saves
    nottsaves = saving_throw_block()    
    nottsaves.str = 0
    nottsaves.dex = 7
    nottsaves.con = 2
    nottsaves.intel = 6
    nottsaves.wis = 0
    nottsaves.cha = -3
    
    nott.saves = nottsaves

    #Ability Checks
    nottchecks = ability_check_block()
    
    nott.checks = nottchecks    

    #nott's weapons
    hand_crossbow = weapon()
    hand_crossbow.name = "Hand Crossbow"
    hand_crossbow.weapon_type = weapon_type.Crossbow;
    hand_crossbow.range = 30
    hand_crossbow.range_upper = 120
    
    hand_crossbow.damage_die = 6
    hand_crossbow.damage_die_count = 1
    hand_crossbow.weapon_damage_type = damage_type.Piercing
    
    hand_crossbow.light = True
    hand_crossbow.loading = True 
    
    nott.weapon_inventory().append(hand_crossbow)

    shortsword = weapon()
    shortsword.name = "Shortsword"
    shortsword.weapon_type = weapon_type.Shortsword
    shortsword.range = 0    
    
    shortsword.damage_die = 6
    shortsword.damage_die_count = 1
    shortsword.weapon_damage_type = damage_type.Piercing
    
    shortsword.finesse = True
    shortsword.light = True 

    nott.weapon_inventory().append(shortsword)

    #nott's gear
    # combat stats # 

    init_combatants.append(nott)    

def init_yasha(init_combatants):

    #yasha
    yasha = creature()

    yasha.notes = "Yasha, Path of the Zealot Barbarian"

    yasha.fullname = "Yasha"
    yasha.name = "Yasha"
    yasha.race = race.Aasamir
    
    barbarian_class = player_class_block()
    barbarian_class.player_class = player_class.Barbarian
    barbarian_class.player_subclass = player_subclass.PathOfTheZealot
    barbarian_class.player_class_level = 5
    yasha.player_classes().append(barbarian_class)

    #yasha.fighting_style = fighting_style.Great_Weapon_Fighting
    yasha.max_health = 55
    yasha.armour_class = 14
    yasha.speed = 40
    yasha.proficiency = calc_proficiency(yasha)
    yasha.weapon_proficiency().append(weapon_type.Greatsword)
    

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
    
def init_arkhan(init_combatants):

    #Arkhan
    arkhan = creature()

    arkhan.notes = "Wields the Hand of Vecna; can't cast any spells out of it yet!"

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

    arkhan.speed = 40
    arkhan.proficiency = calc_proficiency(arkhan)
    arkhan.weapon_proficiency().append(weapon_type.Axe)

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
    fane_eater.weapon_type = weapon_type.Axe;
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

    init_combatants.append(arkhan)    

def init_umbrasyl(init_combatants):

    umbrasyl = creature()

    umbrasyl.notes = "Can't fly, but can deal some serious damage. Multiattack = bite/claw/claw"

    umbrasyl.creature_type = creature_type.Monster
    umbrasyl.fullname = "Umbrasyl"
    umbrasyl.name = "Umbrasyl"
    umbrasyl.race = race.Dragon    
    umbrasyl.monster_type = monster_type.Ancient_Black_Dragon
    umbrasyl.max_health = 640
    umbrasyl.armour_class = 22
    umbrasyl.speed = 40
        
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

    doty.notes = "The new and improved Doty featuring a single-use Arm Cannon"

    doty.creature_type = creature_type.Monster
    doty.fullname = "Doty 2.0"
    doty.name = "Doty"
    doty.race = race.Construct
    doty.monster_type = monster_type.Doty    
    doty.max_health = 42
    doty.armour_class = 12
    doty.speed = 40
        
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

    hillgiant.notes = "The formidable Hill Giant from C2E18, missing his Legendary Action, but still packs a wallop!"

    hillgiant.creature_type = creature_type.Monster
    hillgiant.fullname = "Hill Giant"
    hillgiant.name = "Hill Giant"
    hillgiant.race = race.Giant
    hillgiant.monster_type = monster_type.Hill    
    hillgiant.max_health = 105
    hillgiant.armour_class = 13
    hillgiant.speed = 40
        
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


def init_trinket(init_combatants):

    trinket = creature()

    trinket.notes = "Everyone's favourite bear. Lacks resistance to Bludgeoning damage granted by his special armour in the show"

    trinket.creature_type = creature_type.Monster
    trinket.fullname = "Trinket"
    trinket.name = "Trinket"
    trinket.race = race.Beast
    trinket.monster_type = monster_type.Bear    
    trinket.max_health = 64
    trinket.armour_class = 20
    trinket.speed = 40
        
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

def characterlevel(combatant):
    player_level = 0
    for class_instance in combatant.player_classes():
        player_level += class_instance.player_class_level
    return player_level

def calc_proficiency(combatant):
    prof_calc = 7+characterlevel(combatant)
    return math.floor(prof_calc/4)