from battle_simulator import combatants
from battle_simulator.classes import * 
from battle_simulator.print_functions import * 
from battle_simulator.combat_functions.damage import * 
import operator
from operator import attrgetter

#Cast a spell  
def cast_spell(combatant,spell,crit):
    #Check if a spell slot is available to be used
    #Always use highest level spellslot to cast spell (for now...)
    spellslot = get_highest_spellslot(combatant,spell)
    #See if a spellslot was returned by the function
    if spellslot:               
        #Check that components (V,S,M) are available for spell?
        #Evaluate if spell is targetted or self (i.e. buff?)?
        #Check that the target is in a condition to warrant casting the spell on?
        if combatant.target.conscious:
            #Check that target is in range of spell (spells with range 0 always satisfy this condition - i.e. Divine Smite is tied to attack)
            if (spell.range == 0) or calc_distance(combatant,combatant.target) <= spell.range:
                #Resolve saving throw
                #if spell.saving_throw:
                    #Resolve saving throw to see if damage/condition is applied
                #Consume the spell slot from player's available slots
                print_output(combatant.name + ' is burning a ' + numbered_list(spellslot.level) + ' level spellslot to cast ' + spell.name)                            
                # Deduct one usage from the spellslot
                spellslot.current -= 1             
            
                print_output(indent() + 'Rolling spell damage:')                        
                spell_damage = 0
                if spell.damage_die > 0:
                    # Start with base damage of spell
                    for x in range(0,spell.damage_die_count):
                        die_damage = roll_die(spell.damage_die)
                        print_output(doubleindent() + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(spell.damage_die) + ' (Spell Damage)')
                        spell_damage += die_damage

                    #Add additional damage for levels of expended spell slot
                    if spellslot.level > spell.min_spellslot_level:
                        # If the spell gains no benefit for spells higher than the maximum, we still burn the higher slot, but only get benefit from the maximum against the spell                
                        if spell.max_spellslot_level < spellslot.level:
                            spellslot_bonus = spell.max_spellslot_level
                        else:
                            spellslot_bonus = spellslot.level                
                
                        for x in range(spell.min_spellslot_level,spellslot_bonus):
                            for y in range(0,spell.damage_die_count_per_spell_slot):
                                die_damage = roll_die(spell.damage_die_per_spell_slot)
                                print_output(doubleindent() + combatant.name + ' rolled a ' + repr(die_damage) + ' on a d' + repr(spell.damage_die_per_spell_slot) + ' (Additional Spell Damage from Spell Slot)')
                                spell_damage += die_damage

                    #Add bonus damage
                    if combatant.target.race == spell.bonus_damage_target:
                        for x in range(0,spell.bonus_damage_die_count):
                            die_damage = roll_die(spell.bonus_damage_die)
                            spell_damage += die_damage
            
                #Double dice if crit
                if crit:
                    spell_damage = spell_damage * 2
                # Add modifier

                print_output(indent() + combatant.name + ' cast ' + spell.name + ' and dealt a total of ' + repr(spell_damage) + ' points of ' + spell.damage_type.name + ' damage!')                    
                deal_damage(combatant,combatant.target,spell_damage,spell.damage_type,True)
                #Resolve spell damage immediately
                resolve_damage(combatant.target)

                #Check if we have spellslots left
                if spellslot.current == 0:
                    print_output(combatant.name + ' has no ' + numbered_list(spellslot.level) + ' level spellslots remaining!')

def get_highest_spellslot(combatant,spell):
    # Sort spells by level (use highest slots first)
    initkey = operator.attrgetter("level")
    sorted_spells = sorted(combatant.spellslots(), key=initkey,reverse=True)    

    for spellslot in sorted_spells:
        if spellslot.level >= spell.min_spellslot_level and spellslot.current > 0:
            return spellslot             