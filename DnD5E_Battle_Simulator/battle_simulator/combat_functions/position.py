#Explicit imports
from battle_simulator import combatants

#Implicit imports
from battle_simulator.classes import *
from battle_simulator.print_functions import *
from battle_simulator.combat_functions.conditions import *

from . import combat 

from copy import copy

### Core Round functions ###
def movement(combatant):
    # Only move if a target exists
    if combatant.target:
        # combatant.movement #
        combatant.movement = combatant.speed
        if combatant.hasted:
            combatant.movement = combatant.movement * 2
        use_movement(combatant)

    combatant.movement_used = True

def use_movement(combatant):
    # Goal: make sure we're in range to use our attacks/abilities if we have available
    # If we're a melee fighter, try to close the gap
    # If we're a ranged fighter, try to keep at maximum range (but don't run off into the wilderness)

    if combatant.prone:
        # Spend half combatant.movement to get up #
        combatant.movement = math.floor(combatant.movement/2)
        print_output(combatant.name + ' spends ' + repr(combatant.movement) + ' feet of movement to stand up from prone')            
        combatant.prone = False

    # Are we wielding a melee weapon that we cannot throw?
    if (combatant.main_hand_weapon.range == 0) and not (combatant.main_hand_weapon.thrown):                    
        if target_in_weapon_range(combatant,combatant.target,combatant.main_hand_weapon.range):            
            print_output(combatant.name + ' stays where they are, in melee range of ' + combatant.target.name + '. ' + position_text(combatant.xpos,combatant.ypos))
        else:
            move_to_target(combatant,combatant.target)    
    else:
        #Otherwise use the range of the weapon to determine where to move 
        if target_in_weapon_range(combatant,combatant.target,combatant.main_hand_weapon.range):               
            # Don't move out of weapon range - figure out current gap, subtract it from weapon range, thats how far we can move           
            if combatant.movement > combatant.main_hand_weapon.range - calc_distance(combatant,combatant.target):
                # Set our movement to the maximum range            
                combatant.movement = combatant.main_hand_weapon.range - calc_distance(combatant,combatant.target)                             
            # Movement must be at least higher than one grid or its not worth using
            if combatant.movement >= 5:
                print_output(combatant.name + ' will attempt to use ' + repr(combatant.movement) + ' feet of movement to increase distance, but stay within weapon range of ' + combatant.target.name)
                move_from_target(combatant,combatant.target)
        else:
            #Close the distance to be able to use weapon 

            gap_to_close = calc_distance(combatant,combatant.target) - combatant.main_hand_weapon.range;
            if gap_to_close <= combatant.movement:
                combatant.movement = gap_to_close
            if combatant.movement >= 5:
                print_output(combatant.name + ' will attempt to use ' + repr(combatant.movement) + ' feet of movement to get within weapon range of ' + combatant.target.name)
                move_to_target(combatant,combatant.target)

# Position/movement functions
def getposition(combatant):
    return(combatant.xpos,combatant.ypos)

