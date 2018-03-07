#Explicit imports
#Global settings
from battle_simulator import settings

#Generic combat initialisation functions
from battle_simulator import initialise_combat

#Hard-coded combatant values
from battle_simulator import vox_machina

#Implicit imports
from .print_functions import *
from .combat_functions import *
from .classes import *

#System imports
import operator
from operator import itemgetter, attrgetter, methodcaller



def simulate_battle():
    settings.init() # do only once
    set_output_file()

    init_combatants = []
    vox_machina.initialise_combatants(init_combatants)
    
    attempt=0
    while attempt < settings.max_attempts:
        
        print_output('_____________________________________________________________________________')
        attempt += 1
        print_output('Attempt number:' + repr(attempt))
        print_output(' ')      

        initialise_combat.reset_combatants(init_combatants)

        # Hard-coded initialisation functions for combatants
        vox_machina.initialise_position(init_combatants)
        vox_machina.initialise_team(init_combatants)

        # Get targets
        initialise_combat.initialise_targets(init_combatants)          

        combatantdead = False

        # roll initiative #
        print_output('Rolling initiative...')
        for combatant in init_combatants:     
            roll_initiative(combatant)            
            
            print_output(combatant.name + ' rolled a total of ' + repr(combatant.initiative_roll) + '. They are located at co-ordinates: ' + repr(combatant.position))
            #If the combatant has a valid target, equip a weapon
            if combatant.target:
                weapon_swap(combatant,getdistance(combatant.position,combatant.target.position))
                    #print_output('ERROR: ' + combatant.name + ' has no valid weapons to draw. They will be unable to partake in combat.')


            initkey = operator.attrgetter("initiative_roll")

            combatants = sorted(init_combatants, key=initkey,reverse=True)
        
        #print_output out combat order at top of attempt
        print_output('')
        print_output('Combat order: ')
        combatorder = 0
        for combatant in combatants:                     
            combatorder += 1
            print_details(combatant,combatorder)
            
        #Begin combat rounds (up to a maximum to avoid overflow)
        round = 0        
        while not combatantdead and settings.max_rounds:
            print_output('')
            round = round + 1
            print_output('Round: ' + repr(round))
    
            for combatant in combatants:        
                if not combatantdead:
                    if combatant.alive:
                        print_output('It is now ' + combatant.name + '\'s turn. Current HP: ' + repr(combatant.current_health) + '/' + repr(combatant.max_health))
                        combatant.movement_used = False
                        combatant.action_used = False
                        combatant.bonus_action_used = False
                        combatant.reaction_used = False

                        #print_output(combatant.name + ' starts the turn at position ' + repr(combatant.position))
                        if combatant.target:
                            print_output('Distance to target: ' + repr(getdistance(combatant.position,combatant.target.position)) + ' feet')

                        #check for breath weapon recharge
                        if combatant.creature_class == creature_class.Monster:
                            if combatant.creature_subclass == creature_subclass.Ancient_Black_Dragon:
                                if not combatant.breath_attack:
                                    breath_recharge(combatant)

                        # use movement first #
                        movement(combatant)

                        # action #
                        action(combatant)              

                        # bonus action #        
                        bonus_action(combatant)            
                
                        # additional abilities (action surge etc.)
                        if combatant.action_surge > 0: 
                            print_output('********************')
                            print_output(combatant.name + ' summons all their might, and uses an Action Surge!')
                            print_output('********************')
                            combatant.action_surge -= 1
                            combatant.action_used = False;
                            action(combatant)

                        #print_output(combatant.name + "s new position: " + repr(combatant.position))
                        
                        #Apply Hemorraging Critical damage
                        if combatant.hemo_damage > 0:
                            print_output(combatant.name + ' bleeds profusely from an earlier gunshot wound, suffering ' + repr(combatant.hemo_damage) + ' points of damage from Hemorrhaging Critical!')
                            #hack
                            #combatant.hemo_damage_type = combatant.target.current_weapon.weapon_damage_type
                            #deal damage to yourself
                            deal_damage(combatant,combatant.hemo_damage,combatant.hemo_damage_type,combatant.target.current_weapon.magic)
                            combatant.hemo_damage = 0
                            combatant.hemo_damage_type = 0                        

                        print_output('That finishes ' + combatant.name + '\'s turn.')
                        print_output('')
                    elif combatant.alive and not combatant.target.alive:
                        combatantdead = True
                        print_output(combatant.target.name + ' is unconscious! Team ' + combatant.team.name + ' wins!')
                        combatant.no_of_wins += 1
                    else:
                        combatantdead = True
                        print_output(combatant.name + ' is unconscious! Team ' + combatant.target.team.name + ' wins!')
                        print_output('_____________________________________________________________________________')
                        combatant.team.no_of_wins += 1                    
        
        # After 1000 rounds, if no victor, declare stalemate
        if not combatantdead:
            print_output('Nobody wins - stalemate!')        

    print_output('')
    print_output('------------------------')
    print_output('Summary:')
    teams = []
    for combatant in combatants:
        teams.append(combatant.team)
    for t in teams:
        print_output('Name: ' + t.name + ' ----- No. of wins: ' + repr(t.no_of_wins))
    
    #Close the output file if it is open
    close_file()
