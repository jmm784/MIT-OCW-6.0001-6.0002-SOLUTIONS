# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 15:35:48 2024

@author: josep
"""

from graph import Digraph, Node, WeightedEdge

def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """

    # TODO
    print("Loading map from file...")
    
    file = map_filename
    open_file = open(file,'r')
    line = open_file.readline()


    digraph = Digraph()
    while line:
        
        line = line.rstrip('\n')
        line = line.split(' ')
        fromm = Node(line[0])
        to = Node(line[1])
        wedge = WeightedEdge(fromm, to, line[2], line[3])

        if not digraph.has_node(fromm):
            digraph.add_node(fromm)
        if not digraph.has_node(to):
            digraph.add_node(to)
        digraph.add_edge(wedge)
        line = open_file.readline()

    open_file.close()

    return digraph