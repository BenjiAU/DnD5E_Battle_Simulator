# DnD5E_Battle_Simulator

An increasingly complicated script that simulates a bunch of different combat elements in a mock DnD 5E battle - inspired by the Critical Role internet series and characters. 

This all came about because of "Percy vs Grog" theorycrafting in Discord, where it seemed there were too many variables to definitively state whether one combatant or the other would be victorious in any given situation. It turns out, there are a lot of freaking variables, but if you make some assumptions, control different variables and simulate the combat a bunch of times, you can get a pretty good idea!

This has now extended into simulating other characters from Critical Role, and is starting to become something that can be applied generically to DnD 5E combat encounters. Long term, it may be possible to throw a given PC or party into the simulation against your big bads, and simulate the battle a few hundred times before actually playing out combat. It works best in 1v1 situations, with more combatants adding levels of complexity (regarding targetting logic and action selection) that are probably beyond what I'm capable of implementing in a reasonable amount of time. It will never match the real thing, but if you're worried about the deadliness or threat an encounter poses, it could be pretty handy!

Simulation Notes:
The core combat loop consists of:
* Evaluating targets
   * Note that targets are only evaluated once, at the start of the creature's turn. This is currently a naive process, and means that the entire turns worth of actions will be executed against the single target. More sophisticated targetting logic is a possibility in the future.
* Resolving start-of-round activities (i.e. recharge Breath Attack, check if Assassinate condition is fulfilled)
* Using Equipment items (which may consume Action/Bonus Action)
* Using Movement (all movement is consumed here if it is available; this is the only place the actual Movement activity of the turn is evaluated (you can't use 10 feet of movement here, 10 feet there))
* Checking for Bonus Action use (i.e. Vow of Enmity, Hunters Mark should be used prior to Action)
* Checking for Action use (normally Dash or Attack)
* Checking for Bonus Action use (i.e. off-hand attack that can only fire after Attack)
* Checking for Hasted Action use (restricted to Dash/Attack)
* Checking for Action Surge and gaining benefit (currently Action Surges are burned straight away, meaning characters will waste them Dashing instead of saving them for when they can attack)
* Resolving damage that occurs 'at end of turn' (i.e. Gunslinger's Haemmorhaging Critical)

Missing Behaviour:

Several rules that come into play in your typical DnD battle are currently missing; some of these may be implemented, others may stay out of scope due to their complexity:
* Limited customisation - at time of writing you can only simulate battles from a handful of pre-loaded characters. My intention is to have all aspects of your fights be customisable, but I'll need to dust up on JSON to make some serialisable data objects to handle the data selection. This is on the list!
* Missing Classes - at time of writing only Barbarians, Fighters, Paladins and Rogues have a substantial implementation in the simulator. Next up will likely be Monks and Rangers due to their lack of relying on spellcasting. Druids, Clerics, Bards, Wizards, Sorcerers and Warlocks will require a more comprehensive spell system, and will probably not be available for some time.
* Threat Consideration - while there is no 'threat' mechanic in DnD per se, players in particular will generally target spell casters or weaker threats to even out the action economy. I'm considering different ways of managing targets; if you have any thoughts, please let me know!
* Reactions - there is currently no facility to handle other combatants acting outside of the confines of their turn. If they can use their Reaction to react to a specific activity (for example, an attacker landing an attack on a defender) we can trigger the reaction that way (see Rogue's Uncanny Dodge), but we currently do not, say, iterate through all combatants every time someone moves to see if an opportunity attack would be triggered. This should be possible, but will require a fairly significant refactor
* Terrain - combat currently takes place on an infinite featureless arena centered at co-ordinates 0,0. Most DnD battles will have some sort of terrain or features to block line of sight, grant cover, allow Rogues to Hide, and generally add more complexity to the battle. This is likely to be outside the scope of the simulation, which also means any spells that rely on terrain or influence terrain (i.e. Wall of Force, Reverse Gravity, Shape Earth) will not be implemented.
* Area Effecting Abilities - this should be possible to implement now that we have an x/y co-ordinate system, with any spheres or cubes listed in the PHB being treated as their 2-dimensional equivalent. Hope to get Breath Attack affecting multiple people soon.
* Spell Casting - I really want to implement every spell in DnD, with a proper decision tree for evaluating a combat situation and spell-selection logic to choose the appropriate spell and slot given a certain situation. However, as anyone who's ever looked at the Player's Handbook knows, spell casting rules are complicated, and there is a huge variety of spells to consider. For the purposes of the simulation, I will be keeping spells limited to direct-damage dealing spells where possible (targetted first, AoE spells once there is better logic for handling AoE target selection). In a 1v1 scenario for high-level casters there are many spells that can outright delete the opponent from the map (Banishment, Plane Shift) or otherwise render them useless in combat (Feeblemind, Hold Person). These are cool spells, but from a simulation point of view, having a coin flip decide the outcome of a battle is not very interesting. If there is enough interest in the simulator for larger-scale combat where more sophisticated spellcasting is highly desireable, I may implement it down the road.
* Z-axis movement - flying is not currently possible, and probably won't be for a long time. Z-axis movement introduces a whole knew range of complications. In a game, if you have a monster capable of flight against a melee heavy party, you're likely to want to land the monster somewhere to give the party a fighting chance; the simulation won't allow for this, so you'll easily be put in situations where the optimal approach is to fly at maximum range with Haste and 120 feet of movement, bounce into range to attack, and bounce out to make yourself invincible. I'm looking at you, Vax. The point of this isn't really to simulate every possible thing that can happen in DnD, but more to evaluate the effect of random dice and creature abilities in a slugfest; flying is antithical to that. If there's high demand for it in the future I may consider it, but for now, the dragons will be bound to the Earth.


Other notes
* The project is designed to run on a Flask virtual environment. It will probably work with Django as the actual web operation isn't very complicated; there are just a few library in print_functions and index.py that will need to be adjusted
* After each simulation, output is dumped to /combatlog/combat_<datetime>. The file is opened and read out to be displayed on the main index page, but isn't stored anywhere else. Hitting the 'Reset' button will delete this file and refresh the page to clear the output. Hitting 'Simulate' will generate a new file and read that instead, keeping the original file in the log. 
* Live version of this project is hosted at benjib.pythonanywhere.com and available for public access
 
