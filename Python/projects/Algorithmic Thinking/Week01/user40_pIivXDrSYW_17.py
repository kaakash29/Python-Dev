"""
Provided code for application portion of module 1

1) Imports physics citation graph 

2) Helper class for implementing efficient version
of DPA algorithm

"""

# general imports
import urllib2
import simpleplot
import math
import random
import codeskulptor
codeskulptor.set_timeout(10000)

# Global Constants 
STANDARD = True
LOGLOG = False


#######################
# SOME HELPER FUNCTIONS

def totalInDegree(graph):
    indeg_dist = in_degree_distribution(graph)
    sum = 0 
    for node in indeg_dist:
        sum += node
        
    return sum
        
def choose_random_nodes(graph, total):
    list_of_Rnodes = set()
    in_degrees = compute_in_degrees(graph)
    
    for node in graph:
        probability = (in_degrees[node] + 1)/total 
        if random.random() < probability:
            list_of_Rnodes.add(node)
    
    return list_of_Rnodes
        
def numberOfNodes(graph):
    numOfNodes = 0 
    for nodes in graph:
        numOfNodes += 1
    return numOfNodes

#######################

class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]
        

    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
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

        complete_graph = {}

        for dictindex in range(0, num_nodes):
            dup_node_set = node_set.copy()
            dup_node_set.remove(dictindex)
            complete_graph[dictindex] = dup_node_set 

        return complete_graph

    def dpa(self,n, m):
        print "Inside DPA"
        graph = self.make_complete_graph(m)
        for newnode in range(m, n):
            random_nodes = self.run_trial(m)
            new_graphelem = {newnode: random_nodes}
            graph[newnode] = random_nodes
            
        print "Returning From DPA"
        return graph

###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


def compute_in_degrees(digraph):
    """
    :param digraph: Is the dictionary representation of a directed graph
    :return: indegree_computation: dictionary representation of
    the in-degrees of a digraph

    Consumes a directed graph and computes the in-degree distribution representation
    the directed graph.
    """
    indegree_dict = {}
    for key in digraph:
        indegree_dict[key] = 0.0

    for key in digraph:
        for node in digraph[key]:
            indegree_dict[node] += 1.0
            
    return indegree_dict


def in_degree_distribution(digraph):
    """
    :param digraph: 
    :return: Dictionary representing the degree distributions
    of teh input digraph
    """
    indegrees = compute_in_degrees(digraph)
    indegreedist = {}
    for node in indegrees:
        if indegrees[node] not in indegreedist:
            indegreedist[indegrees[node]] = 1.0
        else:
            indegreedist[indegrees[node]] += 1.0

    return indegreedist


def normalize_dist(degree_dist):
    """
    :param degree_dist: 
    :return: void:
    Consumes a unnormalized degree distribution optained from
    a large data det of Citation Digraph 
    Normalizes the indegree disribution
    """
    normalize_deg_dist = {}
    
    oldsum = 0
    for key in degree_dist:
        oldsum += degree_dist[key]
        
    for key in degree_dist:
        if key != 0.0: 
            normalize_deg_dist[key] = degree_dist[key]/oldsum
    
    return normalize_deg_dist
        

def avgOutDegree(graph):
    totaloutdeg = 0.0
    totalnode = 0.0
    for node in graph:
        totaloutdeg += len(graph[node])
        totalnode += 1.0
        
    avgoutdegree = totaloutdeg/totalnode
    return avgoutdegree
    
    
def distribution(graphurl, plot_type=LOGLOG):
    """
    :param void: 
    :return: void:
    The main function to get the indegree distribution 
    LOGLOG plot for a given citation digraph.
    1) Load the citation digraph to dictionary structure 
    2) Get the in_degree distribution for the citation digraph
    3) Normalize the indegree Distribution for the given digraph
    4) Plot the indegree distribution on a LOGLOG type plot
    """
    
    # Step 1
    if isinstance(graphurl, str):
        citation_graph = load_graph(graphurl)
    else:
        citation_graph = graphurl
    
    # Step 2
    in_degdist = in_degree_distribution(citation_graph)
    
    # Step 3
    normalized_dist = normalize_dist(in_degdist)
    
    # Step 4   
    plot = []
    
    for input_val in normalized_dist:
        norm_degree = normalized_dist[input_val]
        if plot_type == LOGLOG:
            plot.append([math.log(input_val), math.log(norm_degree)])
        else:
            plot.append([input_val, norm_degree])
    
    simpleplot.plot_scatter("Degree Distribution", 400, 400, 
                      "log(indegree)", "log(normalized distribution)", [plot])
    
    print "Avg Out Degree For this graph is = ", avgOutDegree(citation_graph)

#----------------------------
# Call to main function 
#----------------------------
#distribution(CITATION_URL)

def genERgraph (numnodes):
    graph = {}
    prob = random.random()
    for node in range(0, numnodes):
        graph[node]=[]
        for connectedto in range(0, numnodes):
            porbability_of_connection = random.random()
            if connectedto != node \
               and  porbability_of_connection < prob:
                        graph[node].append(connectedto)
    
    return graph

#distribution(genERgraph(700))


# -----------------------------

obj = DPATrial(13)
distribution (obj.dpa(27770, 13))