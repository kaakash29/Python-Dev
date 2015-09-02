#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Kumar
#
# Created:     27/07/2015
# Copyright:   (c) Kumar 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import random
import math
import time
import alg_cluster as C

#import codeskulptor
#codeskulptor.set_timeout(1000000)


######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters

    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))

####

def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    distance = float('inf')
    index1 = -1
    index2 = -1

    for idx1 in range(len(cluster_list)):
        for idx2 in range(len(cluster_list)):

            if idx1 == idx2:
                continue
            else:
                pair_dist_tuple = pair_distance(cluster_list, idx1, idx2)

                #print "Distance_tuple = ", pair_dist_tuple

                if pair_dist_tuple[0] < distance:
                    distance = pair_dist_tuple[0]
                    index1 = pair_dist_tuple[1]
                    index2 = pair_dist_tuple[2]
                else:
                    continue


    return (distance, index1, index2)

########
# tests
########

CL_LIST1 = [
    C.Cluster(set([1069]), 740.09731366, 463.241137095, 88787, 4.0E-05),
    C.Cluster(set([1067]), 741.064829551, 454.67645286, 16310, 3.4E-05),
    C.Cluster(set([1061]), 730.413538241, 465.838757711, 25764, 3.8E-05),
    C.Cluster(set([1031]), 726.661721748, 459.039231303, 43615, 3.8E-05),
    C.Cluster(set([1045]), 733.967850833, 457.849623249, 49129, 3.9E-05)
]

#print "Return Tuple = ", slow_closest_pair(CL_LIST1)


#######

