#Explicit imports
from battle_simulator import combatants

#Implicit imports
from battle_simulator.classes import *
from battle_simulator.print_functions import *
from battle_simulator.combat_functions.position import * 
from battle_simulator.combat_functions.generics import *
from battle_simulator.combat_functions.conditions import check_condition

def find_target(combatant):    
    #Always set the target as a reference to the master list of combatants (to avoid having to constantly refresh to pick up changes in the target)
    original_target = combatant.target
    combatant.target = None    
    best_target = None
    for enemy in get_living_enemies(combatant):                   
        #Target selection priority:                     
        if not check_condition(enemy,condition.Unconscious):                                
            # If we have no target, choose this enemy
            if best_target == None:
                best_target = enemy    
                
            # If the enemy is within our range, and closer to us than the current target, swap to this enemy
            if calc_distance(combatant,enemy) <= combatant.desired_range:
                best_target = enemy
            #If the enemy is closer than the current target, swap to it
            elif calc_distance(combatant,enemy) < calc_distance(combatant,best_target):                
                best_target = enemy                            

    #If we do not have a target, allow target selection from unconscious targets
    if best_target == None:
        for enemy in get_living_enemies(combatant):                   
        #Target selection priority:                                                     
            if best_target == None:
                best_target = enemy                   
            if calc_distance(combatant,enemy) <= combatant.desired_range:
                best_target = enemy            
            elif calc_distance(combatant,enemy) < calc_distance(combatant,best_target):                
                best_target = enemy                                            
                    
    combatant.target = best_target
    if combatant.target:
        if combatant.target == original_target:
            return True
        else:
            print_output(combatant.name + ' is now targetting ' + combatant.target.name)                     
            return True
    else:
        return False

def find_heal_target(combatant,range):
    heal_target = None    
    for ally in get_living_allies(combatant):
        if calc_distance(combatant,ally) <= range:
            if check_condition(ally,condition.Unconscious):
                heal_target = ally
            elif heal_target == None and ally.current_health <= ally.max_health/4:
                heal_target  = ally

    if heal_target == None:
        if combatant.current_health <= combatant.max_health/2:
            heal_target = combatant    
    return heal_target

def find_buff_target(combatant,buff_condition,range):
    buff_target = None    
    for ally in get_living_allies(combatant):
        if calc_distance(combatant,ally) <= range:
            if not check_condition(ally,condition.Unconscious) and not check_condition(ally,condition.Stunned) and not check_condition(ally,condition.Incapacitated):
                #For testing - target Raging allies with Enlarge or Haste if we have it
                if buff_condition == condition.Enlarged:                    
                    buff_target = ally        
                elif buff_condition == condition.Hasted:                    
                    buff_target = ally        
    if buff_target == None:    
        buff_target = combatant
    return buff_target

def find_targets_in_area(combatant,affected_grids):    
    affected_targets = []
    potential_targets = []
    potential_targets = all_other_combatants(combatant)
    for potential_target in potential_targets:
        if (potential_target.xpos,potential_target.ypos) in affected_grids:
            affected_targets.append(potential_target)
    return affected_targets

