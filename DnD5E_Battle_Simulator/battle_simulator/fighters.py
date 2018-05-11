#Explicit imports
from .combat_functions import characterlevel
#Implicit imports
from .classes import *

#Other imports
import math

def initialise_combatants(init_combatants):
    #init_percy(init_combatants)
    #init_arkhan(init_combatants)
    init_grog(init_combatants)
    init_vax(init_combatants)
    #init_yasha_level4(init_combatants)
    #init_hill_giant(init_combatants)
    #init_yasha(init_combatants)
    #init_umbrasyl(init_combatants)
    #init_doty(init_combatants)
    #init_trinket(init_combatants)

def initialise_team(combatants):
    vm = team()
    vm.name = "Vox Machina"
    monster = team()
    monster.name = "Monsters"
    beserker = team()
    beserker.name = "Path of the Beserker"
    assassin = team()
    assassin.name = "The Lord of Edges"
    zealot = team()
    zealot.name = "Path of the Zealot"
    doty = team()
    doty.name = "Tary"
    trinket = team()
    trinket.name = "Rrraoowr"
    for combatant in combatants:
        if combatant.name == "Grog":
            combatant.team = beserker
        if combatant.name == "Vax":
            combatant.team = assassin
        if combatant.name == "Yasha":
            combatant.team = zealot
        if combatant.name == "Arkhan":
            combatant.team = monster
        if combatant.name == "Percy":
            combatant.team = vm
        if combatant.name == "Umbrasyl":
            combatant.team = monster
        if combatant.name == "Hill Giant":
            combatant.team = monster        
        if combatant.name == "Doty":
            combatant.team = doty
        if combatant.name == "Trinket":
            combatant.team = trinket
                

def initialise_position(combatants):
    for combatant in combatants:
        if combatant.name == "Grog":
            combatant.xpos = 50
            combatant.ypos = 50
        if combatant.name == "Vax":
            combatant.xpos = 75
            combatant.ypos = 75
        
        #if combatant.name == "Yasha":
        #    combatant.position = 1420
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
    percy.fullname = "Percival Fredrickstein Von Musel Klossowski De Rolo III"
    percy.name = "Percy"
    percy.race = race.Human
    percy.creature_class = creature_class.Fighter
    percy.creature_subclass = creature_subclass.Gunslinger
    percy.fighter_level = 20
    percy.fighting_style = fighting_style.Archery
    percy.max_health = 149
    percy.armour_class = 18
    percy.speed = 30
    percy.proficiency = math.floor((7+characterlevel(percy)/4))
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
    grog.fullname = "Grog Strongjaw"
    grog.name = "Grog"
    grog.race = race.Goliath
    grog.creature_class = creature_class.Barbarian
    grog.creature_subclass = creature_subclass.Beserker    
    grog.barbarian_level = 17
    grog.fighter_level = 3
    grog.fighting_style = fighting_style.Great_Weapon_Fighting
    grog.max_health = 248
    grog.armour_class = 17
    grog.speed = 50
    grog.proficiency = math.floor((7+characterlevel(grog))/4)
    grog.weapon_proficiency().append(weapon_type.Axe)

    grog.creature_feats().append(feat.Great_Weapon_Master)

    #Stats
    grogstats = statblock()
    grogstats.str = 26
    grogstats.dex = 15
    grogstats.con = 20
    grogstats.intel = 6
    grogstats.wis = 10
    grogstats.cha = 13

    grog.stats = grogstats
    
    #Saves
    grogsaves = saveblock()    
    grogsaves.str = 14
    grogsaves.dex = 2
    grogsaves.con = 11
    grogsaves.intel = -2
    grogsaves.wis = 0
    grogsaves.cha = 1
    
    grog.saves = grogsaves

    #Ability Checks
    grogchecks = checkblock()
    
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
    vax.fullname = "Vax'ildan"
    vax.name = "Vax"
    vax.race = race.Half_Elf
    vax.subrace = subrace.Revenant
    vax.creature_class = creature_class.Rogue
    vax.creature_subclass = creature_subclass.Assassin
    vax.rogue_level = 12
    vax.paladin_level = 6
    vax.druid_level = 1    
    vax.max_health = 127
    vax.armour_class = 20
    vax.speed = 30
    vax.proficiency = math.floor((7+characterlevel(vax))/4)
    vax.weapon_proficiency().append(weapon_type.Dagger)

    vax.creature_feats().append(feat.Sharpshooter)

    #Stats
    vaxstats = statblock()
    vaxstats.str = 14
    vaxstats.dex = 20
    vaxstats.con = 12
    vaxstats.intel = 16
    vaxstats.wis = 14
    vaxstats.cha = 14

    vax.stats = vaxstats
    
    #Saves
    vaxsaves = saveblock()    
    vaxsaves.str = 2
    vaxsaves.dex = 11
    vaxsaves.con = 7
    vaxsaves.intel = 9
    vaxsaves.wis = 2
    vaxsaves.cha = 2
    
    vax.saves = vaxsaves

    #Ability Checks
    vaxchecks = checkblock()
    
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
    
    # combat stats # 

    init_combatants.append(vax)    

