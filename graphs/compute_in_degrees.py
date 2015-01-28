"""
Created on Sep 1, 2014
@author: abanoub milad nassief
"""
def compute_in_degrees(digraph):
    """ take in param graph, output in degree dictionary """

    graph = {}
    for node in digraph:
        graph[node] = 0
    for node in digraph:
        for itr in digraph[node]:
            graph[itr] += 1 
    return graph
 