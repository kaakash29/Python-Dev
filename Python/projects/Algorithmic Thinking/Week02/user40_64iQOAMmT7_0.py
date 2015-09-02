"""
This file contains the implementation of the Queue Class which
contains a list & supports 2 operations engueue dequeue
__author__ = 'Kumar'
__date__= 'June 25 2015'
"""

# general imports
import urllib2
import random
import time
import math

# CodeSkulptor import
import simpleplot
import codeskulptor
codeskulptor.set_timeout(1000)

#------------------------------------------------------
#######################################################
#------------------------------------------------------

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


#---------------------------------------------------


def bfs_visited(smgraph, starting_node):
    """
    Retunrs a list of nodes in the order in
    which they are traversed.
    :param smgraph:
    :param starting_node:
    :return: List of Trsversed Nodes in Order
    """
    traversal_queue = Queue()

    visted_nodes = set([starting_node])

    traversal_queue.enqueue(starting_node)

    while not traversal_queue.isempty():
        curr_elem = traversal_queue.dequeue()
        neighbours = smgraph[curr_elem]
        for a_nebour in neighbours:
            if a_nebour not in visted_nodes:
                visted_nodes.update([a_nebour])
                traversal_queue.enqueue(a_nebour)

    return  visted_nodes

# Tests :

EX_GRAPH1 = {0:set([1, 2, 5]),
             1:set([0, 3]),
             2:set([0, 5]),
             3:set([1]),
             4:set([6, 7]),
             5:set([0, 2]),
             6:set([4]),
             7:set([4])}

EX_GRAPH0 = {0:set([1, 2, 5]),
             1:set([0, 3]),
             2:set([0, 5]),
             3:set([1]),
             4:set([]),
             5:set([0, 2]),
             6:set([]),
             7:set([])}

#print ("BFS on GRAPH0 starting at vertex 0 = ", \
#       bfs_visited(EX_GRAPH0, 0))

#print ("BFS on GRAPH0 starting at vertex 4 = ", \
#       bfs_visited(EX_GRAPH0, 4))

#------------------------------------------------------

def cc_visited(a_graph):
    """
    Consumes a graph and returns a list of
    list of connected components
    :param a_graph:
    :return:
    """
    remainin_nodes_set = set(x for x in a_graph)
    cclist = []  # list of connected components
    visited_nodes_set = () # set of visited nodes during BFS

    while len(remainin_nodes_set) > 0:
        a_node = random.choice(list(remainin_nodes_set))
        visited_nodes_set = bfs_visited(a_graph, a_node)
        remainin_nodes_set = remainin_nodes_set.difference(visited_nodes_set)
        cclist.append(visited_nodes_set)

    return cclist


# Tests :
# print ("Connected Components in GRAPH0 = ",cc_visited(EX_GRAPH0))

#------------------------------------------------------

def largest_cc_size(ugraph):
    """
    Returns the size of teh largest connected component of a graph
    :param ugraph:
    :return: integer
    """
    graph_ccs = cc_visited(ugraph)
    maxm = 0
    for conn_comp in graph_ccs:
        if len(conn_comp) > maxm:
            maxm = len(conn_comp)
        else:
            pass

    return maxm

# Test
# print ("Largest connected component in "
#       "GRAPH0 is of size = ",largest_cc_size(EX_GRAPH0))

#------------------------------------------------------

def compute_resilience(ugraph, attack_order):
    """
    Computes the resilience valu of a graph by
    removin the given node and its edges from the
    graph and then calculating the length of largest CC
    :param ugraph:
    :param attack_order:
    :return: List of CC-lengths
    CC_lengths[0] = largest_cc_size(ugraph)
    """
    resilience_list = [largest_cc_size(ugraph)]
    for a_node in attack_order:
        ugraph = remove_node_from_graph(a_node, ugraph)
        resilience_k = largest_cc_size(ugraph)
        resilience_list.append(resilience_k)

    return resilience_list

#------------------------------------------------------

def remove_node_from_graph(node2remove, dgraph):
    """
    Removes a node and all its conencting edges from
    the graph
    :param anode:
    :param smgraph:
    :return: graph with the node removed.
    """
    smgraph = dictcopy(dgraph)
    for smnode in dgraph:
        if smnode == node2remove:
            #if this node is d node to remove
            smgraph.pop(smnode)
        elif node2remove in smgraph[smnode]:
            #if the node2remove is in edges list from smnode
            #remove that edge
            smgraph[smnode].remove(node2remove)


    return smgraph

#------------------------------------------------------

def dictcopy(dicttocopy):
    """
    Returns a new dictionary with same values
    :param dicttocopy:
    :return: graph with the node removed.
    """
    new_dict = dict()
    for key, value in dicttocopy.items():
        new_dict[key] = set(value)

    return new_dict


#------------------------------------------------------
#######################################################
#------------------------------------------------------
# Code to generate the ER Graph 
#------------------------------------------------------
#######################################################
#------------------------------------------------------

def gen_ER_graph (numnodes):
    """
    Generates an undirected ER graph with randomly chosen
    probability.
    """
    graph = {}
    prob = random.random()
    
    for node in range(0, numnodes):
        graph[node]=set([])
        for connectedto in range(0, numnodes):
            porbability_of_connection = random.random()
            
            # if not connecting to self node and 
            # probility is within check 
            if   connectedto != node \
            and  porbability_of_connection < prob:
                    # connect from node to connectedto
                    
                    graph[node].add(connectedto)
                    
                    # connect from connectedto to node
                    
                    if connectedto not in graph.keys():
                        # if connectedTo is not is in graph
                        # till now
                        graph[connectedto] = set([node])
                    else:
                        # if connectedTo is already in graph
                        graph[connectedto].add(node)
                        
                        
                        
    
    return graph

print "Generating ER graph with 5 nodes "
print gen_ER_graph(5)


#------------------------------------------------------
#######################################################
#------------------------------------------------------

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
    
    
    def make_complete_graph(self, num_nodes):
        """
        :param num_nodes:
        :return: dictoiionary
        Consumes the number of nodes and returns a complete graph
        where all nodes are connected to each other.
        """
        node_set = set()

        for nodenum in range (0 , num_nodes):
            node_set.add(nodenum)

        complete_graph = dict()

        for dictindex in range(0, num_nodes):
            dup_node_set = node_set.copy()
            dup_node_set.remove(dictindex)
            complete_graph[dictindex] = dup_node_set 

        return complete_graph
    

    def upa(self,n, m):
        """
        Main function to generate a UPA graph from a 
        complete graph
        """
        graph = self.make_complete_graph(m)
        
        for newnode in range(m, n):
            
            random_nodes = self.run_trial(m)
            
            # Add the random nodes to newnodes list 
            graph[newnode] = random_nodes
            
            # Add the newnode to random_nodes's lists
            for anode in random_nodes:
                if anode not in graph.keys():
                    graph[anode] = set([newnode])
                else:
                    graph[anode].union([newnode])
                    
        return graph

#------------------------------------------------------
#######################################################
#------------------------------------------------------

#obj = UPATrial(10)
#print "Generating UPA Graph n = 10 m = 5"
#print obj.upa(10,5)


############################################
# Provided code Assignment 2
############################################

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order


#------------------------------------------------------
#######################################################
#------------------------------------------------------
# 		Code for loading computer network graph
#------------------------------------------------------
#######################################################
#------------------------------------------------------

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

#================================================
#================================================

#print len(load_graph(NETWORK_URL))
gen_ER_graph(300)
    

    