def move_grid(combatant,direction):
    if direction == cardinal_direction.Stay:
        return 

    # Round positions to the nearest 5 for simplicity
    initialxpos = round_to_integer(combatant.xpos,5)
    initialypos = round_to_integer(combatant.ypos,5)
    
    #1 = Southwest
    #2 = South
    #3 = Southeast
    #4 = East
    #5 = NorthEast
    #6 = North
    #7 = Northwest
    #8 = West    
    #9 = Random

    if direction == None or direction == cardinal_direction.Random:       
        rand_direction = random.randint(1,8)
        direction = cardinal_direction(rand_direction)

        if settings.verbose_movement:
            print_output(indent() + combatant.name + ' chooses to travel ' + direction.name)
    
    xpos = 0
    ypos = 0

    xpos,ypos = calc_grid_step(direction,xpos,ypos)    

    # Evaluate opportunity attacks
    new_xpos = initialxpos + xpos 
    new_ypos = initialypos + ypos
    
    if settings.verbose_movement:
        print_output(indent() + combatant.name + ' attempts to move ' + direction.name + ' from (' + repr(initialxpos) + ',' + repr(initialypos) + ') to (' + repr(new_xpos) + ',' + repr(new_ypos) + ')')

    #Check that the grid is not occupied
    other_combatants = all_other_combatants(combatant)
    for other_combatant in other_combatants:
        if (other_combatant.xpos == new_xpos) and (other_combatant.ypos == new_ypos):
            #Force any other combatant in those positions to block movement through that square
            print_output(indent() + movement_text(combatant.name + ' failed to move - ' + other_combatant.name + ' is blocking them at (' + repr(new_xpos) + ',' + repr(new_ypos) + ')!'))
            return False

    #Check for opportunity attacks
    evaluate_opportunity_attacks(combatant,new_xpos,new_ypos)    

    if combatant.movement > 0 and not combatant.prone:        
        combatant.xpos = new_xpos
        combatant.ypos = new_ypos
        # Update movement
        combatant.movement -= 5
        if settings.verbose_movement:
            print_output(indent() + combatant.name + ' successfully moved, spending 5 points of movement (Remaining Movement: ' + repr(combatant.movement) + ' feet.)')
        return True
    else:        
        if settings.verbose_movement:
            print_output(indent() + movement_text(combatant.name + ' failed to move - they have no movement remaining!'))            
        return False

def calc_distance(combatant,target):
    xdistance = int(math.fabs(combatant.xpos-target.xpos))
    ydistance = int(math.fabs(combatant.ypos-target.ypos))
    return int(math.sqrt((xdistance * xdistance) + (ydistance * ydistance)))

def derive_cardinal_direction(x1,x2,y1,y2):
    direction = cardinal_direction.Stay
    if x1 > x2 and y1 > y2:
        direction = cardinal_direction.SouthWest
    elif x1 > x2 and y1 < y2:
        direction = cardinal_direction.NorthWest
    elif x1 < x2 and y1 < y2:
        direction = cardinal_direction.NorthEast
    elif x1 < x2 and y1 > y2:
        direction = cardinal_direction.SouthEast
    elif x1 < x2 and y1 == y2:
        direction = cardinal_direction.East
    elif x1 > x2 and y1 == y2:
        direction = cardinal_direction.West
    elif x1 == x2 and y1 < y2:
        direction = cardinal_direction.North
    elif x1 == x2 and y1 > y2:
        direction = cardinal_direction.South
    return(direction)

def derive_perpendicular(direction):
    if direction == cardinal_direction.North:
        perpendicular = cardinal_direction.East        
    elif direction == cardinal_direction.NorthEast:        
        perpendicular = cardinal_direction.SouthEast
    elif direction == cardinal_direction.East:
        perpendicular = cardinal_direction.South        
    elif direction == cardinal_direction.SouthEast:
        perpendicular = cardinal_direction.SouthWest
    elif direction == cardinal_direction.South:
        perpendicular = cardinal_direction.West
    elif direction == cardinal_direction.SouthWest:
        perpendicular = cardinal_direction.NorthWest
    elif direction == cardinal_direction.West:
        perpendicular = cardinal_direction.North
    elif direction == cardinal_direction.NorthWest:
        perpendicular = cardinal_direction.NorthEast
    return(perpendicular)
        
def calc_grid_step(direction,x,y):    
    if direction == cardinal_direction.SouthWest:
        x = -5
        y = -5
    elif direction == cardinal_direction.South:
        x = 0
        y = -5
    elif direction == cardinal_direction.SouthEast:
        x = 5
        y = -5
    elif direction == cardinal_direction.East:
        x = 5
        y = 0
    elif direction == cardinal_direction.NorthEast:
        x = 5
        y = 5
    elif direction == cardinal_direction.North:
        x = 0
        y = 5
    elif direction == cardinal_direction.NorthWest:
        x = -5
        y = 5
    elif direction == cardinal_direction.West:
        x = -5
        y = 0
    return(x,y)

