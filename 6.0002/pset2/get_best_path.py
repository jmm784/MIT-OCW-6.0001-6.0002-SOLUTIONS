# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 11:44:04 2024

@author: josep
"""

from graph import Digraph, Node, WeightedEdge
from ps2 import load_map

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


#Testing:
filename = 'mit_map.txt'
digraph = load_map(filename)
print(digraph)
node_list = list(digraph.edges.keys())
print(node_list)
print(node_list[0])
print(node_list[0].get_name())
demo_path = [[node_list[0], node_list[1], node_list[12]], 0, 0]
print(demo_path)
print(get_path_length(digraph, demo_path))
    

























