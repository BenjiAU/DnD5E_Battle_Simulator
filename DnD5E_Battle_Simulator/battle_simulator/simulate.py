#Explicit imports
#Global settings
from battle_simulator import settings

#Generic combat initialisation functions
from battle_simulator import initialise_combat

#Hard-coded combatant values for initialisation
from battle_simulator import fighters

#The master list of combatants, shared between modules
from battle_simulator import combatants

# Combat functions
from battle_simulator import combat_functions

#Implicit imports
from .print_functions import *
from .combat_functions import *
from .classes import *

#System imports
import operator
from operator import itemgetter, attrgetter, methodcaller

def load_combatants():
    combatants.list = []
    combatants.teams = []
    fighters.initialise_combatants(combatants.list)
    fighters.initialise_teams(combatants.list,combatants.teams)    
    fighters.initialise_starting_positions(combatants.list)

def set_combatants(selected_combatants,selected_teams):
    for combatant in combatants.list:
        combatant_selected = False
        for selected_combatant in selected_combatants:
            if combatant.fullname == selected_combatant:
                combatant_selected = True
                #Retrieve the team object base don the team name for the same position element in 'selected teams'
                position = selected_combatants.index(selected_combatant)
                for team in combatants.teams:
                    # If the team name matches the name from the list in the same position as the combatant, and doesn't match the existing team name, update it
                    if team.name == selected_teams[position] and team.name != combatant.team.name:
                        #Swap the combatant to the selected team
                        combatant.team = team

        if not combatant_selected:
            combatants.list.remove(combatant)    