def move_to_target(combatant,target):
    # Goal - decrease the distance between us and target
    print_output(movement_text(combatant.name + ' is currently located at position: (' + repr(combatant.xpos) + ',' + repr(combatant.ypos) + '), and wants to move towards ' + combatant.target.name + ' at (' + repr(combatant.target.xpos) + ',' + repr(combatant.target.ypos) + ')'))    
    print_output(movement_text(combatant.name + ' begins to use their ' + repr(combatant.movement) + ' feet of movement.'))
    initial_distance = calc_distance(combatant,target)
    initial_grids = calc_no_of_grids(initial_distance)
    grids_to_move = calc_no_of_grids(initial_distance)
    initial_grid_movement = calc_no_of_grids(combatant.movement)
    grid_movement = calc_no_of_grids(combatant.movement)
    movement_complete = False

    if settings.verbose_movement:
        print_output(combatant.name + ' has ' + repr(initial_grid_movement) + ' grids, or ' + repr(combatant.movement) + ' feet of movement to spend. (Distance to destination: ' + repr(initial_grids) + ' grids, or ' + repr(initial_distance) + ' feet)')

    grids_moved = 0    
    while grids_to_move > 0 and grid_movement > 0:      
        initial_xpos = combatant.xpos
        initial_ypos = combatant.ypos

        if settings.verbose_movement:
            print_output(indent() + combatant.name + ' is ' + repr(grids_to_move) + ' grids away from their destination and has ' + repr(grid_movement) + ' grids of movement remaining')

        #x1,x2,y1,y2
        direction = derive_cardinal_direction(combatant.xpos,target.xpos,combatant.ypos,target.ypos)
        
        grid_moved = False
        while not grid_moved:
            if move_grid(combatant,direction):
                grid_moved = True
            else:
                # The desired direction failed (because of prone, another character blocking square etc.)
                # Try moving perpendicular to the desired direction (this should let us move around on the next tick)
                direction = derive_perpendicular(direction)
                if move_grid(combatant,direction):
                    grid_moved = True
                else:
                    # Move in a random direction to see if that lets us get around the obstacle on the next tick (as we derive a new path to target0
                    direction = cardinal_direction.Random
                    if move_grid(combatant,direction):
                        grid_moved = True             
                    else:
                        print_output('Could not move!')
                        grid_moved = True             

        grids_moved += 1
        #Evaluate after each step if the target is in range of our weapon
        if target_in_weapon_range(combatant,combatant.target,combatant.main_hand_weapon.range):                        
            print_output(movement_text(combatant.name + ' skids to a halt, now in range of ' + combatant.target.name + '. ') + position_text(combatant.xpos,combatant.ypos))
            movement_complete = True

            grids_to_move = 0
            grid_movement = 0

        grids_to_move -= 1
        grid_movement -= 1
    
    if not movement_complete:
        print_output(movement_text(combatant.name + ' has used all of their available movement. ') + position_text(combatant.xpos,combatant.ypos))
        movement_complete = True

