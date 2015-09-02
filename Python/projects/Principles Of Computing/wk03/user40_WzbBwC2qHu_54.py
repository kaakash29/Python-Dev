"""
Monte Carlo Tic-Tac-Toe Player
"""

# Imports 
import random
import poc_ttt_gui
import poc_ttt_provided as provided
import codeskulptor

# set the time to higher value
codeskulptor.set_timeout(50)


# Constants for Monte Carlo simulator
NTRIALS = 128       # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player



def mc_trial(board, player):   
    """
    TODO : 
    Takes a current board and the next player to move. 
    The function should play a game starting with the 
    given player by making random moves, alternating 
    between players. The function should return when 
    the game is over
    """
    while (True):
        empt_bxs = board.get_empty_squares()
        
        if len(empt_bxs) < 1:
            return

        move_in_box = random.choice(empt_bxs)
        
        board.move(move_in_box[0], move_in_box[1], player)
        
        winner = board.check_win()
        
        if  winner == None:
            player = provided.switch_player(player)
            continue
        else:
            break
    
    # on completing the game just 
    return 



def mc_update_scores(scores, board, player):
    """
    TODO : 
    Takes a completed game board , the machine player, 
    computes the score and updates the score grid.
    """
    machine_player = player
    board_winner = board.check_win()

    # is board_winner a machine player?
    # YES -> SCORE_CURRENT and -SCORE_OTHER
    # NO -> -SCORE_CURRENT and +SCORE_OTHER
    
    if board_winner == provided.DRAW:
        # if game is draw return without touching board 
        return 
    elif board_winner == machine_player:
        mc_machine = SCORE_CURRENT
        mc_other = -SCORE_OTHER
    else:
        mc_machine = -SCORE_CURRENT
        mc_other = SCORE_OTHER
 
    # traverse over score and add the delta scores  
    # to the score grid
    
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            square_winner = board.square(row, col)
            
            if square_winner == provided.EMPTY:
                pass
            elif square_winner == machine_player: 
                scores[row][col] += mc_machine
            else:
                scores[row][col] += mc_other   



def get_best_move(board, scores):
    """
    TODO :
    Takes a current board and a grid of scores.
    The function should find all of the empty 
    squares with the maximum score and randomly 
    return one of them as a (row, column) tuple
    """
    
    # Setting maxm to a very large -ve value
    maxm = -99999999 
    
    empt_sq = board.get_empty_squares()
    
    for iterator in empt_sq:
        if scores[iterator[0]][iterator[1]] > maxm:
            maxm = scores[iterator[0]][iterator[1]]

    max_list = []
    for iterator in empt_sq:
        if scores[iterator[0]][iterator[1]] == maxm:
            max_list.append(iterator)

    return random.choice(max_list)
    

    
def mc_move(board, player, trials):
    """
    TODO :
    Takes a current board, which player the 
    machine player is, and the number of trials to run.
    The function should use the Monte Carlo simulation
    described above to return a move for the machine 
    player in the form of a (row, column) tuple. 
    """
    row = 0 
    col = 0
    
    # Creating a score array
    scores = [[0 for col in range(board.get_dim())] \
                 for row in range(board.get_dim())]
 
    while trials > 0:
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
        trials -= 1
    
    # Adding this line to prevent a warning 
    # from OwlTest 
    trials = row * col
    
    best_move = get_best_move(board, scores)
    return best_move

# ----------------------------------------------------
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.
# ---------------------------------------------------
# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
# ----------------------------------------------------