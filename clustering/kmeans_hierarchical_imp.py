"""
name: abanoub milad nassief

inclues:
slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a list of clusters
"""

import math
import alg_cluster 


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]),
            min(idx1, idx2), max(idx1, idx2))


def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    pairs = set([])
    min_dis = float("inf")
    for itr in range(len(cluster_list) - 1):
        for etr in range(itr + 1, len(cluster_list)):
            temp = pair_distance(cluster_list, itr, etr)
            if temp[0] < min_dis:
                min_dis = temp[0]
                pairs = set([])
                pairs.add(temp)
            elif temp[0] == min_dis:
                pairs.add(temp)
    return pairs

def bf_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    min_tuple = (float("inf"), 0, 0)
    for itr in range(len(cluster_list) - 1):
        for etr in range(itr + 1, len(cluster_list)):
            temp = pair_distance(cluster_list, itr, etr)
            if temp[0] < min_tuple[0]:
                min_tuple = temp
    return min_tuple

def generat_v(cluster_list, horiz_order, vert_order, v_left, v_right):
    """
    Compute the vert_order by cluster_list, horiz_order
    
    """
    m_points = len(horiz_order) // 2
    max_left_value = cluster_list[horiz_order[m_points - 1]].horiz_center() 
    for index in vert_order:
        # right v
        if cluster_list[index].horiz_center() > max_left_value:
            v_left.append(index)
        # left v 
        elif cluster_list[index].horiz_center() < max_left_value:
            v_right.append(index)
        # left v    
        elif cluster_list[index].vert_center() == \
            cluster_list[horiz_order[m_points - 1]].vert_center():
            v_right.append(index)
        else:
            flag = True
            for itr in range(m_points - 2, -1, -1):
                if cluster_list[index].horiz_center() != \
                    cluster_list[horiz_order[itr]].horiz_center(): 
                    flag = False
                    break
                elif cluster_list[index].vert_center() == \
                        cluster_list[horiz_order[itr]].vert_center():
                    v_right.append(index)
                    break
            if flag:
                for itr in range(m_points, len(horiz_order)):
                    if cluster_list[index].horiz_center() != \
                        cluster_list[horiz_order[itr]].horiz_center(): 
                        break
                    elif cluster_list[index].vert_center() == \
                        cluster_list[horiz_order[itr]].vert_center():
                        v_left.append(index)
                        break
    
def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """
    # compute list of indices for the clusters
    # ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) 
                        for idx in range(len(cluster_list))]    
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] 
                   for idx in range(len(hcoord_and_index))]
     
    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) 
                        for idx in range(len(cluster_list))]    
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] 
                  for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order) 
    return (answer[0], min(answer[1:]), max(answer[1:]))

def fast_helper(cluster_list, horiz_order, vert_order):
    """
    Divide and conquer method for computing distance between closest pair of points
    Running time is O(n * log(n))
    
    horiz_order and vert_order are lists of indices for clusters
    ordered horizontally and vertically
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters

    """
    
    # base case
    if len(horiz_order) <= 3:
        min_tuple = bf_closest_pairs([cluster_list[index] 
                                        for index in horiz_order])
        return (min_tuple[0], horiz_order[min(min_tuple[1:])],
                horiz_order[max(min_tuple[1:])])
    
# divide
    m_points = len(horiz_order) // 2
    mid = (cluster_list[horiz_order[m_points]].horiz_center() + 
                 cluster_list[horiz_order[m_points - 1]].horiz_center()) / 2

    
    splited = [[], [], [], []]
    # right h
    splited[0] = horiz_order[m_points:]
    # left h
    splited[2] = horiz_order[:m_points]
    
    
    generat_v(cluster_list, horiz_order, vert_order,
              splited[1], splited[3])

    
    min_tuple = fast_helper(cluster_list, splited[0], splited[1])
    left_tuple = fast_helper(cluster_list, splited[2], splited[3])
    if left_tuple[0] < min_tuple[0]:
        min_tuple = left_tuple
    
    temp_set = [index for index in vert_order 
                if abs(cluster_list[index].horiz_center() - 
                       mid) < min_tuple[0]]         

    for u_itr in range(len(temp_set) - 1):
        for v_itr in range(u_itr + 1,
                           1 + min(u_itr + 3, len(temp_set) - 1)):
            temp = math.sqrt((cluster_list[temp_set[u_itr]].horiz_center() - 
            cluster_list[temp_set[v_itr]].horiz_center()) ** 2 + 
            (cluster_list[temp_set[u_itr]].vert_center() - 
            cluster_list[temp_set[v_itr]].vert_center()) ** 2)
            
            if temp < min_tuple[0]:
                min_tuple = (temp , min(temp_set[u_itr], temp_set[v_itr]),
                       max(temp_set[u_itr], temp_set[v_itr]))               
        
    return min_tuple
    
    
def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """    
    while len(cluster_list) > num_clusters:
#         tupl=slow_closest_pairs(cluster_list).pop()
        tupl = fast_closest_pair(cluster_list)
        cluster_list[tupl[1]].merge_clusters(cluster_list[tupl[2]])
        del cluster_list[tupl[2]]
    return cluster_list



    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    # initialize k-means clusters to be
    # initial clusters with largest populations
    
    clust = sorted(cluster_list,
                   key=lambda x: x.total_population(), reverse=True)
    
    centers = [(clust[itr].horiz_center(), \
               clust[itr].vert_center()) \
              for itr in range(num_clusters)]
    
    k_sets = [alg_cluster.Cluster(set([]), \
              clust[itr].horiz_center(), clust[itr].vert_center(), 0, 0) \
              for itr in range(num_clusters)]   
        
    for _ in range(num_iterations):
        
        k_sets = [alg_cluster.Cluster(set([]), \
              clust[itr].horiz_center(), clust[itr].vert_center(), 0, 0) \
              for itr in range(num_clusters)] 
        
        point_index = -1
        for point in cluster_list:
            min_tuple = [float("inf"), -1]
            locat = -1
            point_index += 1
            for location in centers:
                locat += 1
                temp = math.sqrt((point.vert_center() - 
                location[1]) ** 2 + 
                (point.horiz_center() - location[0]) ** 2)
                if temp < min_tuple[0]:
                    min_tuple[0] = temp
                    min_tuple[1] = locat
            k_sets[min_tuple[1]].merge_clusters(cluster_list[point_index])
        for cluster in range(len(k_sets)):
            centers[cluster] = (k_sets[cluster].horiz_center(),
                              k_sets[cluster].vert_center())
    return k_sets