def move_from_target(combatant,target):
    # Goal - extend the distance between us and target
    #Essentially figure out where we are in relation to the target, and keep travelling in that direction
    print_output(movement_text(combatant.name + ' is currently located at position: (' + repr(combatant.xpos) + ',' + repr(combatant.ypos) + '), and wants to move away from ' + combatant.target.name + ' at (' + repr(combatant.target.xpos) + ',' + repr(combatant.target.ypos) + ')'))
    print_output(movement_text(combatant.name + ' has ' + repr(combatant.movement) + ' feet of movement to spend.'))
    initial_distance = combatant.movement
    initial_grids = calc_no_of_grids(initial_distance)    

    grids_to_move = calc_no_of_grids(initial_distance)
    grid_movement = calc_no_of_grids(combatant.movement)
    
    if settings.verbose_movement:
        print_output(combatant.name + ' has ' + repr(grid_movement) + ' grids, or ' + repr(combatant.movement) + ' feet of movement to spend. (Distance to destination: ' + repr(initial_grids) + ' grids, or ' + repr(initial_distance) + ' feet)')

    grids_moved = 0
    while grids_to_move > 0 and grid_movement > 0:
        initial_xpos = combatant.xpos
        initial_ypos = combatant.ypos

        if settings.verbose_movement:
            print_output(indent() + combatant.name + ' is ' + repr(grids_to_move) + ' grids away from their destination and has ' + repr(grid_movement) + ' grids of movement remaining')

        direction = cardinal_direction.Stay

        #Note that this is the inverse of the derive_direction function and has to be replicated here 
        if combatant.xpos == target.xpos and combatant.ypos == target.ypos:
            #Choose a random direction to move in         
            direction = cardinal_direction.Random
        elif combatant.xpos > target.xpos and combatant.ypos > target.ypos:
            direction = cardinal_direction.NorthEast
        elif combatant.xpos > target.xpos and combatant.ypos < target.ypos:
            direction = cardinal_direction.SouthEast
        elif combatant.xpos < target.xpos and combatant.ypos < target.ypos:
            direction = cardinal_direction.SouthWest
        elif combatant.xpos < target.xpos and combatant.ypos > target.ypos:
            direction = cardinal_direction.NorthWest
        elif combatant.xpos < target.xpos and combatant.ypos == target.ypos:
            direction = cardinal_direction.West
        elif combatant.xpos > target.xpos and combatant.ypos == target.ypos:
            direction = cardinal_direction.East
        elif combatant.xpos == target.xpos and combatant.ypos < target.ypos:
            direction = cardinal_direction.South
        elif combatant.xpos == target.xpos and combatant.ypos > target.ypos:
            direction = cardinal_direction.North
                   
        
        if direction != cardinal_direction.Stay:
            grid_moved = False
            while not grid_moved:
                if move_grid(combatant,direction):
                    grid_moved = True
                else:
                    # The desired direction failed (because of prone, another character blocking square etc.)
                    # Try moving perpendicular to the desired direction (this should let us move around on the next tick)
                    direction = derive_perpendicular(direction)
                    if move_grid(combatant,direction):
                        grid_moved = True
                    else:
                        # Move in a random direction to see if that lets us get around the obstacle on the next tick (as we derive a new path to target0
                        direction = cardinal_direction.Random
                        if move_grid(combatant,direction):
                            grid_moved = True             
                        else:
                            #Movement failed for some other reason
                            grid_moved = True             
        
        #If we haven't attacked yet, we don't want to run out of our weapon range
        #If combatant.movement would take us outside the maximum range of our weapon, stop here instead
        if not combatant.action_used: 
            if not target_in_weapon_range(combatant,combatant.target,combatant.main_hand_weapon.range):                        
                print_output(indent() + combatant.name + ' changes their mind at the last second, moving back to (' + repr(initial_xpos) + ',' + repr(initial_ypos) + ') to stay in weapon range of ' + combatant.target.name)
                combatant.xpos = initial_xpos;
                combatant.ypos = initial_ypos;
                grids_to_move = 0
                grid_movement = 0

        grids_to_move -= 1
        grid_movement -= 1

    print_output(movement_text(combatant.name + ' is now located at position: (' + repr(combatant.xpos) + ',' + repr(combatant.ypos) + ')'))    
    
def calc_no_of_grids(distance):
    return(int(round(math.fabs(distance/5))))

def get_living_enemies(combatant):
    enemies = []
    for potential_enemy in combatants.list:
        if combatant.name != potential_enemy.name and combatant.team != potential_enemy.team:
            if potential_enemy.alive:                
                enemies.append(potential_enemy)
    return enemies

def all_other_combatants(combatant):
    targets = []
    for target in combatants.list:
        if combatant.name != target.name:
            if target.alive:                
                targets.append(target)
    return targets

def determine_enemy_positions(combatant):        
    enemy_positions = []
    for potential_enemy in combatants.list:
        if combatant.name != potential_enemy.name and combatant.team != potential_enemy.team:
            if potential_enemy.alive:                
                enemy_positions.add((potential_enemy.xpos,potential_enemy.ypos))
    return enemy_positions