def calculate_area_effect(combatant,xorigin,yorigin,xtarget,ytarget,shape,width,length):
    #Determines area of effect of passed in parameters and returns a dict of affected x,y co-ords    
    #First round the values to the nearest 5 foot
    width = round_to_integer(width,5)
    # Subtract 5 feet from the length of the ability (as the effective origin point of the ability is 5 feet 'in front of' the cast point)
    length = round_to_integer(length-5,5)
    grid_width = int(width/5)
    grid_length = int(length/5)
    max_grids = grid_width * (grid_length+1)
    total_affected_grids = 0    
    line_grids = []                 
    affected_grids = []    
    targets = []
    x = 0
    y = 0
    xdestination = 0
    ydestination = 0

    # Begin at point of origin
    # Determine direction of ability
    # Calculate perpendicular direction and go the inverse perpendicular by round(width/2,5) steps
    # Cast forward to the length from this point
    # Iterate through the remaining steps along the width and cast forward to length
    if shape == area_of_effect_shape.Line:            
        width_limit = width/5
        width_pointer = 1
        width_step = 5
        width_direction = 1
        
        first_xorigin = xorigin
        first_yorigin = yorigin        
        
        # Calculate the angle between the origin point and target points in radians            
        radians = math.atan2(ytarget-yorigin, xtarget-xorigin)    
                
        # Calculate the distance 1 step towards the destination from the origin point
        length_origin_deltax = 5 * math.cos(radians) 
        length_origin_deltay = 5 * math.sin(radians)
        
        # Normalise the target to 1/2 the length away
        # Target adjustment
        # To make sure the lines draw correctly, convert the effective target to a point 1/2 the length along the line from xorigin to xtarget, then calculate angles from there
        # Otherwise we get weird behaviour (i.e. if the target is adjacent on an axis to our current point)
        
        #print_output('Target Point: (' + repr(xtarget) + ',' + repr(ytarget) + ')')

        length_target_deltax = length/2 * math.cos(radians)
        length_target_deltay = length/2 * math.sin(radians)   

        xtarget = round_to_integer(xtarget + length_target_deltax,5)
        ytarget = round_to_integer(ytarget + length_target_deltay,5)

        # Initialise an origin point to this location - this is where all lines will be drawn from
        central_xorigin = round_to_integer(xorigin + length_origin_deltax,5)
        central_yorigin = round_to_integer(yorigin + length_origin_deltay,5)
               
        #print_output('Central origin: (' + repr(central_xorigin) + ',' + repr(central_yorigin) + ')')

        # Recalculate the angle between the new origin point and target points in radians            
        radians2 = math.atan2(ytarget-central_yorigin, xtarget-central_xorigin)    

        # Calculate the length in feet from origin point - this determines the length delta to be added to our derived origin point
        length_deltax = length * math.cos(radians2)
        length_deltay = length * math.sin(radians2)    

        # Find the perpendicular angle from the origin point
        perpendicular = math.atan2(xtarget-central_xorigin, (ytarget-central_yorigin) * -1)    
       
        # Force line to shift on the target side of the initial origin point (the aoe effect cannot begin behind - or in line with - the caster)
        # The line must also begin on the same plane as the origin point
        width_offset = 0
        while width_pointer <= width_limit:
            if total_affected_grids + grid_length <= max_grids:
                # Find the step along the perpendicular        
                # Width offset starts at zero (first width delta = 0 for first line to cast from init_origin)
                # Width offset alternates multiplying by *-1 each step, and adding +5 every other step (so first line cast from 0, second from -5, third from 5, fourth from -10 etc.)
                # If the length delta is smaller than one grid, do not apply an offset and keep the same line on that axes
                if abs(length_deltay) >= 5:
                    width_deltax = width_offset * math.cos(perpendicular) * width_direction
                else:
                    width_deltax = 0
                if abs(length_deltax) >= 5:
                    width_deltay = width_offset * math.sin(perpendicular) * width_direction 
                else:
                    width_deltay = 0

                # Set the origin point as a function of the initial line
                xorigin = round_to_integer(central_xorigin + width_deltax,5)                   
                yorigin = round_to_integer(central_yorigin + width_deltay,5)  

                # Determine destination
                xdestination = round_to_integer(xorigin + length_deltax,5)
                ydestination = round_to_integer(yorigin + length_deltay,5)
                        
                # Debug output
                #print_output('Line origin: (' + repr(xorigin) + ',' + repr(yorigin) + ')' + ' Normalised Target point: (' + repr(xtarget) + ',' + repr(ytarget) + ')' + ' Line destination: (' + repr(xdestination) + ',' + repr(ydestination) + ')')
        
                # Uses a variation of Brehenams algorithm to return the grids that are supercovered by a line drawn from origin -> destination
                line_grids = evaluate_line(yorigin,xorigin,ydestination,xdestination)                
            
                #Append affected grids to master list if they're not present
                i = 0
                while i < len(line_grids):
                    if line_grids[i] not in affected_grids:
                        affected_grids.append(line_grids[i])
                    i += 1

                total_affected_grids += len(line_grids)

            width_pointer += 1            
            width_direction *= -1
            if width_direction == -1:
                width_offset += 5
                  
    # Find enemy locations and see if targets are located within the grid set; this will be returned for the damage function    
    affected_targets = find_targets_in_area(combatant,affected_grids)

    # Find all tar
    #Print out a grid (half debugging, may leave it in) - show all the targets so they can be rendered
    #print_output('AoE Debugging: Total potential grids: ' + repr(total_affected_grids) + ' Max grids: ' + repr(max_grids) + ' Affected grids: ' + repr(len(affected_grids)))

    # Pass the affected grids to the print_grid function, focused on the origin of the spell, and with all combatants listed so we can see the location of other member
    print_grid(first_xorigin,first_yorigin,affected_grids,combatants.list)

    return affected_targets
            
