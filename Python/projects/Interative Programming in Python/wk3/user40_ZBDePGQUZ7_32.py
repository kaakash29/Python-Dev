# "Stopwatch: The Game"

# Imports 
import simplegui

# Globals

# Constants
RUNNING = 0
STOPPED = 1

# Variables 
ticks_counter = 0
watch_state = STOPPED # or not started yet
tries = 0
succesful_tries = 0


def format(numofticks):
    """
    Consumes teh numner of ticks and returns teh 
    formatted string in the form A:BC:D
    A [0-9] BC = [00 - 60] D: [0-9]
    A = mins BC = secs D = milisecs
    """
    milisecs = numofticks % 10
    secs = (numofticks/10) % 60
    mins = (numofticks/10)/60
    
    if secs < 10:
        secsstr = "0"+str(secs)
    else:
        secsstr = str(secs)
        
    time = str(mins)+":"+secsstr+":"+str(milisecs)
    return time
    

def handle_start():
    """
    Called when the start button is clicked 
    has no effect if the clock is in running state
    if the clock is paused/stopped sets it to running stete
    """
    global watch_state
    
    if watch_state == STOPPED:
        # set the state to running state    
        watch_state = RUNNING
    else:
        pass
    
    
def handle_stop():
    """
    Called when the stop button is clicked 
    Updates score and stops running timer
    """
    global watch_state, ticks_counter 
    global tries, succesful_tries
    
    milisecs = ticks_counter % 10
    if watch_state == RUNNING:
        if milisecs == 0:
            tries += 1
            succesful_tries += 1
        else: 
            tries += 1
        
    watch_state = STOPPED
    
def handle_reset():
    """
    Called when the reset button is clicked 
    Resets a running clock
    """
    global watch_state , ticks_counter
    
    if watch_state == RUNNING:
        watch_state = STOPPED
    else:
        pass
    
    ticks_counter = 0
    


def handle_tick():
    """
    Called on every tick event increases the 
    ticks counter by 1 to keep track of timer
    """
    global ticks_counter , watch_state 
    if watch_state == RUNNING:
        ticks_counter += 1
    else:
        pass


def handle_draw(canvas):
    """
    Called for drawing teh events on canvas 
    draws formatted time and scores
    """
    global ticks_counter,succesful_tries,tries
    
    msg = format(ticks_counter)
    score = str(succesful_tries)+"/"+str(tries)
    
    canvas.draw_text(score, [10, 30], 30, "Green")
    canvas.draw_text(msg, [200, 250], 60, "Red")
    
    
    
# create frame
frame = simplegui.create_frame("StopWatch", 500, 500)

# register event handlers
frame.add_button("Reset", handle_reset, 100)
frame.add_button("Start", handle_start, 100)
frame.add_button("Stop", handle_stop, 100)
timer = simplegui.create_timer(0.1, handle_tick)
frame.set_draw_handler(handle_draw)

# start frame
frame.start()
timer.start()
