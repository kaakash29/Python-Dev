"""
Cookie Clicker Simulator
"""

import simpleplot
import math
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(30000)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    def __init__(self):
        # This function initializes the local vaiables
        # of the class.
        self._total_cookies_produced = 0.0
        self._current_cookies = 0.0
        self._game_time = 0.0
        self._cps = 1.0 # rate at which cookies are being produced
        self._current_item = None
        self._current_item_cost = 0.0
        self._history = []
        self._history.append(self.__state__())

        
    def __state__(self):
        # Returns the state of teh game can be appended into 
        # history directly 
        return (self._game_time,  \
                self._current_item, \
                self._current_item_cost,\
                self._total_cookies_produced)
        
        
    def __str__(self):
        """
        Return human readable state
        """
        string = "\n\n -- COOKIES CLICKER GAME STATE REPORT -- \n\n"
        string +=" MACHINERY PRODUCED "+ str(self._total_cookies_produced) + " COOKIES TILL NOW \n"
        string +=" PLAYER HOLDS "+ str(self._current_cookies) + " COOKIES CURRENTLY \n"
        string +=" TIME IN-GAME = "+ str(self._game_time)+" \n"
        string +=" CURRENTLY PRODUCING COOKIES @ "+ str(self._cps) + " COOKIES/SEC \n"
        string +=" HISTORY OF LENGTH = "+ str(len(self.get_history()))
        string +="\n -- -- \n"
        
        return string
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return float(self._current_cookies)
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return float(self._cps)
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return float(self._game_time)
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies > cookies:
            return 0.0
        else:
            time = math.ceil((cookies - self._current_cookies)/float(self._cps))
            return time
        
        
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        #print "  WAITING FOR  . .  ", time
        if time <= 0.0:
            pass
        else:
            self._game_time += time
            self._current_cookies += (self._cps * time)
            self._total_cookies_produced += (self._cps * time)
            
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        
        #print "  Currently Holding Cookies ",self._current_cookies
        #print "  BUYING ITEM . . ", item_name," @ Cost ", cost,
        
        if self._current_cookies >= cost:
            # Can afford to bu this item
            # print " BOUGHT "
            self._cps += additional_cps
            self._current_cookies -= cost
            self._current_item = item_name
            self._current_item_cost = cost
            self._history.append(self.__state__())
        else:
            # Cannot afford the item
            # print " NOT BOUGHT "
            pass
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    
    # first thing you should do in this function is to make a clone of the
    # build_info object and create a new ClickerState object.
    
    dup_buildinfo = build_info.clone()
    simulated_clicks = ClickerState()
    
    #print "Duration for game is =", duration
    
    while simulated_clicks.get_time() <= duration:
        
        #print "Current Game Time = ",simulated_clicks.get_time()
        
        # Call the strategy function with the appropriate 
        # arguments to determine which item to purchase next. 
        
        new_item = strategy(simulated_clicks.get_cookies(), 
                            simulated_clicks.get_cps(), 
                            simulated_clicks.get_history(), 
                            (duration - simulated_clicks.get_time()),
                            dup_buildinfo)
        
        #print "Item that teh strategy wants = ",new_item
        
        # If the strategy function returns None, you should break out
        # of the loop, as that means no more items will be purchased. 
        
        if new_item == None:
            simulated_clicks.wait(duration - simulated_clicks.get_time())
            break
        
        # Determine how much time must elapse until it is 
        # possible to purchase the item. 
        time_needed = simulated_clicks.time_until(dup_buildinfo.get_cost(new_item))
        
        # print new_item, " needs time = ",time_needed
        
        # If you would have to wait past the duration of the simulation 
        # to purchase the item, you should end the simulation.
        
        # print "time left in simulation = ", duration - simulated_clicks.get_time()
        
        if time_needed > (duration - simulated_clicks.get_time()):
            # Impossible case
            simulated_clicks.wait(duration - simulated_clicks.get_time())
            break
        else:           
            # Wait until that time.
            simulated_clicks.wait(time_needed)
            #print simulated_clicks
            
            # Buy the item.
            simulated_clicks.buy_item(new_item, dup_buildinfo.get_cost(new_item),
                                                dup_buildinfo.get_cps(new_item))

            # Update the build information. 
            dup_buildinfo.update_item(new_item)

    
    return simulated_clicks


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
       
    affordable_number_of_cookies = cookies + cps * time_left
    
    min_cost = affordable_number_of_cookies
    cheapest_item = None
    
    items_list = build_info.build_items()
    
    #print "---"
    #print get_buildinfodict(build_info)
    #print "---"   
    
    for item in items_list:
                
        if build_info.get_cost(item) <= min_cost:
            min_cost = build_info.get_cost(item)
            cheapest_item = item
        else:
            pass
    
    #print "Chosen Cheapest Items is = ", cheapest_item
    return cheapest_item


def get_buildinfodict(smbuildinfo):
    """
    Returns a dictionary about teh values stores 
    in the build infor object passed
    """
    retdict = {}
    cloned_build_info = smbuildinfo.clone()
    for item in cloned_build_info.build_items():
        retdict[item] = (cloned_build_info.get_cps(item), \
                                cloned_build_info.get_cost(item))
        
    return retdict
   

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
        
    affordable_number_of_cookies = cookies + (cps * time_left)
    
    max_cost = affordable_number_of_cookies
    costliest_item = None
    #print "affordable_number_of_cookies ",affordable_number_of_cookies
    items_list = build_info.build_items()

    max_cost = float('-inf')
    
    #print get_buildinfodict(build_info)
    
    for item in items_list:
        #print "max_cost",max_cost
        #print "Item = ",item," cost ",build_info.get_cost(item)
        
        if build_info.get_cost(item) >= max_cost and \
            build_info.get_cost(item) <= affordable_number_of_cookies:
                
            max_cost = build_info.get_cost(item)
            costliest_item = item            
        else:
            pass
    
    return costliest_item
   

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    Select the item with the least cost/cps value
    """
           
    affordable_number_of_cookies = cookies + cps * time_left
    
    #print "---"
    #print get_buildinfodict(build_info)
    #print "---"
    
    # find the item with the least cost/cps ratio everytime
    
    affordable_items = [] # list of all items that are affordable
    
    for item in build_info.build_items():
        if build_info.get_cost(item) <= affordable_number_of_cookies:
            affordable_items.append(item)
    
    #print "List of affordable items = ", affordable_items
    
    costbycps = float('inf')
    selected_item = None
    for an_item in affordable_items:
        curr_item_costtocps = float(build_info.get_cost(an_item)/build_info.get_cps(an_item))
        if curr_item_costtocps <= costbycps:
            costbycps = curr_item_costtocps
            selected_item = an_item
    
    #print "returning ", selected_item
    return selected_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
    
run()

#print strategy_expensive(0.0, 1.0, [(0.0, None, 0.0, 0.0)], 5.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))    
#print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001]}, 1.15), 5000.0, strategy_none) 