def evaluate_line(y1,x1,y2,x2):
    affected_grids = []
# From http://eugen.dedu.free.fr/projects/bresenham/
# use Bresenham-like algorithm to print a line from (y1,x1) to (y2,x2)
# The difference with Bresenham is that ALL the points of the line are
#   printed, not only one per x coordinate.
# Principles of the Bresenham's algorithm (heavily modified) were taken from:
#   http://www.intranet.ca/~sshah/waste/art7.html 
    i = 0               # loop counter
    ystep = 0           # the step on y and x axis
    xstep = 0    
    error = 0           # the error accumulated during the increment
    errorprev = 0       # *vision the previous value of the error variable
    y = y1              # the line points
    x = x1;     
    ddy = 0             # compulsory variables: the double values of dy and dx
    ddx = 0        
    dx = x2 - x1
    dy = y2 - y1
    affected_grids.append((x1,y1))  #first point
  
    if (dy < 0):
        ystep = -5;
        dy = -dy;
    else:
        ystep = 5;

    if (dx < 0):
        xstep = -5;
        dx = -dx;
    else:
        xstep = 5;

    ddy = float(2 * dy);  # work with double values for full precision
    ddx = float(2 * dx);

    if (ddx >= ddy):  # first octant (0 <= slope <= 1)
        # compulsory initialization (even for errorprev, needed when dx==dy)
        errorprev = error = dx  # start in the middle of the square
        i = 0
        while i < dx:  # do not use the first point (already done)
            x += xstep
            error += ddy
            if (error > ddx):  # increment y if AFTER the middle ( > )
                y += ystep;
                error -= ddx;
                # three cases (octant == right->right-top for directions below):
                if (error + errorprev < ddx):  #bottom square also
                    affected_grids.append((x,y-ystep))
                elif (error + errorprev > ddx):  # left square also
                    affected_grids.append((x-xstep,y))
                # Evaluating this condition will also return any grid that the line passes over the corner of
                # This causes strange behaviour in DnD as clipping the square should not necessarily include the square in the AoE
                else: # corner: bottom and left squares also                
                    affected_grids.append((x,y-ystep))
                    affected_grids.append((x-xstep,y))
            i += 5

            affected_grids.append((x,y))      
            errorprev = error;
            
    else: # the same as above
        errorprev = error = dy
        i = 0
        while i < dy:     
            y += ystep;
            error += ddx;
            if (error > ddy):
                x += xstep;
                error -= ddy;
                if (error + errorprev < ddy):
                  affected_grids.append((x-xstep,y))
                elif (error + errorprev > ddy):
                  affected_grids.append((x,y-ystep))
                # Evaluating this condition will also return any grid that the line passes over the corner of
                # This causes strange behaviour in DnD as clipping the square should not necessarily include the square in the AoE                
                else:
                    affected_grids.append((x-xstep,y))
                    affected_grids.append((x,y-ystep))

            i += 5

            affected_grids.append((x,y))
            errorprev = error;

    return affected_grids        
  # assert ((y == y2) && (x == x2));  // the last point (y2,x2) has to be the same with the last point of the algorithm    
 
 