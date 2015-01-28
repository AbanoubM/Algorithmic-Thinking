"""

Name: Abanoub Milad Nassief
Email: abanoubcs@gmail.com
Description: citation paper analyser

Imports physics citation graph 
"""

# general imports
from pylab import *
import math

###################################
# Code for loading citation graph


def load_graph():
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = open("phy.txt","r")
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print ("Loaded graph with", len(graph_lines), "nodes")
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

def compute_in_degrees(digraph):
    """ take in param graph, output in degree dictionary """

    graph = {}
    for node in digraph:
        graph[node] = 0
    for node in digraph:
        for itr in digraph[node]:
            graph[itr] += 1 
    return graph
                
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

def build_plot(graph):
    """
    Build plot using graph
    """
    plot = []
    for degree in graph:
            plot.append([math.log(degree), math.log(graph[degree])])
    return plot



citation_graph = load_graph()
result_graph = in_degree_distribution(citation_graph)
#Pass graph in as a parameter
plot = build_plot(result_graph)
matlibplot.plot_lines("Iteration counts", 600, 600,"in-degree", "distribution", [plot])



