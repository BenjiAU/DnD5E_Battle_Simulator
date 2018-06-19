#Explicit imports
#Global settings
from battle_simulator import settings

#Generic combat initialisation functions
from battle_simulator import initialise_combat

#Hard-coded combatant values for initialisation
from battle_simulator import fighters

#The master list of combatants, shared between modules
from battle_simulator import combatants

#Implicit imports
from battle_simulator.classes import *
from battle_simulator.print_functions import *
from battle_simulator.combat_functions.action import *
from battle_simulator.combat_functions.target import *
from battle_simulator.combat_functions.inventory import *
from battle_simulator.combat_functions.position import *
from battle_simulator.combat_functions.conditions import *

#System imports
import operator
from operator import itemgetter, attrgetter, methodcaller

def load_combatants():
    combatants.list = []
    combatants.teams = []
    fighters.initialise_combatants(combatants.list)
    fighters.initialise_teams(combatants.list,combatants.teams)    
    fighters.randomise_starting_positions(combatants.list)    

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
    if len(combatants.list) > 1:
        enemy_found = False        
        first_team_name = ""
        for combatant in combatants.list:       
            if first_team_name == "":
                first_team_name = combatant.team.name
            if combatant.team.name != first_team_name:
                enemy_found = True
        if not enemy_found:
            print_output('Error: there must be at least 2 competing teams to battle. Change the combatants, or change the Team that the combatant belongs to in order to simulate a battle.')
            error_occurred = True
    else:
        print_output('Error: you must select at least two combatants to simulate a battle.')
        error_occurred = True    

    attempt=0
    while attempt < settings.max_attempts and not error_occurred:
        # Beginning of battle attempt
        battle_complete = False        
        attempt += 1
        print_output('<b>Attempt number: ' + repr(attempt)+ '</b>')
        print_output(' ')      
        
        #Reset values on the global module list of combatants
        print_output('<bResetting Combatants...</b>')
        initialise_combat.reset_combatants(combatants.list)

        #Re-initialise position for new round
        initialise_combat.set_starting_positions(combatants.list)
            
        # roll initiative #        
        print_output('<b>Rolling Initiative...</b>')
        set_initiative_order()
        
        #print_output out combat order at top of attempt
        print_output("</br>")
        print_output('Combat order established: ')
        combatorder = 0                   
        
        #Print initiative order and initialise targets
        begin_combatant_details()
        for combatant in combatants.list:                   
            #Determine teams for battle            
            for team in combatants.teams:
                if team.name == combatant.team.name:
                    team.battling = True

            combatorder += 1            
            print_combatant_details(combatant,combatorder)
            if find_target(combatant):                
                weapon_swap(combatant,calc_distance(combatant,combatant.target))               
        end_combatant_details()

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
                    print_output('It is now ' + combatant.name + '\'s turn. ' + hp_text(combatant.current_health,combatant.max_health) + '. ' + position_text(combatant.xpos,combatant.ypos))
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
                                    if find_target(combatant):                
                                        weapon_swap(combatant,calc_distance(combatant,combatant.target))   
                            else:
                                if find_target(combatant):                
                                    weapon_swap(combatant,calc_distance(combatant,combatant.target))   
                                
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


                                ### Begin actual turn operations ###
                                if check_condition(combatant,condition.Incapacitated):
                                    print_output(combatant.name + ' is incapacitated, and incapable of any action this turn!')
                                else:
                                    # Is the combatant wearing equipment? Evaluate and use if appropriate
                                    if combatant.equipment_inventory():
                                        print_output('<b>Use Equipment:</b>')                            
                                        use_equipment(combatant)

                                    # bonus action (pre-movement)#       
                                    if not combatant.bonus_action_used:                                    
                                        bonus_action(combatant)      

                                    # use movement first #
                                    print_output('<b>Movement:</b>')
                                    movement(combatant)

                                    if not combatant.conscious or not combatant.alive:
                                        break

                                    # bonus action (pre-action)#       
                                    if not combatant.bonus_action_used:                                    
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
                                        # Don't blow action surge if current target is down; find a new target instead
                                        if not combatant.target.alive or not combatant.target.conscious:
                                            find_target(combatant)
                                        # If we still have a target, use our action surge
                                        if combatant.target:
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
                        
                                ### END OF TURN ACTIONS ###

                                #Resolve events at the end of turn                                    
                                print_output('<b>End of Turn:</b>')
                                
                                # Update the duration counter on any conditions currently suffered by the combatant
                                update_conditions(combatant)

                                #Apply Hemorraging Critical damage
                                resolve_hemo_damage(combatant)                   
                                if not combatant.conscious or not combatant.alive:
                                    break
                                
                                # Resolve Head Shot status
                                if combatant.head_shotted:
                                    print_output(combatant.name + ' shakes off the effects of the Head Shot, and no longer has disadvantage on attacks!')
                                    combatant.head_shotted = False
                                    combatant.has_disadvantage = False

                                # Update rage counter
                                if combatant.raging:
                                    combatant.rage_duration += 1
                                if combatant.raging and combatant.rage_duration >= combatant.max_rage_duration:
                                    print_output(combatant.name + ' cannot sustain their rage any longer, and it expires')
                                    combatant.raging = False                                    
                                    # Resolve fatality to see if the combatant dies because of Rage Beyond Death
                                    resolve_fatality(combatant)

                                # Turn completion events
                                # Reset sneak attack on anyone who used sneak attack (i.e. opportunity attacks)
                                for sneak_attack_combatant in combatants.list:
                                    if sneak_attack_combatant.sneak_attack:
                                        sneak_attack_combatant.sneak_attack_used = False

                                #Mark the turn as complete
                                print_output('That finishes ' + combatant.name + '\'s turn.')

                                turn_complete = True
                            else:
                                print_output(victory_text(combatant.name + ' has no valid targets! ' + combatant.team.name + ' wins!'))
                                                                
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

                    #Turn Over
                    turn_complete = True
                    #Turn Over
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

    if not error_occurred:
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
                print_output(victory_text(team.name + ' ----- No. of wins: ' + repr(team.no_of_wins)))
    
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
        roll_initiative(combatant)            
                            
    initkey = operator.attrgetter("initiative_roll")
    combatants.list = sorted(unsorted_combatants, key=initkey,reverse=True)    
    namestring += ': I need you to roll initiative!'
    print_output(namestring)

    for combatant in combatants.list:
        print_output(indent() + 'Name:' + combatant.name + ': Initiative Roll: ' + repr(combatant.initiative_roll))
    