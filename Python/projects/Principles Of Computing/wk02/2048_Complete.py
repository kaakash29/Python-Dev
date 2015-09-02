"""
Clone of 2048 game.
"""
import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP    = 1
DOWN  = 2
LEFT  = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP:   (1, 0),
           DOWN: (-1,0),
           LEFT: (0, 1),
           RIGHT:(0,-1)}

def slid_nz_front(line):
    """
    Consumes a line and slides all the non-zero
    elements of teh line infront and returns a 
    list
    """
    newline = [0 for elm in range(len(line))]
    
    index = 0
    for elm in range(0, len(line)):
        if(line[elm] != 0):
            newline[index] = line[elm]
            index += 1
    
    return newline    	
    
def merge_two(line):
    """
    Merges teh two consecutive elements of a 
    list and replaces them by double and 0
    """
    nuline = line
    for elm in range (0, len(line) - 1, 1):
        if line[elm] == line[elm + 1]:
            nuline[elm] = 2* line[elm]
            nuline[elm + 1] = 0
        else:
            nuline[elm] = line[elm]
            nuline[elm+1] = line[elm + 1]
            
    return nuline
           
def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    list1 = slid_nz_front(line)
    # list after sliding
    list2 = merge_two(list1)
    # list after merging
    list3 = slid_nz_front(list2)
    # list after sliding again
    
    return list3


class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width):
        """
        1) Class constructor 
        2) Stores the board height and width 
        3) Calls reset() to create a new board
        """
        self._height = grid_height
        self._width = grid_width
        self._initdict = { UP: [(0, col) for col in range(self._width)],
                         DOWN: [((self._height - 1), col) for col in range(self._width)], 
                         LEFT: [(row, 0) for row in range(self._height)],
                         RIGHT:[(row,(self._width - 1)) for row in range(self._height)]
        }
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        1) Create s grid of height x width
        2) Initialize the grid with all zeros
        3) Call new_tile() to add the initial tiles        
        """
        self._grid = [[row + col for col in range(self._width)]
                           for row in range(self._height)]
        self.initialize_grid(0)
        self.new_tile()
        self.new_tile()
        
    def initialize_grid(self, value):
        """
        Traveses through the grid and initializes 
        all the cells with 0's
        """
        for row in range (0, self._height, 1):
            for column in range (0, self._width, 1):
                self._grid[row][column] = 0
         
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        string = ""
        for row in range (0, self._height, 1):
            
            string += "\n"
            for column in range (0, self._width, 1):
                string +=  "    " + str(self._grid[row][column])      
        
        return string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        1) Run throught the list of initial positions and 
        2) Traverse each row/column by adding the direction offset
        3) Create a list of traversed value and pass to the merge function.
        4) Replace the merged list back to the locations
        """
        
        moved = False 			# boolean value to track change in grid
        
        init_dir_list = self._initdict[direction]
        
        mv_offset = OFFSETS[direction]
        
        maxm = (self._height - 1) if mv_offset[0] != 0 else (self._width - 1)

        for start_cell in init_dir_list:
            # Iterate through the initial direction list for start_cell
            list2merge = []    
            # Get list to merge
            
            getter = 0
            for getter in range(maxm + 1):
                row = start_cell[0] + getter * mv_offset[0]
                col = start_cell[1] + getter * mv_offset[1]
                
                list2merge.append(self._grid[row][col])
            
            # Merge operation on list2merge
            
            mergedlist = merge(list2merge)
            
            # Check whether relacing is required or not ?
            
            if list2merge == mergedlist:
                #print "No movement"
                pass
            else:
                #print "Movement Observed"
                moved = True
                merger = 0 
                for merger in range(maxm + 1):
                    row = start_cell[0] + merger * mv_offset[0]
                    col = start_cell[1] + merger * mv_offset[1]
                    self._grid[row][col] = mergedlist[merger]
                
                
        
        # If there was movement in the grid create a new tile
        if moved:
            self.new_tile()
            
           
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        freecells = []
        freecells = self.get_empty_cells()
        
        if len(freecells) == 0:
            print "NO Cells are free"
        else:
            randsel = random.randint(0, len(freecells) -1)
            randval = random.choice([2,2,2,2,2,2,2,2,2,4])
            
            sel_cell = freecells[randsel]
            
            row = sel_cell[0]
            col = sel_cell[1]
            
            self._grid[row][col] = randval
         
        
    def get_empty_cells(self):
        """
        Creates a list of tuples of empty cells (ones having 0)
        and returns the same for plaing a new time.
        """
        emp = []
        for row in range (0, self._height, 1):
            for column in range (0, self._width, 1):
                if(self._grid[row][column] == 0):
                    emp.append((row, column))
                else:
                    continue
        
        return emp
    

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        
        return self._grid[row][col]

