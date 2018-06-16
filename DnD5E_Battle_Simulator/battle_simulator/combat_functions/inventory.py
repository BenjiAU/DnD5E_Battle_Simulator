#Explicit imports
from battle_simulator import combatants

#Implicit imports
from battle_simulator.classes import *
from battle_simulator.print_functions import *

def use_equipment(combatant):
    # Iterate through equipment and use any available spells (if possible)
    for eq in combatant.equipment_inventory():
        # Enlarge (i.e. from Titanstone Knuckles)
        if eq.grants_equipment_spell == equipment_spells.Enlarge:
            if not combatant.enlarged:
                print_output(combatant.name + ' smashes the ' + eq.name + ' together and grows in size! This uses up their Action')            
                combatant.enlarged = True
                combatant.action_used = True

        # Haste (i.e. from Boots of Haste)
        if eq.grants_equipment_spell == equipment_spells.Haste:
            if not combatant.hasted:
                print_output(combatant.name + ' clicks the ' + eq.name + ' together and begins to move rapidly! (+ Hasted Action, +2AC) This uses up their Bonus Action')            
                combatant.hasted = True
                combatant.hasted_bonus_armour = 2;
                combatant.hasted_action = True;
                combatant.hasted_action_used = False;
                combatant.bonus_action_used = True

        # Blade Return (Belt of Blade Returning - does not use an action/bonus action, just happens at the start of each round)
        if eq.grants_equipment_spell == equipment_spells.BladeReturn:            
            reequip_thrown_weapon = False
            for weapon in combatant.weapon_inventory():                                    
                if weapon.thrown and weapon.was_thrown:
                    reequip_thrown_weapon = True
                    weapon.was_thrown = False
                    print_output(weapon.name + ' re-appears on ' + combatant.name + '\'s ' + eq.name)            

            #Re-equip the first weapon on the list                                
            if reequip_thrown_weapon:
                wield(combatant,itemgetter(0)(combatant.weapon_inventory()))     
                print_output(combatant.name + ' draws ' + combatant.main_hand_weapon.name + ' and prepares to fight once more!')                        

#Weapon swap
def weapon_swap(combatant,current_range):
    # A weapon is already equipped; equip a new one
    if combatant.main_hand_weapon != None:
        for weapon in combatant.weapon_inventory():                            
            # Swap to range weapon if within range (preferring shorter range non-broken weapons), unless in melee, in which case only swap to melee                        
                # swap out broken weapon, unless this is the better weapon
            if ((weapon.range >= current_range and current_range > melee_range() and combatant.main_hand_weapon.broken and not weapon.broken) or 
                # prefer unbroken shorter range weapon
            (weapon.range >= current_range and current_range > melee_range() and weapon.range < combatant.main_hand_weapon.range) or 
                # prefer range weapon at range over melee weapon
            (weapon.range >= current_range and current_range > melee_range() and weapon.range != 0 and combatant.main_hand_weapon.range == 0) or
                # prefer melee weapon for melee range, but don't swap out for no reason
            (weapon.range == 0 and current_range <= melee_range() and combatant.main_hand_weapon.range != 0)):         
                # Don't swap if we're already using this weapon
                if combatant.main_hand_weapon != weapon:
                    # Draw ruined and cry if main hand weapon is ruined - making it here means there are no better options
                    if weapon.ruined and (combatant.main_hand_weapon.ruined):                        
                        if wield(combatant,weapon,True):
                            print_output(combatant.name + ' sadly puts away ' + combatant.main_hand_weapon.name + ' and draws out the ruined ' + weapon.name)                        
                            return True
                    # Draw broken if we have to (i.e. main hand weapon is broken/ruined, and we need to repair the better one)                    
                    if weapon.broken and (combatant.main_hand_weapon.broken or combatant.main_hand_weapon.ruined):                          
                        if wield(combatant,weapon,True):
                            print_output('Frustrated, ' + combatant.name + ' stows ' + combatant.main_hand_weapon.name + ' and draws out the broken ' + weapon.name)                        
                            return True
                    # If the weapon is neither broken nor ruined, and it makes it here, it's the best choice
                    if not weapon.ruined and not weapon.broken:                        
                        if wield(combatant,weapon,True):
                            print_output(combatant.name + ' stows ' + combatant.main_hand_weapon.name + ' and readies ' + weapon.name + ' in their main hand.')                        
                            return True
                    
            #Thrown weapon handling
            if combatant.main_hand_weapon.was_thrown:                    
                if not weapon.was_thrown:                    
                    if wield(combatant,weapon,True):
                        print_output(combatant.name + ' draws  ' + weapon.name + ' after throwing their weapon')                        
                        return True

    # No weapon is equipped; draw one
    else:
        for weapon in combatant.weapon_inventory():                            
            if wield(combatant,weapon,False):                
                print_output(combatant.name + ' draws their first weapon!')
                return True

    if combatant.main_hand_weapon.name == "":
        # If no weapon has been equipped, and we haven't been able to draw one, equip a phantom 'Unarmed Strike' weapon
        if wield(combatant,unarmed_strike(combatant),True):            
            print_output(combatant.name + ' raises their fist and prepares to strike!')
            return True
    
    # Debug output - if characters aren't swapping weapons correctly, print this out
    #print_output(combatant.name + ' considered swapping their weapon, but decided against it. Main Hand: ' + combatant.main_hand_weapon.name + ' Off Hand: ' + combatant.offhand_weapon.name)
    return False

# Wield a weapon (check hands free and which weapon goes where)
def wield(combatant,weapon,replace_mainhand):    
    #If our main hand is empty, equip the weapon automatically
    if combatant.main_hand_weapon == None:        
        combatant.main_hand_weapon = weapon
        print_output(combatant.name + ' begins wielding ' + weapon.name + ' in their main hand.')
        if weapon.two_handed or weapon.versatile:
            if combatant.offhand_weapon == None:    
                print_output(combatant.name + ' grasps their weapon with both hands!')
                combatant.offhand_weapon = weapon            
        return True
    # If our main hand is not empty but the weapon swap is forced to the main hand, equip the weapon
    elif combatant.main_hand_weapon != None and replace_mainhand:            
        combatant.main_hand_weapon = weapon
        print_output(combatant.name + ' begins wielding ' + weapon.name + ' in their main hand.')
        if weapon.two_handed or weapon.versatile:
            if combatant.offhand_weapon == None:    
                print_output(combatant.name + ' grasps their weapon with both hands!')
                combatant.offhand_weapon = weapon                    
        return True    
    # If we are holding something in the main hand and have not specified the new weapon to overwrite the mainhand, equip the weapon to the offhand
    else:
        print_output(combatant.name + ' begins wielding ' + weapon.name + ' in their off hand.')
        combatant.offhand_weapon = weapon
        return True

    print_output('Error: ' + combatant.name + ' was unable to correctly wield ' + weapon.name)
    return False

def unarmed_strike(combatant):    
    # Create and equip a phantom 'unarmed strike' weapon to proceed with attack calculations
    unarmed_strike = weapon()
    unarmed_strike.name = "Unarmed Strike"
    unarmed_strike.weapon_type = weapon_type.Unarmed
    unarmed_strike.monk_weapon = True    
    unarmed_strike.weapon_damage_type = damage_type.Bludgeoning
    if combatant.martial_arts:
        unarmed_strike.damage_die = combatant.martial_arts_die
        unarmed_strike.damage_die_count = 1
    if combatant.ki_empowered_strikes:
        unarmed_strike.magic = True
    return unarmed_strike