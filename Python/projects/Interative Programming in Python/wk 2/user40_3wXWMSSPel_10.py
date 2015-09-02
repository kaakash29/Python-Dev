# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# Global variables 
Range = 100  # defaulted to 100
target = 0
guesses = 0


# helper function to start and restart the game
def new_game():
    """
    Creates a new game with fresh state, note that the 
    default value of state holder Rangge is used unless
    explicitly set before
    """
    global target, Range, guesses
    
    if Range == 100: 	
            guesses = 7
    elif Range == 1000:
            guesses = 10
        
    target = random.randrange(0, Range)
    print "----------- New Game ---------------"
    print "Selected Range : 1 to ", Range
    print "Remaining guesses : ", guesses, "\n"
    print "GOOD LUCK !!!"
    


# define event handlers for control panel
def range100():
    """
    Button handler for seting Range to 0 - 100
    Sets teh range value and restarts teh game
    """
    global Range
    Range = 100
    print "\n\nGame Range Changed !!!\n\n"
    new_game()

    
def range1000():
    """
    Button handler for seting Range to 0 - 100
    Sets teh range value and restarts teh game
    """
    global Range
    Range = 1000
    print "\n\nGame Range Changed !!!\n\n"
    new_game()
    
def input_guess(smguess):
    """
    Input field handler for getting and evaluating the guess
    provides teh result to the user.
    """
    global guesses, Range, target
    
    
    # subtract 1 from remaining guesses
    guesses -= 1
    
    if guesses < 1:
        print "\n\nSorry !!! You Lose  "
        print "Please Try Again !!!\n\n"
        new_game()
    
    # Convert the guess to a string
    try:
        guess = int(smguess)
    except ValueError:
        print "Invalid Input !!!"
        return
        
    print "\n"
    print "You' ve guessed : ",guess
    
    
    
    # Game evalaution logic
    if guess < Range and guess > 0:
        if guess < target:
            print "Guess Higher !!"
        elif guess > target:
            print "Guess Lower !!"
        else:
            print "Correct Guess !! \n\n"
            print "Lets Start with a new target \n\n"
            new_game()
    else:
        print "Number out of guessing range !!"
        print "Selected Range is  1 to ", Range
        
    print "Remaining Guesses : ",guesses
    
    
# create frame
smframe = simplegui.create_frame("Guessing Game !!", 400,200)

# register event handlers for control elements and start frame
smframe.add_button("Range 0 to 100", range100)
smframe.add_button("Range 0 to 1000", range1000)
smframe.add_input("Enter your Guess",input_guess, 200)

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
