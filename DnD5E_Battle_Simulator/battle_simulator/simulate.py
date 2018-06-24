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
        #Gag output (to stop weapon/target/roll spam at the start of the sim)
        settings.suppress_output = True

        # Beginning of battle attempt
        battle_complete = False        
        attempt += 1                
        
        #Reset values on the global module list of combatants
        print_output('<bResetting Combatants...</b>')
        initialise_combat.reset_combatants(combatants.list)

        #Re-initialise position for new round
        initialise_combat.set_starting_positions(combatants.list)
            
        # roll initiative #                
        set_initiative_order()
        
        #print_output out combat order at top of attempt        
        combatorder = 0                   
        
        #Remove the gag on output (to stop weapon/target/roll spam at the start of the sim)
        settings.suppress_output = False
        begin_div('attempt')
        print_output('<b>Attempt number: ' + repr(attempt)+ '</b>')
        print_output('<b>Rolling Initiative...</b>')
        print_output('Combat order established: ')

        #Print initiative order and initialise targets        
        begin_combatant_details()
        for combatant in combatants.list:                   
            #Determine teams for battle            
            for team in combatants.teams:
                if team.name == combatant.team.name:
                    team.battling = True

            combatorder += 1            
            print_combatant_details(combatant,combatorder)
        end_combatant_details()
        print_output("")

        #Begin combat rounds (up to a maximum to avoid overflow)
        round = 0              
        print_output('<b>Beginning combat round simulation...</b>')
        while not battle_complete and round < settings.max_rounds:
            begin_div('round')
            # Beginning of round
            round_complete = False
            round = round + 1                
            print_output('<b>Round: ' + repr(round) + '</b>')
            
            #Print a grid 50 units around the combatants to show the relative positions    
            print_grid(0,0,[],combatants.list)            

            for combatant in combatants.list:        
                if not round_complete:
                    begin_div('turn')
                    print_output('It is now ' + combatant.name + '\'s turn. ' + hp_text(combatant.alive,combatant.current_health,combatant.max_health) + '. ' + position_text(combatant.xpos,combatant.ypos))
                    turn_complete = False                    
                    while not turn_complete:
                        # Continuously evaluate this subloop only while combatant is alive/conscious; if these conditions change, skip out to death handling
                        combatant_alive_this_turn = False
                        while not turn_complete and combatant.alive and not check_condition(combatant,condition.Unconscious):                            
                            combatant_alive_this_turn = True
                            # update statistics
                            combatant.rounds_fought += 1

                            # Re-evaluate targets                            
                            if find_target(combatant):                
                                weapon_swap(combatant,calc_distance(combatant,combatant.target))   
                                
                            #If we have not retrieved a target from the function, victory is declared for this team
                            if combatant.target:
                                combatant.movement_used = False
                                combatant.action_used = False
                                combatant.bonus_action_used = False
                                combatant.bonus_action_spell_casted = False
                                combatant.reaction_used = False
                                
                                # Reset the granted actions provided by various conditions (i.e. Haste)
                                for combatant_condition in combatant.creature_conditions():
                                    if combatant_condition.grants_action:
                                        combatant_condition.granted_action_used = False                                

                                #Divine Fury (resets at the start of each turn)
                                if combatant.divine_fury:
                                    combatant.divine_fury_used = False

                                # Sneak Attack (resets at the start of each turn)
                                if combatant.sneak_attack:
                                    combatant.sneak_attack_used = False                                

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

                                # Update concentration, to end the concentration effect if the targets were were concentrating on saved against the spell effects etc.
                                update_concentration(combatant)

                                ### Begin actual turn operations ###
                                if not continue_turn(combatant):
                                    break
                                    
                                # Is the combatant wearing equipment? Evaluate and use if appropriate
                                if combatant.equipment_inventory():                                        
                                    use_equipment(combatant)

                                # bonus action (pre-movement)#       
                                if not combatant.bonus_action_used:                                    
                                    bonus_action(combatant)      

                                # use movement first #
                                movement(combatant)

                                if not continue_turn(combatant):
                                    break

                                # bonus action (pre-action)#       
                                if not combatant.bonus_action_used:                                    
                                    bonus_action(combatant)     

                                if not continue_turn(combatant):
                                    break

                                # action #
                                action(combatant)              
                                
                                if not continue_turn(combatant):
                                    break

                                # bonus action (post-action)#       
                                if not combatant.bonus_action_used:                                    
                                    bonus_action(combatant)            

                                if not continue_turn(combatant):
                                    break

                                # hasted action #
                                for combatant_condition in combatant.creature_conditions():
                                    if combatant_condition.grants_action and not combatant_condition.granted_action_used:
                                        #Hasted condition (hasted action has limits on what can be done)
                                        if combatant_condition.condition == condition.Hasted:
                                            hasted_action(combatant)
                                            combatant_condition.granted_action_used = True
                                
                                if not continue_turn(combatant):
                                    break

                                # additional abilities (action surge etc.)                                    
                                if combatant.action_surge > 0: 
                                    # Reassess targets
                                    if find_target(combatant):
                                        # Don't blow action surge if current target is down; find a new target instead
                                        if combatant.target.alive and not check_condition(combatant.target,condition.Unconscious):
                                            print_output('********************')
                                            print_output(combatant.name + ' summons all their might, and uses an Action Surge!')
                                            print_output('********************')
                                            combatant.action_surge -= 1
                                            combatant.action_used = False;
                                            print_output('<b>Action Surge action:</b>')
                                            action(combatant)                                
                                
                                if not continue_turn(combatant):
                                    break
                                #print_output(combatant.name + "s new position: " + repr(combatant.position))
                        
                                ### END OF TURN ACTIONS ###

                                #Resolve events at the end of turn                                    
                                print_output('<b>End of Turn:</b>')
                                
                                # Update the duration counter on any conditions currently suffered by the combatant
                                update_conditions(combatant)

                                # Resolve fatality to see if the combatant dies because of expired conditions
                                resolve_fatality(combatant)

                                if check_condition(combatant,condition.Unconscious) or not combatant.alive:
                                    break

                                #Apply Hemorraging Critical damage
                                resolve_hemo_damage(combatant)                   

                                if check_condition(combatant,condition.Unconscious) or not combatant.alive:
                                    break
                                                                
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
                        if combatant.alive and check_condition(combatant,condition.Unconscious):
                            print_output(combatant.name + ' is unconscious on the ground!')
                            # Unconscious actions
                            # If we're struck down by something on our turn, we don't need to death save til next turn
                            if not combatant_alive_this_turn:
                                if check_condition(combatant,condition.Unconscious) and combatant.current_health <= 0 and not combatant.stabilised:
                                    death_saving_throw(combatant)
                                    # See if they're dead
                                    resolve_fatality(combatant)                           
                            turn_complete = True
                        elif not combatant.alive and check_condition(combatant,condition.Unconscious):
                            print_output(combatant.name + ' is dead!')    
                            print_output("")
                            turn_complete = True                                                                       

                    #Turn Over
                    turn_complete = True
                    end_div()
                    #Turn Over
            #End of Round
            round_complete = True
            end_div()
            #End of Round

        # After settings.max_rounds of combat, if no victor, declare stalemate
        if not battle_complete:
            print_output(repr(settings.max_rounds) + ' rounds of combat have passed, and there is no clear victor in the battle. Stalemate!')  
            battle_complete = True
        

        print_output('<b>Attempt complete.</b>')        
        end_div()
        # End of battle

    if not error_occurred:
        print_output("")
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
        roll_initiative(combatant)            
                            
    initkey = operator.attrgetter("initiative_roll")
    combatants.list = sorted(unsorted_combatants, key=initkey,reverse=True)    

    for combatant in combatants.list:
        print_indent( 'Name:' + combatant.name + ': Initiative Roll: ' + repr(combatant.initiative_roll))
    