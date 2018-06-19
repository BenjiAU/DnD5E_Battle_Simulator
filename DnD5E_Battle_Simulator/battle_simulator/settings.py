def init():
    #File-specific fields to allow print_functions to output consistently to the same file despite being called from all over the place
    global filename
    filename = ""
    
    global file_open
    file_open = False

    global file

    #Simulation controls
    #Maximum number of battle simulations to occur
    global max_attempts
    max_attempts = 10

    #Maximum number of rounds of combat before aborting
    global max_rounds
    max_rounds = 50

    #Randomises starting positions within a range
    global randomise_starting_positions
    randomise_starting_positions = True    

    #Verbosity controls
    # Movement verbosity - if True, will output each step taken in the movement functions (lots of spam)
    global verbose_movement
    verbose_movement = False

    # Damage summary - if True, will output a damage summary at the end of each damage calculation revealing the breakdown of damage; mainly useful to show all the additions/reductions in a complicated round
    global show_damage_summary
    show_damage_summary = False

    global start_time
    
    global end_time
    
    #List for appending output
    global output
    output = []
