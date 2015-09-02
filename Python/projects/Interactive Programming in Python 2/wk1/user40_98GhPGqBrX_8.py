# implementation of card game - Memory

import simplegui
import random

# States of the game 
HIDDEN = False
EXPOSED = True

ZERO = 0 
ONE = 1
TWO = 2

# the deck of numbers
memory_deck = []
exposed = []
state = ZERO
exposed1_index = -1
exposed2_index = -1
turns = 0

# creates a list of 16 numbers following game specifications
def create_random_list():
    rand_list8 = range(0, 8)
    dup_rand_list8 = range(0, 8) 
    rand_list16 = rand_list8 + dup_rand_list8
    random.shuffle(rand_list16)
    return rand_list16
  

# helper function to initialize globals
def new_game():
    global memory_deck, exposed
    memory_deck = create_random_list()
    exposed = [HIDDEN]*16
        
# returns the index for the clicked position
def clickindex(pos):
    for idx in range(0, 16):
        if (50 * idx <= pos[0] <= 50 * idx + 50) and (0 <= pos[1] <=100):
            return idx
        else:
            continue

# mouse event handler
def mouseclick(pos):
    
    global memory_deck, exposed, exposed1_index, exposed2_index, state, turns

    index_of_mouseclick = clickindex(pos)
    
    
    
    if exposed[index_of_mouseclick] == HIDDEN: # valid click
        
        turns += 1
        label.set_text("Turns = " + str(turns))
        
        if state == ZERO:
            exposed[index_of_mouseclick] = EXPOSED
            exposed1_index = index_of_mouseclick
            state = ONE
            
        elif state == ONE:
            exposed[index_of_mouseclick] = EXPOSED
            exposed2_index = index_of_mouseclick
            state = TWO
            
        elif state == TWO:
            # check for match
            if memory_deck[exposed1_index] != memory_deck[exposed2_index]:
                exposed[exposed1_index] = HIDDEN
                exposed[exposed2_index] = HIDDEN
                
            exposed[index_of_mouseclick] = EXPOSED    
            exposed1_index = index_of_mouseclick
            state = ONE
     
    else: # invalid Click 
        pass

# draws a green rectangle at given index
def draw_green_rectangle(canvas, idx):
    canvas.draw_polygon([(50 * idx, 0),
                         (50 * idx, 100),
                         (50 * idx + 50, 100),
                         (50 * idx + 50, 0)], 1, "White", "Green")
    
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global memory_deck, exposed
    
    for idx in range(0, 16):
        if exposed[idx] == EXPOSED:
            canvas.draw_text(str(memory_deck[idx]), (15 + (50*idx) , 50), 40, "White")
        else:
            draw_green_rectangle(canvas, idx);


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric