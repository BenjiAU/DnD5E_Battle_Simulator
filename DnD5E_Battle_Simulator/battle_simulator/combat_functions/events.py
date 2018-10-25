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
                if combatant.current_health > 0:
                    if check_condition(combatant,condition.Cauterised):
                        print_output('At the end of their turn, ' + combatant.name + ' cannot regrow any heads due to suffering Fire damage this round!')      
                        #Clear the cauterised condition for the next round
                        remove_condition(combatant,condition.Cauterised)
                    else:
                        head_count_differential = combatant.turn_start_head_count - combatant.current_head_count
                        if head_count_differential > 0:
                            print_output('<b>-------------Event----------</b>')
                            print_output('At the end of their turn, ' + combatant.name + ' regrows one head for each head lost this round!')      
                            i = 0
                            while i < head_count_differential:
                                #hydra's weapons are a bit different - append one weapon for each 'head', remove weapons as heads are destroyed, modify multiattack to be number of heads 
                                bite = weapon()
                                bite.name = "Bite"
                                bite.weapon_type = weapon_type.Natural;
                                bite.range = 0
    
                                bite.damage_die = 10
                                bite.damage_die_count = 1
                                bite.weapon_damage_type = damage_type.Piercing
        
                                bite.magic_to_hit_modifier = 3
                                hydra.weapon_inventory().append(bite)
                                hydra.weapon_inventory().append(bite)
                                i += 1

                                #Heal 10 hp per head
                                damage.heal_damage(combatant,event.self_heal)
                    
        
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
                    print_output('Upon suffering damage, something happens to ' + combatant.name + ' and they cast the ' + event.spell.name + ' spell!')      
                    spells.cast_spell(combatant,event.spell)
        elif event.trigger == event_trigger.OnSufferDamageThreshold:
            if combatant.damage_taken_this_turn >= event.requirements:                
                    execute = True
            if execute:
                print_output('<b>-------------Event----------</b>')
                if event.invoke == event_invoke.Feature:     
                    if combatant.monster_type == monster_type.Hydra:                        
                        print_output('Upon suffering ' + repr(event.requirements) + ' damage this turn, one of the ' + combatant.name + '\'s heads dies! They lose one bite from their Multiattack')
                        del combatant.weapon_inventory()[-1]
                        del combatant.multiattack[-1]
                        combatant.current_head_count -= 1
                        #If this is the last head, the hydra dies
                        if combatant.current_head_count <= 0:
                            combatant.current_health = 0
                            combatant.death_saving_throw_failure = 3
                            print_output('Its last head destroyed, ' + combatant.name + ' perishes instantly!')
                            resolve_fatality(combatant)
            