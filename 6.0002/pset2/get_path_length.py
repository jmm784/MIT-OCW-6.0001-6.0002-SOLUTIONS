# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 11:44:04 2024

@author: josep
"""

from graph import Digraph, Node, WeightedEdge
from ps2 import load_map

'''

def get_path_length(digraph, path):
    journey = path[0]
    path_length = len(path[0])
    print(path_length)
    distance = [0,0]
    if path_length == 1 or 0:
        print('the path length = 0')
        return distance
    else:
        for i in range(len(path)):
            print('done1')
            for j in digraph.edges[journey[i]]:
                print('done2')
                try:
                    print('done3')
                    print(j.get_destination())
                    print(journey[i+1])
                    if j.get_destination() == journey[i+1]:
                        print('done4')
                        distance[0] += int(j.get_total_distance())
                        distance[1] += int(j.get_outdoor_distance())
                        print(distance)
                except:
                    IndexError()
                
    return distance

'''

def get_path_length(digraph, path):
    '''

    Parameters
    ----------
    digraph : Digraph instance
        DESCRIPTION.
    path : list
        list of strings that have the same names as nodes.
        They will need to be converted as part of this function

    Returns
    -------
    A list of 2 components by the name 'distance'. Element [0] will
    be the total distance travelled along that path and element [1]
    will be the total outdoor distance travelled along that path.

    '''
    path_length = len(path)
    distance = [0,0]
    print('done1')
    if path_length == (0 or 1):
        print('done1.5')
        return distance
    else:
        print('done2')
        node_path = []
        for node in path:
            node_path.append(Node(node))
        try:
            for i in range(path_length):
                for w_edge in digraph.edges[node_path[i]]:
                    dest_name = w_edge.get_destination()
                    if dest_name == node_path[i+1]:
                        distance[0] += int(w_edge.get_total_distance())
                        distance[1] += int(w_edge.get_outdoor_distance())
        except:
            IndexError()
            
    return distance

#Testing:
filename = 'mit_map.txt'
digraph = load_map(filename)
print(digraph)
print('\n')
node_list = list(digraph.edges.keys())
print(node_list)


demo_path = [['32', '36', '34', '38', '39', '13'], 0, 0]

print(demo_path)


