def target_in_weapon_range(combatant,target,range):
    if range == 0:        
        range = melee_range()
    #Calculate distance in feet
    distance_to_target = calc_distance(combatant,target)
    if (distance_to_target <= range) or (combatant.main_hand_weapon.reach and distance_to_target < range + 5):
        return True
    #Check that no grids are adjacent for melee attacks
    if is_adjacent(combatant,target):
        return True
    return False

def enemy_in_melee_range(combatant,excluded_combatant):
    enemies = get_living_enemies(combatant)
    for enemy in enemies:
        if is_adjacent(combatant,enemy) and enemy != excluded_combatant:
            return True

    return False

def melee_range():
    #Treating default melee weapon range as 5 feet, upped to 8 to avoid clipping issues on corners of grid
    return 8

def is_adjacent(combatant,target):
    if (combatant.xpos == target.xpos) or (combatant.xpos == target.xpos-5) or (combatant.xpos == target.xpos+5):
        if (combatant.ypos == target.ypos) or (combatant.ypos == target.ypos-5) or (combatant.ypos == target.ypos+5):
            return True
    elif (combatant.ypos == target.ypos) or (combatant.ypos == target.ypos-5) or (combatant.ypos == target.ypos+5):
        if (combatant.xpos == target.xpos) or (combatant.xpos == target.xpos-5) or (combatant.xpos == target.xpos+5):
            return True
    return False

def evaluate_opportunity_attacks(combatant_before_move,new_xpos,new_ypos):
    # Create a copy of the combatant to capture the new co-ordinate and compare to existing co-ordiantes (basically casting forward and simulating the movement)
    combatant_after_move = creature()
    combatant_after_move = copy(combatant_before_move)
    combatant_after_move.xpos = new_xpos
    combatant_after_move.ypos = new_ypos

    #Evaluate for each enemy unit
    enemies = get_living_enemies(combatant_before_move)
    for opportunity_attacker in enemies:                
        #Only conscious enemies with capacity can make an opportunity attack
        if opportunity_attacker.conscious and not check_condition(opportunity_attacker,condition.Incapacitated):
            # Evaluate only if reaction available
            if not opportunity_attacker.reaction_used:
                # Only provoke opportunity attacks for melee weapons
                if opportunity_attacker.main_hand_weapon.range == 0:
                    # If the enemy is currently adjacent, but would not be after movement, condition is fulfilled
                    # Note - this will not work with Reach weapons, will need additional conditions to handle Reach
                    # This won't play nice with Multiattack? May need a new function to evaluate if any instant-equippable weapon would trigger the OA
                    if is_adjacent(opportunity_attacker,combatant_before_move) and not is_adjacent(opportunity_attacker,combatant_after_move):                    
                        #Swap targets if necessary
                        original_target = opportunity_attacker.target 
                        if opportunity_attacker.target != combatant_before_move:                            
                            opportunity_attacker.target = combatant_before_move

                        # Make the attack out of sequence
                        print_output('-------------------------------------------------------------------------------------------------------------------------')
                        print_output(combatant_before_move.name + '\'s movement has triggered an Attack of Opportunity from ' + opportunity_attacker.name + ' !')                        
                        print_output('Resolving Attack of Opportunity!')                            
                        if combatant_before_move.disengaged:
                            print_output(opportunity_attacker.name + ' can not make an Attack of Opportunity against ' + combatant_before_move.name + ', as they have Disengaged!')
                        else:
                            if combat.attack(opportunity_attacker,opportunity_attacker.main_hand_weapon):
                                for feat in opportunity_attacker.creature_feats():
                                    if feat == feat.Sentinel:
                                        #Successful opportunity attacks reduce creatures speed to 0
                                        combatant_before_move.movement = 0
                                        print_output(opportunity_attacker.name + ' uses their Sentinel feat to reduce ' + combatant_before_move.name + '\'s remaining movement to 0!')                        
                            print_output('The Attack of Opportunity has been resolved! ' + opportunity_attacker.name + ' has spent their reaction')                        
                            print_output('-------------------------------------------------------------------------------------------------------------------------')
                            # Consume reaction
                            opportunity_attacker.reaction_used = True

                        # Reset target
                        opportunity_attacker.target = original_target