def init_yasha(init_combatants):

    #yasha
    yasha = creature()
    yasha.fullname = "Yasha"
    yasha.name = "Yasha"
    yasha.race = race.Aasamir
    yasha.creature_class = creature_class.Barbarian
    yasha.creature_subclass = creature_subclass.Zealot    
    yasha.barbarian_level = 20
    yasha.fighter_level = 0
    yasha.fighting_style = fighting_style.Great_Weapon_Fighting
    yasha.max_health = 248
    yasha.armour_class = 17
    yasha.speed = 50
    yasha.proficiency = math.floor((7+characterlevel(yasha))/4)
    yasha.weapon_proficiency().append(weapon_type.Axe)

    yasha.creature_feats().append(feat.Great_Weapon_Master)

    #Stats
    yashastats = statblock()
    yashastats.str = 26
    yashastats.dex = 15
    yashastats.con = 20
    yashastats.intel = 6
    yashastats.wis = 10
    yashastats.cha = 13

    yasha.stats = yashastats
    
    #Saves
    yashasaves = saveblock()    
    yashasaves.str = 14
    yashasaves.dex = 2
    yashasaves.con = 11
    yashasaves.intel = -2
    yashasaves.wis = 0
    yashasaves.cha = 1
    
    yasha.saves = yashasaves

    #Ability Checks
    yashachecks = checkblock()
    
    yasha.checks = yashachecks    

    #yasha's weapons
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

    yasha.weapon_inventory().append(bloodaxe)

    #yasha's gear
    
    titanstoneknuckles = equipment()
    titanstoneknuckles.name = "Titanstone Knuckles"
    titanstoneknuckles.grants_equipment_spell = equipment_spells.Enlarge    

    yasha.equipment_inventory().append(titanstoneknuckles)

    bootsofferalleaping = equipment()
    bootsofferalleaping.name = "Boots of Feral Leaping"
    bootsofferalleaping.grans_spell = equipment_spells.Leap

    yasha.equipment_inventory().append(bootsofferalleaping)

    # combat stats # 

    init_combatants.append(yasha)    