# Call to GUI 

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

# Tests 
__obj__ = TwentyFortyEight(4, 4)
__obj__.set_tile(0, 0, 2)
__obj__.set_tile(0, 1, 0)
__obj__.set_tile(0, 2, 0)
__obj__.set_tile(0, 3, 0)
__obj__.set_tile(1, 0, 0)
__obj__.set_tile(1, 1, 2)
__obj__.set_tile(1, 2, 0)
__obj__.set_tile(1, 3, 0)
__obj__.set_tile(2, 0, 0)
__obj__.set_tile(2, 1, 0)
__obj__.set_tile(2, 2, 2)
__obj__.set_tile(2, 3, 0)
__obj__.set_tile(3, 0, 0)
__obj__.set_tile(3, 1, 0)
__obj__.set_tile(3, 2, 0)
__obj__.set_tile(3, 3, 2)

print __obj__.__str__()
print "\nMOVE UP"
__obj__.move(UP)
print __obj__.__str__()


__obj__ = TwentyFortyEight(4, 5)
__obj__.set_tile(0, 0, 8)
__obj__.set_tile(0, 1, 16)
__obj__.set_tile(0, 2, 8)
__obj__.set_tile(0, 3, 16)
__obj__.set_tile(0, 4, 8)
__obj__.set_tile(1, 0, 16)
__obj__.set_tile(1, 1, 8)
__obj__.set_tile(1, 2, 16)
__obj__.set_tile(1, 3, 8)
__obj__.set_tile(1, 4, 16)
__obj__.set_tile(2, 0, 8)
__obj__.set_tile(2, 1, 16)
__obj__.set_tile(2, 2, 8)
__obj__.set_tile(2, 3, 16)
__obj__.set_tile(2, 4, 8)
__obj__.set_tile(3, 0, 16)
__obj__.set_tile(3, 1, 8)
__obj__.set_tile(3, 2, 16)
__obj__.set_tile(3, 3, 8)
__obj__.set_tile(3, 4, 16)
print __obj__.__str__()
print "\nMOVE UP"
__obj__.move(UP) 
print __obj__.__str__()


__obj__ = TwentyFortyEight(5, 6)
__obj__.set_tile(0, 0, 0)
__obj__.set_tile(0, 1, 2)
__obj__.set_tile(0, 2, 4)
__obj__.set_tile(0, 3, 8)
__obj__.set_tile(0, 4, 8)
__obj__.set_tile(0, 5, 32)
__obj__.set_tile(1, 0, 16)
__obj__.set_tile(1, 1, 2)
__obj__.set_tile(1, 2, 4)
__obj__.set_tile(1, 3, 16)
__obj__.set_tile(1, 4, 64)
__obj__.set_tile(1, 5, 32)
__obj__.set_tile(2, 0, 0)
__obj__.set_tile(2, 1, 2)
__obj__.set_tile(2, 2, 4)
__obj__.set_tile(2, 3, 8)
__obj__.set_tile(2, 4, 0)
__obj__.set_tile(2, 5, 32)
__obj__.set_tile(3, 0, 16)
__obj__.set_tile(3, 1, 16)
__obj__.set_tile(3, 2, 16)
__obj__.set_tile(3, 3, 16)
__obj__.set_tile(3, 4, 16)
__obj__.set_tile(3, 5, 16)
__obj__.set_tile(4, 0, 16)
__obj__.set_tile(4, 1, 8)
__obj__.set_tile(4, 2, 4)
__obj__.set_tile(4, 3, 4)
__obj__.set_tile(4, 4, 16)
__obj__.set_tile(4, 5, 2)
print __obj__.__str__()
print "\nMOVE DOWN"
__obj__.move(DOWN)
print __obj__.__str__()

