"""
Created on Sep 1, 2014
@author: abanoub milad nassief
"""
def in_degree_distribution(digraph):    
    """" take in param graph, output in degree distribution dictionary """  
    digraph = compute_in_degrees(digraph)
    graph = {}
    for degree in range(len(digraph)):
        count = 0
        for node in digraph:
            if digraph[node] == degree:
                count += 1
        if count >0:        
            graph[degree] = count
    
    return graph