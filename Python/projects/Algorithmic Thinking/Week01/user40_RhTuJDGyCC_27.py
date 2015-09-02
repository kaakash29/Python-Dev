"""
 This is a placeholder for assignment 01 of Algorithmic thinking,in
 this file we try to create a python program that computes teh degree
 distributions of a given graph in dictionary representation.#
 __author__ = "techcurrentz"
 __date__   = "June 11"
"""

EX_GRAPH0 = {0:set([1, 2]),
             1:set([]),
             2:set([])}

EX_GRAPH1 = {0:set([1, 5, 4]),
             1:set([2, 6]),
             2:set([3]),
             3:set([0]),
             4:set([1]),
             5:set([2]),
             6:set([])}

EX_GRAPH2 = {0:set([1, 5, 4]),
             1:set([2, 6]),
             2:set([3, 7]),
             3:set([7]),
             4:set([1]),
             5:set([2]),
             6:set([]),
             7:set([3]),
             8:set([1, 2]),
             9:set([0, 3, 4, 5, 6, 7])}

def make_complete_graph(num_nodes):
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
        indegree_dict[key] = 0

    for key in digraph:
        for node in digraph[key]:
            indegree_dict[node] += 1
            
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
            indegreedist[indegrees[node]] = 1
        else:
            indegreedist[indegrees[node]] += 1

    return indegreedist

# Examples :
print (" 1) Indegrees    ")
print (compute_in_degrees(EX_GRAPH0))
print (" Indegrees Distribution   ")
print in_degree_distribution(EX_GRAPH0)

print (" 2) Indegrees    ")
print (compute_in_degrees(EX_GRAPH1))
print (" Indegrees Distribution   ")
print in_degree_distribution(EX_GRAPH1)

print (" 3) Indegrees    ")
print (compute_in_degrees(EX_GRAPH2))
print (" Indegrees Distribution   ")
print in_degree_distribution(EX_GRAPH1)
