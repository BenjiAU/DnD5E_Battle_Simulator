# DnD5E_Battle_Simulator

A fun script that simulates a bunch of different combat elements in a mock DnD 5E battle - inspired by the "Percy vs Grog" theorycrafting that has run amok since the Skull incident.

Notes:
* The package currently consists of 5 main files:
  * classes.py - this contains all of the class definitions for the package; this will likely be further split as time goes on
  * initialise_combat.py - this manages the instance-level combat tasks of initialising new spells, defining which abiltiies are active on a creature based on its class levels, and managing target selection
  * combat_functions.py - this contains all of the generic combat-related functions, including the mechanisms for actions/bonus actions, handling movement, and handling attacks/spell casting and subsequent damage rolls. This may be split further as time goes on
  * print_functions - this controls output directed by other parts of the program
  * main.py - this contains the main 'simulate_battle' function and calls to open/close the output file
* I created a new Python Web Application for the purposes of GitHub (this was originally a console app) - eventually I intend for this to be able to function on a public website and allow users to select combatants/details as input, but for now executing the script is sufficient to get the output
* Output will be generated to C:\stuff\combatlog_<timestamp>, no directory identification or customisation is present; edit the path if you want to output to a different file
