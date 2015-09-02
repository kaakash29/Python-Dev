"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60000)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    #print "Player = X " if player is provided.PLAYERX else "Player = O "
    #print board
    
    
    # if the game on curr_board has already completed return teh score 
    # and return no valid move
    # Base Case for recursion 
    if board.check_win() != None:
        
        #print "Current Board is already Over ... "
        
        #if provided.PLAYERX is board.check_win():
            #print "Player = X has won " 
        #elif provided.PLAYERX is board.check_win():
            #print "Player = O has won "
        #else:
            #print "The Game is DRAWN !!!"

        return SCORES[board.check_win()], (-1, -1)
    
    # else  go for the recursive case
    else:
        #print "\n\nCurrent Board is not won ... "
        curr_board = board.clone()    
        possible_moves = curr_board.get_empty_squares()
        
        best_scores = []
        
        for a_move in possible_moves:
            # make a move from the possible moves and apply the Algo 
            # on the newly created board 
            curr_board = board.clone()
            curr_board.move(a_move[0], a_move[1],  player)
            #print "Board after making the move ... "
            #print curr_board
            
            curr_score, dummy_winning_move = mm_move(curr_board, provided.switch_player(player))
            #print "Board Score = ",curr_score

            best_scores.append((curr_score, a_move))
            
        
        print "Best Scores list = "
        print best_scores

        if player is provided.PLAYERO:
            best_scores.sort(key=lambda x: x[0])
            return best_scores[0][0], best_scores[0][1] 
        
        elif player is provided.PLAYERX: 
            best_scores.sort(reverse=True, key=lambda x: x[0])
            return best_scores[0][0], best_scores[0][1]

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)


# smboard = [[2,1,2],
#           [2,2,3],
#           [3,1,3]]

# bobj = provided.TTTBoard(3, True, smboard)

# print bobj
# print mm_move(bobj, 3)

# mm_move(provided.TTTBoard(3, 
#                          False,
#                          [[provided.PLAYERX, provided.PLAYERX, provided.PLAYERO],
#                           [provided.EMPTY,   provided.PLAYERX, provided.PLAYERX],
#                           [provided.PLAYERO, provided.EMPTY,   provided.PLAYERO]]),
#        provided.PLAYERO)

# mm_move(provided.TTTBoard(3, 
#                          False,
#                          [[provided.EMPTY, provided.PLAYERX, provided.EMPTY],
#                           [provided.PLAYERO, provided.PLAYERX, provided.EMPTY],
#                           [provided.PLAYERO, provided.EMPTY, provided.EMPTY]]), provided.PLAYERO)

