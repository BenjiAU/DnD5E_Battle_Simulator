#Explicit imports
#Global settings
from battle_simulator import settings

#Generic combat initialisation functions
from battle_simulator import initialise_combat

#Hard-coded combatant values
from battle_simulator import fighters

#Implicit imports
from .print_functions import *
from .combat_functions import *
from .classes import *

#System imports
import operator
from operator import itemgetter, attrgetter, methodcaller


def default_simulation(init_combatants):
    fighters.initialise_combatants(init_combatants)
    fighters.initialise_team(init_combatants)
    # Hard-coded initialisation functions for combatants
    fighters.initialise_position(init_combatants)

def simulate_battle():
    settings.init() # do only once
    set_output_file()

    init_combatants = []
    default_simulation(init_combatants)

    attempt=0
    while attempt < settings.max_attempts:
        # Beginning of battle attempt
        battle_complete = False
        print_output('_____________________________________________________________________________')
        attempt += 1
        print_output('<b>Attempt number: ' + repr(attempt)+ '</b>')
        print_output(' ')      
        
        initialise_combat.reset_combatants(init_combatants)
        
        #Re-initialise position for new round
        fighters.initialise_position(init_combatants)

        # Get targets
        initialise_combat.initialise_targets(init_combatants)          

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
        print_output("</br>")
        print_output('Combat order: ')
        combatorder = 0
        for combatant in combatants:                     
            combatorder += 1
            print_details(combatant,combatorder)
            
        #Begin combat rounds (up to a maximum to avoid overflow)
        round = 0              
        while not battle_complete and round < settings.max_rounds:
            # Beginning of round
            round_complete = False
            print_output("</br>")
            round = round + 1                
            print_output('<b>Round: ' + repr(round) + '</b>')
    
            for combatant in combatants:        
                if not round_complete:
                    print_output("</br>")
                    print_output('It is now ' + combatant.name + '\'s turn. Current HP: ' + repr(combatant.current_health) + '/' + repr(combatant.max_health))
                    if combatant.alive:
                        print_output('<b>Determining targets:</b>')
                        if combatant.target:
                            if not combatant.target.alive:
                                #refresh targets
                                print_output(combatant.name + '\'s target is dead! Choosing new target...')
                                initialise_combat.initialise_targets(init_combatants)

                            # Conscious actions
                            if combatant.conscious:
                                if combatant.target:
                                    print_output(combatant.name + ' is targetting: ' + combatant.target.name)

                                    combatant.movement_used = False
                                    combatant.action_used = False
                                    combatant.bonus_action_used = False
                                    combatant.reaction_used = False

                                    #Divine Fury (resets at thes tart of each turn)
                                    if combatant.divine_fury:
                                        combatant.divine_fury_used = False
                                    
                                    # Determine distance between targets and report if it is > 0
                                    dist = getdistance(combatant.position,combatant.target.position)
                                    if combatant.target and dist > 0:
                                        print_output('Distance to target: ' + repr(dist) + ' feet')

                                    #check for breath weapon recharge
                                    if combatant.creature_class == creature_class.Monster:
                                        if combatant.creature_subclass == creature_subclass.Ancient_Black_Dragon:
                                            if not combatant.breath_attack:
                                                breath_recharge(combatant)

                                    # use movement first #
                                    print_output('<b>Movement:</b>')
                                    movement(combatant)

                                    # action #
                                    print_output('<b>Action:</b>')
                                    action(combatant)              

                                    # bonus action #       
                                    print_output('<b>Bonus Action:</b>') 
                                    bonus_action(combatant)            
                
                                    # additional abilities (action surge etc.)
                                    if combatant.action_surge > 0: 
                                        print_output('********************')
                                        print_output(combatant.name + ' summons all their might, and uses an Action Surge!')
                                        print_output('********************')
                                        combatant.action_surge -= 1
                                        combatant.action_used = False;
                                        print_output('<b>Action Surge action:</b>')
                                        action(combatant)                                
                                
                                    #print_output(combatant.name + "s new position: " + repr(combatant.position))
                        
                                    #Resolve events at the end of turn                                    
                                    print_output('<b>End of Turn:</b>')
                                    
                                    #Apply Hemorraging Critical damage
                                    resolve_hemo_damage(combatant)                   
                                
                                    # Update rage counter
                                    if combatant.raging:
                                        combatant.rage_duration += 1
                                    if combatant.raging and combatant.rage_duration >= combatant.max_rage_duration:
                                        print_output(combatant.name + ' cannot sustain their rage any longer, and it expires')
                                        combatant.raging = False
                                        # Resolve fatality to see if the combatant dies because of Rage Beyond Death
                                        resolve_fatality(combatant)

                                    print_output('That finishes ' + combatant.name + '\'s turn.')
                                else:
                                    print_output(combatant.name + ' has no valid targets! Team ' + combatant.team.name + ' wins!')
                                    combatant.team.no_of_wins += 1
                                    round_complete = True
                                    battle_complete = True
                            else:
                                print_output(combatant.name + ' is unconscious on the ground!')
                                # unconscious actions
                                if not combatant.conscious and combatant.current_health <= 0 and not combatant.stabilised:
                                    death_saving_throw(combatant)
                                    # See if they're dead
                                    resolve_fatality(combatant)
                    else:
                        print_output(combatant.name + ' is dead!')    
                        print_output("</br>")
                
                
            round_complete = True
            # End of round

        # After settings.max_rounds of combat, if no victor, declare stalemate
        if not battle_complete:
            print_output(repr(settings.max_rounds) + ' rounds of combat have passed, and there is no clear victor in the battle. Stalemate!')  
            battle_complete = True
        
        print_output('_____________________________________________________________________________')        
        print_output('<b>Attempt complete.</b>')
        print_output('_____________________________________________________________________________')
        # End of battle

    print_output("</br>")
    print_output('------------------------')
    print_output('Summary:')
    teams = []
    for combatant in combatants:
        if not combatant.team in teams:
            teams.append(combatant.team)
    for t in teams:
        print_output('Name: ' + t.name + ' ----- No. of wins: ' + repr(t.no_of_wins))
    
    #Close the output file if it is open
    close_file()    

def reset_simulation():
    # delete previous output file
    delete_file()
    settings.output = None
    settings.filename = None