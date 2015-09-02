"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


#############################

class Queue:
    """
    The Queue Class
    """
       
    def __init__(self):
        """
        Constructor for the class initializes a Queue of size 1
        by default.
        :return: Returns a list
        """
        self._qlist = []

    def __str__(self):
        """
        Returns a string representation of your Q
        :return: String
        """
        strn = "|"
        for char in self._qlist:
            strn = strn + str(char) + "|"
        return strn
    
    def __iter__(self):
        """
        Yields all teh elemtns of teh queue" 
        to white iterating
        """
        for elem in self._qlist:
            yield elem

    def enqueue(self, value):
        """
        Appends the valur to teh end of the Queue
        :param value:
        :return: Queue with the Vaue Appended.
        """
        return self._qlist.append(value)

    def dequeue(self):
        """
        Appends the valur to teh end of the Queue
        :param value:
        :return: Value that is being removed from front of Q.
        """
        return self._qlist.pop(0)

    def isempty(self):
        """
        Returns if teh Queue is Empty or not
        :return: Boolean
        """
        return True if len(self._qlist) < 1 else False       

#########################################################

class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        print "Tryin to clear teh game state ... "
        self._zombie_list = []
        self._human_list = []
        poc_grid.Grid.clear(self)
        
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
        print "Added a zombie to the list"
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        print "The number of zombies on the board are : ",len(self._zombie_list)
        return len(self._zombie_list)  
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        
        print "Let's get the zombies one-by-one!!"
        for zombie in self._zombie_list: 
            print "Zombie @ ",zombie
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        print "Added a human to the list"
        
    def num_humans(self):
        """
        Return number of humans
        """
        print "The number of humans on the board are : ",len(self._human_list)
        return len(self._human_list)  
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        
        print "Let's get the humans one-by-one!!"
        for human in self._human_list: 
            print "Human @ ",human
            yield human
        

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        
        MAX_DISTANCE = (self.get_grid_height() * self.get_grid_width())
        
        # a new grid visited of the same size 
        # as the original grid 
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        
        # and initialize its cells to be empty
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                visited[row][col] = EMPTY
                
        # Create a 2D list distance_field of the same size as the original 
        # grid 
        distance_field = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        
        # initialize each of its entries to be the product of
        # the height times the width of the grid.
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                distance_field[row][col] = MAX_DISTANCE
        
        # boundary that is a copy of either the zombie list 
        # or the human list. 
        entity_list = self._human_list if entity_type == HUMAN else self._zombie_list
        
        boundary = poc_grid.Queue()
                
        for elm in entity_list:
            boundary.enqueue(elm)
        
        # For cells in the queue, initialize
        # visited to be FULL and distance_field to be zero. 
        for cell in boundary:
            visited[cell[0]][cell[1]] = FULL
            distance_field[cell[0]][cell[1]] = 0
        
        # BFS implementation 
        
        while len(boundary) > 0 
            current_cell  =  boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            distance_field[current_cell[0]][current_cell[1]] + 1
            for neighhor in neighbors:
                # if neighbor_cell is not in visited
                if visited.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighhor)
                    
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        pass
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        pass

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
