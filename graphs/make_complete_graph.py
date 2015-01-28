"""
Created on Sep 1, 2014
@author: abanoub milad nassief
"""
def make_complete_graph(num_nodes):
    """ take in param num_nodes, output a complete graph """
    graph = {}
    if num_nodes > 0 :
        for node in range(num_nodes):
            temp = set([])
            for itr in range(node):
                temp.add(itr)
            for itr in range(node + 1, num_nodes):
                temp.add(itr)      
            graph[node] = temp
    return graph