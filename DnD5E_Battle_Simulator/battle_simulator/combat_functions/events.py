from battle_simulator import combatants
from battle_simulator.classes import * 
from battle_simulator.print_functions import * 
#from battle_simulator.combat_functions.spells import * 

from . import spells
from . import damage

def on_begin_turn_event(combatant):    
    for event in combatant.events():
        execute = False
        if event.trigger == event_trigger.OnBeginTurn:
            execute = True

        if execute:            
            if event.invoke == event_invoke.Feature:                
                if combatant.current_health > 0 and combatant.current_health < combatant.max_health:
                    print_output('<b>-------------Event----------</b>')
                    print_output('At the start of their turn, ' + combatant.name + ' regenerates health!')      
                    damage.heal_damage(combatant,event.self_heal)
    
def on_damage_taken_event(combatant):    
    for event in combatant.events():
        execute = False
        if event.trigger == event_trigger.OnSufferDamage:
            for x in combatant.pending_damage():                        
                if x.pending_damage_type in event.requirements:
                    execute = True
        if execute:
            if event.invoke == event_invoke.Spell:                
                print_output('<b>-------------Event----------</b>')
                print_output('Upon suffering damage, something happens to ' + combatant.name + ' and they cast the ' + event.spell.name + ' spell!')      
                spells.cast_spell(combatant,event.spell)
    