def init():
    #File-specific fields to allow print_functions to output consistently to the same file despite being called from all over the place
    global filename
    filename = ""
    
    global file_open
    file_open = False

    global file

    #Maximum number of battle simulations to occur
    global max_attempts
    max_attempts = 10

    #Maximum number of rounds of combat before aborting
    global max_rounds
    max_rounds = 50

    #List for appending output
    global output
    output = []

    #Verbosity controls
    global verbose_movement
    verbose_movement = False

    global start_time
    
    global end_time