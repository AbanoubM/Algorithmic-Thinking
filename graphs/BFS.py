'''
Created on Sep 17, 2014

@author: abanoub milad nassief

Breadth First Search Implementation
'''
from Queue import *

def bfs_visited(ugraph, start_node):
    """ implemnts BFS Algorithm, returns set of all visited nodes of a graph"""
    que = Queue()
    visited = set([])
    visited.add(start_node)  
    que.enqueue(start_node)
    while que.__len__() != 0:
        itr = que.dequeue()
        for neighbour in ugraph[itr]:
            if not visited.__contains__(neighbour):
                visited.add(neighbour)
                que.enqueue(neighbour)
    return visited

def cc_visited(ugraph):
    """ returns set of all connected components of a graph"""
    cc_set = []
    remaining_nodes = set(i for i in ugraph)
    while remaining_nodes.__len__() != 0:
        itr = remaining_nodes.pop()
        remaining_nodes.add(itr)
        temp = bfs_visited(ugraph, itr)
        for elm in temp:
            remaining_nodes.remove(elm)    
        cc_set.append(temp)        
    return cc_set        
        
def largest_cc_size(ugraph):
    """ returns size of largest path of a graph"""
    list = cc_visited(ugraph)
    max = 0
    for itr in list:
        if itr.__len__() > max :
            max = itr.__len__()-1
    return max    
    
def compute_resilience(ugraph, attack_order):
    """ prints resilience of a graph"""
    lis=[]
    lis.append(largest_cc_size(ugraph))
    for itr in attack_order:
        del ugraph[itr]
        for etr in ugraph:
            if ugraph[etr].__contains__(itr):
                ugraph[etr].remove(itr)
        lis.append(largest_cc_size(ugraph))
    return lis    
        