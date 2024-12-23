# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 20:36:26 2024

@author: josep
"""

#based off of the geeks for geeks article where they print all possible paths from
#src to dest for a digraph using the dfs traversal algo

from graph import Digraph, Node, WeightedEdge
from ps2 import load_map, get_path_length

filename = 'mit_map.txt'
digraph = load_map(filename)


def print_all_paths(digraph, start, end, path, max_dist_outdoors, path_list, best_dist):
    start_node = Node(start)
    path = path + [start]
    path_dist = get_path_length(digraph, path)
    
    if len(path_list) > 0:
        best_dist = get_path_length(digraph, path_list[-1])[0]
     
    if start == end:
        if path_dist[1] < max_dist_outdoors and (best_dist == None or path_dist[0] < best_dist):
            path = path + [end]
            path_list.append(path)
        
    for edge in digraph.get_edges_for_node(start_node):
        dest_node = edge.get_destination().get_name()
        if dest_node not in path:
            if path_dist[1] < max_dist_outdoors and (best_dist == None or path_dist[0] < best_dist):
                print_all_paths(digraph, dest_node, end, path, max_dist_outdoors, path_list, best_dist)
            
    path.pop()


#Tha above function works and prints all possible paths within the given constraints.
#Will now try this again with adding somemore contraints to allow us to return the best path

#test to see what happens if we call print_all_paths and there is no valid path

start = '2'
end = '9'

digraph = load_map(filename)
path_list = []
path = []
max_dist_outdoors = 1000
best_dist = None

print_all_paths(digraph, start, end, path, max_dist_outdoors, path_list, best_dist)
print('\n')
print(path_list)
print('\n')
for path in path_list:
    print(get_path_length(digraph, path))


#Results of test:
    #for some reason the path.pop() function seems to be messing up the code and when each
    #possible path is returned it then removes the final node from the path.
    #the solution, albeit a bit messy, is to simply add the final node on twice so that
    #when it is popped it is actually the original path that is returned
    #I will try to implement this in tomorrows code and see what happens



def get_all_paths(digraph, start, end, path, max_dist_outdoors, path_list):
    start_node = Node(start)
    path = path + [start]
    
    if start == end:
        path_list.append(path)
        
    for edge in digraph.get_edges_for_node(start_node):
        dest_node = edge.get_destination().get_name()
        if dest_node not in path:
            path_dist = get_path_length(digraph, path)
            if path_dist[1] < max_dist_outdoors:
                get_all_paths(digraph, dest_node, end, path, max_dist_outdoors, path_list)
            
    path.pop()
    
def get_all_paths(digraph, start, end, path, max_dist_outdoors, path_list):
    start_node = Node(start)
    path = path + [start]
    
    if start == end:
        path_list.append(path)
        
    for edge in digraph.get_edges_for_node(start_node):
        dest_node = edge.get_destination().get_name()
        if dest_node not in path:
            path_dist = get_path_length(digraph, path)
            if path_dist[1] < max_dist_outdoors:
                get_all_paths(digraph, dest_node, end, path, max_dist_outdoors, path_list)
            
    path.pop()
    




#get_all_paths(digraph, start, end, path, max_dist_outdoors, path_list)

#print(path_list)


def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    # TODO
    #Ideas:
        # - use DF traverse algo to find a possibl epath and then calculate distance
        # afterwards
        # - use Djikstra's algo if all else fails (kind of cheating...)
    
    start_node = Node(start)
    end_node = Node(end)
    if (digraph.has_node(start_node) or digraph.has_node(end_node)) == False:
        raise ValueError
        
    path_list = []
    get_all_paths(digraph, start, end, path, max_dist_outdoors, path_list)
    route_dict = {}
    
    for route in path_list:
        route_dist = get_path_length(digraph, route)
        tuple_route = tuple(route)
        route_dict[tuple_route] = route_dist[0] + route_dist[1]
    
    route_dict = dict(sorted(route_dict.items(), key=lambda item: item[1]))
    
    ordered_route_list = list(route_dict.keys())
    for route2 in ordered_route_list:
        route2 = list(route)
        route_dist2 = get_path_length(digraph, route2)
        if route_dist2[1] <= max_dist_outdoors:
            return route2



def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    path = []
    best_path = None
    best_dist = get_path_length(digraph, best_path)[0]
    best_journey = get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_path)
    best_journey_dist = get_path_length(digraph, best_journey)
    if best_journey == None or best_journey_dist[0] > max_total_dist:
        raise ValueError
    return best_journey