def simulate_battle():
    #Error handling
    error_occurred = False

    settings.init() # do only once
    set_output_file()            
    
    # Error checking
    if len(combatants.list) <= 1:
        print_output('Error: you must select at least two combatants to simulate a battle')
        error_occurred = True

    #for combatant in combatants.list:
        #if combatant.team
    #    print_output('Error: there must be at least 2 competing teams to battle')
    #    error_occurred = True

    attempt=0
    while attempt < settings.max_attempts and not error_occurred:
        # Beginning of battle attempt
        battle_complete = False        
        attempt += 1
        print_output('<b>Attempt number: ' + repr(attempt)+ '</b>')
        print_output(' ')      
        
        #Reset values on the global module list of combatants
        initialise_combat.reset_combatants(combatants.list)

        #Re-initialise position for new round
        initialise_combat.set_starting_positions(combatants.list)
            
        # roll initiative #        
        set_initiative_order()
        
        #print_output out combat order at top of attempt
        print_output("</br>")
        print_output('Combat order: ')
        combatorder = 0                   
        
        #Print initiative order and initialise targets
        for combatant in combatants.list:                   
            #Determine teams for battle
            for team in combatants.teams:
                if team.name == combatant.team.name:
                    team.battling = True

            combatorder += 1
            print_combatant_details(combatant,combatorder)
            find_target(combatant)
            print_output('</br>')
            print_output('</br>')

        #Begin combat rounds (up to a maximum to avoid overflow)
        round = 0              
        while not battle_complete and round < settings.max_rounds:
            # Beginning of round
            round_complete = False
            print_output("</br>")
            round = round + 1                
            print_output('<b>Round: ' + repr(round) + '</b>')
    
            for combatant in combatants.list:        
                if not round_complete:
                    print_output("</br>")
                    print_output('It is now ' + combatant.name + '\'s turn. Current HP: ' + repr(combatant.current_health) + '/' + repr(combatant.max_health))
                    turn_complete = False
                    while not turn_complete:
                        # Continuously evaluate this subloop only while combatant is alive/conscious; if these conditions change, skip out to death handling
                        combatant_alive_this_turn = False
                        while not turn_complete and combatant.alive and combatant.conscious:
                            combatant_alive_this_turn = True
                            # update statistics
                            combatant.rounds_fought += 1

                            # Re-evaluate targets
                            print_output('<b>Determining targets:</b>')
                            if combatant.target:                                
                                if not combatant.target.alive:
                                    #Aim for a new target as the current one is dead
                                    print_output(combatant.name + '\'s target is dead! Choosing new target...')
                                    find_target(combatant)
                            else:
                                find_target(combatant)
                                
                            #If we have not retrieved a target from the function, victory is declared for this team
                            if combatant.target:
                                # Targetable actions
                                print_output(combatant.name + ' is targetting: ' + combatant.target.name)

                                combatant.movement_used = False
                                combatant.action_used = False
                                combatant.bonus_action_used = False
                                combatant.reaction_used = False
                                
                                # Reset Hasted action if still under the effect of the Haste spell
                                if combatant.hasted:
                                    combatant.hasted_action_used = False;

                                #Divine Fury (resets at the start of each turn)
                                if combatant.divine_fury:
                                    combatant.divine_fury_used = False

                                # Sneak Attack (resets at the start of each turn)
                                if combatant.sneak_attack:
                                    combatant.sneak_attack_used = False

                                # Determine distance between targets and report if it is > 0
                                dist = calc_distance(combatant,combatant.target)
                                grids = calc_no_of_grids(dist)
                                if combatant.target and dist > 0:
                                    print_output('Distance to target: ' + repr(grids) + ' grid squares, or ' + repr(dist) + ' feet')

                                #check for breath weapon recharge
                                if combatant.creature_type == creature_type.Monster:
                                    if combatant.monster_type == monster_type.Ancient_Black_Dragon:
                                        if not combatant.breath_attack:
                                            breath_recharge(combatant)

                                # Can this combatant assassinate it's target? (Advantage on any creature that hasn't had a turn; critical on surprise)
                                if combatant.assassinate:
                                    if (round == 1) and (combatant.initiative_roll > combatant.target.initiative_roll):
                                        combatant.can_assassinate_target = True
                                    else:
                                        combatant.can_assassinate_target = False

                                # Is the combatant wearing equipment? Evaluate and use if appropriate
                                if combatant.equipment_inventory():
                                    print_output('<b>Use Equipment:</b>')                            
                                    use_equipment(combatant)

                                # use movement first #
                                print_output('<b>Movement:</b>')
                                movement(combatant)

                                if not combatant.conscious or not combatant.alive:
                                    break

                                # bonus action (pre-action)#       
                                print_output('<b>Bonus Action:</b>') 
                                bonus_action(combatant)     

                                if not combatant.conscious or not combatant.alive:
                                    break

                                # action #
                                print_output('<b>Action:</b>')
                                action(combatant)              
                                
                                if not combatant.conscious or not combatant.alive:
                                    break

                                # bonus action (post-action)#       
                                if not combatant.bonus_action_used:
                                    print_output('<b>Bonus Action:</b>') 
                                    bonus_action(combatant)            

                                if not combatant.conscious or not combatant.alive:
                                        break

                                # hasted action #
                                if combatant.hasted_action and not combatant.hasted_action_used:
                                    hasted_action(combatant)
                                    combatant.hasted_action_used = True
                                
                                if not combatant.conscious or not combatant.alive:
                                    break

                                # additional abilities (action surge etc.)
                                if combatant.action_surge > 0: 
                                    print_output('********************')
                                    print_output(combatant.name + ' summons all their might, and uses an Action Surge!')
                                    print_output('********************')
                                    combatant.action_surge -= 1
                                    combatant.action_used = False;
                                    print_output('<b>Action Surge action:</b>')
                                    action(combatant)                                
                                
                                if not combatant.conscious or not combatant.alive:
                                    break
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

                                #Mark the turn as complete
                                print_output('That finishes ' + combatant.name + '\'s turn.')
                                turn_complete = True
                            else:
                                print_output('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                                print_output('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                                print_output('~~~~~~~~~~~~~')
                                print_output(combatant.name + ' has no valid targets! ' + combatant.team.name + ' wins!')
                                print_output('~~~~~~~~~~~~~')
                                print_output('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                                print_output('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                                
                                for team in combatants.teams:
                                    if team.battling and team.name == combatant.team.name:
                                        team.no_of_wins += 1

                                turn_complete = True
                                round_complete = True
                                battle_complete = True

                        # Handle unconsciousness/death
                        if combatant.alive and not combatant.conscious:
                            print_output(combatant.name + ' is unconscious on the ground!')
                            # Unconscious actions
                            # If we're struck down by something on our turn, we don't need to death save til next turn
                            if not combatant_alive_this_turn:
                                if not combatant.conscious and combatant.current_health <= 0 and not combatant.stabilised:
                                    death_saving_throw(combatant)
                                    # See if they're dead
                                    resolve_fatality(combatant)                           
                            turn_complete = True
                        elif not combatant.alive and not combatant.conscious:
                            print_output(combatant.name + ' is dead!')    
                            print_output("</br>")
                            turn_complete = True                                                                       

                    #End of Turn
                    turn_complete = True
                    #End of Turn
            #End of Round
            round_complete = True
            #End of Round

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
    print_output('<b>Simulation Complete</b>')
    print_output('------------------------')
    
    # Summary
    print_output('<b>Combatant Summary:</b>')

    for combatant in combatants.list:
        print_summary(combatant)            
    
    print_output('------------------------')
    print_output('<b>Team Summary:</b>')
    print_output('**************************')
    for team in combatants.teams:
        if team.battling and team.no_of_wins > 0:
            print_output(team.name + ' ----- No. of wins: ' + repr(team.no_of_wins))
    
    #Close the output file if it is open    
    close_file()    

def reset_simulation():
    # delete previous output file
    delete_file()
    settings.output = None
    settings.filename = None

def set_initiative_order():    
    namestring = ""
    unsorted_combatants = combatants.list
    #Roll initiative for each combatant
    for combatant in unsorted_combatants:     
        if namestring == '':
            namestring += combatant.name
        else:
            namestring += ', ' + combatant.name
        combat_functions.roll_initiative(combatant)            
                            
    initkey = operator.attrgetter("initiative_roll")
    combatants.list = sorted(unsorted_combatants, key=initkey,reverse=True)    
    namestring += ': I need you to roll initiative!'
    print_output(namestring)

    for combatant in combatants.list:
        print_output(indent() + 'Name:' + combatant.name + ': Initiative Roll: ' + repr(combatant.initiative_roll))
    