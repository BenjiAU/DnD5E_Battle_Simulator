from battle_simulator import combatants
from battle_simulator.classes import * 
from battle_simulator.print_functions import * 
from battle_simulator.combat_functions.generics import * 
from battle_simulator.combat_functions.spells import * 

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

def on_end_turn_event(combatant):    
    for event in combatant.events():
        execute = False
        if event.trigger == event_trigger.OnEndTurn:
            execute = True

        if execute:            
            if event.invoke == event_invoke.Feature:
                if combatant.monster_type == monster_type.Hydra: 
                    if combatant.alive:
                        head_count_differential = combatant.last_turn_head_count - combatant.current_head_count
                        if head_count_differential > 0:
                            print_output('<b>-------------Event----------</b>')
                            print_output('The hydra had ' + repr(combatant.last_turn_head_count) + ' heads at the end of their last turn, and now has ' + repr(combatant.current_head_count))                        
                            if check_condition(combatant,condition.Cauterised):
                                print_output('At the end of their turn, ' + combatant.name + ' cannot regrow any heads due to suffering Fire damage this round!')      
                                #Clear the cauterised condition for the next round
                                remove_condition(combatant,condition.Cauterised)
                            else:                                                            
                                print_output('At the end of their turn, ' + combatant.name + ' regrows one head for each head lost since the end of their last turn!')      
                                i = 0
                                while i < head_count_differential:
                                    print_output('Two new heads spring forth from the Hydra!')
                                    combatant.multiattack.append('Bite')
                                    combatant.current_head_count += 1
                                    damage.heal_damage(combatant,event.self_heal)
                                    combatant.multiattack.append('Bite')                                
                                    combatant.current_head_count += 1                                    
                                    damage.heal_damage(combatant,event.self_heal)
                                    i+= 1

                            #Set the number of heads 
                            print_output('The hydra now has ' + repr(combatant.current_head_count) + ' heads!')
                            combatant.last_turn_head_count = combatant.current_head_count                      
        
def on_damage_taken_event(combatant):    
    for event in combatant.events():        
        execute = False
        if event.trigger == event_trigger.OnSufferDamageType:
            for x in combatant.pending_damage():                        
                if x.pending_damage_type in event.requirements:
                    execute = True
            if execute:
                if event.invoke == event_invoke.Spell:                
                    print_output('<b>-------------Event----------</b>')
                    print_output('Upon suffering damage, ' + combatant.name + ' casts the ' + event.spell.name + ' spell!')      
                    spells.cast_spell(combatant,event.spell)
        elif event.trigger == event_trigger.OnSufferDamageThreshold:            
            if combatant.damage_taken_this_turn >= event.requirements:                
                execute = True
            if execute:
                print_output('<b>-------------Event----------</b>')
                if event.invoke == event_invoke.Feature:                         
                    if combatant.monster_type == monster_type.Hydra:           
                        if not combatant.head_lost_this_turn:
                            print_output('Upon suffering ' + repr(event.requirements) + ' damage this turn, one of the ' + combatant.name + '\'s heads dies!')                          
                            if len(combatant.multiattack) > 0:
                                del combatant.multiattack[-1]
                            combatant.current_head_count -= 1
                            combatant.head_lost_this_turn = True
                            print_output('The Hydra currently has: ' + repr(combatant.current_head_count) + ' heads.')
                            print_output('The Hydra\'s multiattack: ' + repr(combatant.multiattack))
                            #If this is the last head, the hydra dies
                            if combatant.current_head_count <= 0:
                                combatant.death_saving_throw_failure = 3
                                pd = pending_damage()
                                pd.pending_damage_type = damage_type.Generic
                                pd.damage = combatant.current_health
                                combatant.pending_damage().append(pd)
                                print_output('Its last head destroyed, ' + combatant.name + ' suffers massive damage!')                            
            