def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip

    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.
    """
    #print "Cluster List = ", cluster_list
    dummy_s = []

    for dummy_idx in range(0 , len(cluster_list)):
        if abs(cluster_list[dummy_idx].horiz_center() - horiz_center) < half_width:
            dummy_s.append(dummy_idx)

    #print "List of Indexes close to centre = ",S

    dummy_s.sort(key = lambda idx: cluster_list[idx].vert_center()) # sorted list in non decreasing order of y coord

    #print "Sorted List of Indexes close to centre = ",S

    dummy_k = len(dummy_s)

    #print "Len of S  = ",k

    distance = float('inf')
    index1 = -1
    index2 = -1

    for dummy_u in range(0, dummy_k - 2 + 1):
        #print "S[u = ",u,"] : ", S[u]
        for dummy_v in range((dummy_u + 1), min(dummy_u + 3 + 1, dummy_k - 1 + 1)):
            #print "S[v = ",v,"] : ", S[v]
            #print "distance = ",distance
            #print "2 point diff = ",(cluster_list[S[u]].distance(cluster_list[S[v]]))
            if (cluster_list[dummy_s[dummy_u]].distance(cluster_list[dummy_s[dummy_v]])) < distance:
                distance = cluster_list[dummy_s[dummy_u]].distance(cluster_list[dummy_s[dummy_v]])
                index1 = dummy_s[dummy_u]
                index2 = dummy_s[dummy_v]

    return (distance, min(index1, index2), max(index1, index2))

#########
# Tests
#########

#print closest_pair_strip(CL_LIST1, 731.0, 5.0)


#######

def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """

    dummy_n = len(cluster_list)

    if dummy_n <= 3:
        return slow_closest_pair(cluster_list)

    else:
        dummy_m = int(dummy_n//2)

        cluster_list.sort(key = lambda cluster_list: cluster_list.horiz_center())

        left_cluster_list =  [cluster_list[idx] for idx in range(0, dummy_m)]
        right_cluster_list = [cluster_list[idx] for idx in range(dummy_m, dummy_n)]

        least_left = fast_closest_pair(left_cluster_list)
        least_right = fast_closest_pair(right_cluster_list)

        if least_left <= least_right:
            distance = least_left[0]
            index1 = least_left[1]
            index2 = least_left[2]
        else:
            distance = least_right[0]
            index1 = least_right[1] + dummy_m # since in new lsit the indices
            index2 = least_right[2] + dummy_m # have started at 0 again

        mid = 0.50 * (cluster_list[dummy_m - 1].horiz_center() + cluster_list[dummy_m].horiz_center()) # middle line

        centre_tuple = closest_pair_strip(cluster_list, mid, distance)

        if distance < centre_tuple[0]:
            return (distance, index1, index2)
        else:
            return centre_tuple


#######
#Tests:
#######

#print fast_closest_pair(CL_LIST1)

######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list

    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """

    final_cluster_list = [x.copy() for x in cluster_list]

    while len(final_cluster_list) > num_clusters:

        closest_pair_tuple = fast_closest_pair(final_cluster_list)

        index1 = closest_pair_tuple[1]
        index2 = closest_pair_tuple[2]
        cluster1 = final_cluster_list[closest_pair_tuple[1]]
        cluster2 = final_cluster_list[closest_pair_tuple[2]]

        new_cluster = cluster1.merge_clusters(cluster2)

        temp_cluster = []
        for dummy_idx in range(len(final_cluster_list)):
            if dummy_idx != index1 and dummy_idx != index2:
                temp_cluster += [final_cluster_list[dummy_idx]]
        temp_cluster += [new_cluster.copy()]


        final_cluster_list = temp_cluster

    return final_cluster_list

#######
# tests
#######

#print "heirarchical_clustering "
#print hierarchical_clustering(CL_LIST1, 2)


######################################################################
# Code for k-means clustering

def initial_cluster(cluster_list, num_clusters):
    """
    Creates an inital CLuster list of n cluster with
    highest population
    """
    cluster = [dummy_cluster.copy() for dummy_cluster in cluster_list]
    cluster.sort(key = lambda cluster_list: cluster_list.total_population(), reverse = True)
    # position initial clusters at the location of clusters with largest populations
    center = [dummy_cluster for dummy_cluster in cluster[:num_clusters]]

    return center


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list

    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # createa duplicate cluster_list
    dup_cluster_list = [elem.copy() for elem in cluster_list]

    # choose initial-k clusters for dividing
    # returns a list of num_clusters clusters with the highest population
    clstr_centre_list = initial_cluster(dup_cluster_list, num_clusters)

    # print clstr_centre_list

    for dummy_idx in range(num_iterations):
        # Create alist of empty_cluster_centres corresponding to the
        # Cluster_centre_list instead of adding to the original
        temp_cluster_centres  = \
        [C.Cluster(set([]), 0, 0, 0, 0) for dummy_idx in range(num_clusters)]

        # print "Temp Cluster Centres = ",temp_cluster_centres

        for a_cluster in dup_cluster_list:
            # find the closest cluster_centre for each cluster

            closest_centre_index = -1   # stores index of closest cluster centre
            min_distance = float('inf') # initialize dist closest_cluster = inf

            for a_cluster_centre in clstr_centre_list:
                # loop over teh clstr_centre_list to find the cluster_centre
                # closest to this cluster
                curr_distance =  a_cluster.distance(a_cluster_centre)
                # print "Distance = ", curr_distance
                if curr_distance < min_distance:
                    min_distance = curr_distance
                    closest_centre_index = \
                    clstr_centre_list.index(a_cluster_centre)

            # print "Index of the closest centre = ",closest_centre_index

            # closest_cluster_centre's index =  closest_centre_index
            # merge a_cluster to the cluster_centre with closest_centre_index
            # then go for next iteration with the updated  cluster_centre list
            if temp_cluster_centres[closest_centre_index] == \
                                                C.Cluster(set([]), 0, 0, 0, 0):
                temp_cluster_centres[closest_centre_index] = a_cluster.copy()
            else:
                temp_cluster_centres[closest_centre_index].merge_clusters(a_cluster)


        # copy the current_cluster centre list to the initial cluster centre
        # list and continue looping
        for dummy_center in range(num_clusters):
            clstr_centre_list[dummy_center] = temp_cluster_centres[dummy_center].copy()

    return temp_cluster_centres

#print "K means = "
#print kmeans_clustering(CL_LIST1, 2, 3)


##################################
# 	PHASE 2 IMPLEMENTATIOn
##################################


def gen_random_clusters(num_clusters):
    """
    Generates a list of clusters randompy generated
    and appends them to a list
    """
    ret = []
    for idx in range(num_clusters):
        nu_cluster = C.Cluster (set([idx]),
                  (random.random() * 2 - 1),
                  (random.random() * 2 - 1),
                  (random.randrange(10000)),
                  (random.random()))

        ret.append(nu_cluster)

    return ret

#print gen_random_clusters(4)

def calc_running_times(fn, in_fn, num_nodes):
    """
    Returns a list of running times times of a functions.
    Consumes a fn and another function to generate its input
    """
    running_times = []
    for idx in range(num_nodes):

        inp = in_fn(idx)
        t1 = time.time()
        fn(inp)
        t2 = time.time()
        running_time = t2 - t1

        running_times.append(running_time)

    return running_times

FCP = (calc_running_times(fast_closest_pair, gen_random_clusters, 200))
SCP = (calc_running_times(slow_closest_pair, gen_random_clusters, 200))