def init_yasha_level4(init_combatants):

    #yasha
    yasha = creature()
    yasha.fullname = "Yasha"
    yasha.name = "Yasha"
    yasha.race = race.Aasamir
    yasha.creature_class = creature_class.Barbarian
    yasha.creature_subclass = creature_subclass.Zealot    
    yasha.barbarian_level = 4
    yasha.fighter_level = 0
    #yasha.fighting_style = fighting_style.Great_Weapon_Fighting
    yasha.max_health = 42
    yasha.armour_class = 14
    yasha.speed = 30
    yasha.proficiency = math.floor((7+characterlevel(yasha))/4)
    yasha.weapon_proficiency().append(weapon_type.Greatsword)
    

    #Stats
    yashastats = statblock()
    yashastats.str = 17
    yashastats.dex = 15
    yashastats.con = 14
    yashastats.intel = 12
    yashastats.wis = 9
    yashastats.cha = 7

    yasha.stats = yashastats
    
    #Saves
    yashasaves = saveblock()    
    yashasaves.str = 5
    yashasaves.dex = 2
    yashasaves.con = 4
    yashasaves.intel = 1
    yashasaves.wis = -1
    yashasaves.cha = -2
    
    yasha.saves = yashasaves

    #Ability Checks
    yashachecks = checkblock()
    
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
    
    magiciansjudge.magic_to_hit_modifier = 1
    magiciansjudge.magic_damage_modifier = 1

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
    arkhan.fullname = "Highlord Arkhan the Cruel"
    arkhan.name = "Arkhan"
    arkhan.race = race.Dragonborn
    arkhan.creature_class = creature_class.Paladin
    arkhan.creature_subclass = creature_subclass.Oathbreaker
    arkhan.paladin_level = 14
    arkhan.barbarian_level = 3
    arkhan.fighting_style = fighting_style.Great_Weapon_Fighting
    arkhan.max_health = 191
    arkhan.armour_class = 24
    
    #Arkhan is wearing Heavy plate armour
    arkhan.armour_type = armour_type.Heavy

    arkhan.speed = 40
    arkhan.proficiency = math.floor((7+characterlevel(arkhan))/4)
    arkhan.weapon_proficiency().append(weapon_type.Axe)

    #arkhan.creature_feats().append(feat.Great_Weapon_Master)

    #Stats
    arkhanstats = statblock()
    arkhanstats.str = 20
    arkhanstats.dex = 14
    arkhanstats.con = 14
    arkhanstats.intel = 10
    arkhanstats.wis = 12
    arkhanstats.cha = 18

    arkhan.stats = arkhanstats
    
    #Saves
    arkhansaves = saveblock()    
    arkhansaves.str = 5    
    arkhansaves.dex = 2
    arkhansaves.con = 2   
    arkhansaves.intel = 0    
    arkhansaves.wis = 7    
    arkhansaves.cha = 10    
    
    arkhan.saves = arkhansaves

    #Ability Checks
    arkhanchecks = checkblock()    

    arkhan.checks = arkhanchecks    

    #Spell Slots
    arkhanslots = spellslots()
    arkhanslots.FirstLevelMax = 4
    arkhanslots.SecondLevelMax = 3
    arkhanslots.ThirdLevelMax = 3
    arkhanslots.FourthLevelMax = 1

    arkhan.creature_spellslots = arkhanslots

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
    umbrasyl.fullname = "Umbrasyl"
    umbrasyl.name = "Umbrasyl"
    umbrasyl.race = race.Dragon
    umbrasyl.creature_class = creature_class.Monster
    umbrasyl.creature_subclass = creature_subclass.Ancient_Black_Dragon
    umbrasyl.max_health = 640
    umbrasyl.armour_class = 22
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

def init_doty(init_combatants):

    doty = creature()
    doty.fullname = "Doty 2.0"
    doty.name = "Doty"
    doty.race = race.Construct
    doty.creature_class = creature_class.Monster
    doty.creature_subclass = creature_subclass.Doty
    doty.max_health = 42
    doty.armour_class = 12
    doty.speed = 40
        
    #Stats
    dotystats = statblock()
    dotystats.str = 19
    dotystats.dex = 10
    dotystats.con = 16
    dotystats.intel = 10
    dotystats.wis = 12
    dotystats.cha = 7

    doty.stats = dotystats
    
    #Saves
    dotysaves = saveblock()       
    doty.saves = dotysaves

    #Ability Checks
    dotychecks = checkblock()

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
    hillgiant.fullname = "Hill Giant"
    hillgiant.name = "Hill Giant"
    hillgiant.race = race.Giant
    hillgiant.creature_class = creature_class.Monster
    hillgiant.creature_subclass = creature_subclass.Hill
    hillgiant.max_health = 105
    hillgiant.armour_class = 13
    hillgiant.speed = 40
        
    #Stats
    hillgiantstats = statblock()
    hillgiantstats.str = 21
    hillgiantstats.dex = 8
    hillgiantstats.con = 19
    hillgiantstats.intel = 5
    hillgiantstats.wis = 9
    hillgiantstats.cha = 6

    hillgiant.stats = hillgiantstats
    
    #Saves
    hillgiantsaves = saveblock()    
    
    hillgiant.saves = hillgiantsaves

    #Ability Checks
    hillgiantchecks = checkblock()    

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
    trinket.fullname = "Trinket"
    trinket.name = "Trinket"
    trinket.race = race.Beast
    trinket.creature_class = creature_class.Monster
    trinket.creature_subclass = creature_subclass.Bear
    trinket.max_health = 64
    trinket.armour_class = 20
    trinket.speed = 40
        
    #Stats
    trinketstats = statblock()
    trinketstats.str = 19
    trinketstats.dex = 10
    trinketstats.con = 16
    trinketstats.intel = 4
    trinketstats.wis = 13
    trinketstats.cha = 7

    trinket.stats = trinketstats
    
    #Saves
    trinketsaves = saveblock()    
    
    trinket.saves = trinketsaves

    #Ability Checks
    trinketchecks = checkblock()
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