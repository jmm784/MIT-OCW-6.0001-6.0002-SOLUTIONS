# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
#


# Problem 2b: Implementing load_map
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
    

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

#test_file = 'test_load_map.txt'
#test_case = str(load_map(test_file))
#assert test_case == 'a->b (10, 9)\na->c (12, 2)\nb->c (1, 1)', 'You have an error!'
#print('The load_map function has passed all tests')



#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
# I am not entirely sure what is meant when the term 'objective function' is used. If
# I had to guess I would say that it is the function that constructs the graph, in which
# case it would be our digraph function. As for our constraints, we are simply looking
# for the shortest path from A->B without exceeding our limit/distance constraint for the
# time spent outdoors (MIT is very cold in the Winter!)


# Problem 3b: Implement get_best_path

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
    get_all_paths(digraph, start, end, path, max_dist_outdoors, path_list, best_dist)
    
    if len(path_list) == 0:
        return None
    else:
        return path_list[-1]




def get_all_paths(digraph, start, end, path, max_dist_outdoors, path_list, best_dist):
    start_node = Node(start)
    path = path + [start]
    path_dist = get_path_length(digraph, path)
    
    if len(path_list) > 0:
        best_dist = get_path_length(digraph, path_list[-1])[0]
     
    if start == end:
        if path_dist[1] <= max_dist_outdoors and (best_dist == None or path_dist[0] < best_dist):
            path = path + [end]
            path_list.append(path)
        
    for edge in digraph.get_edges_for_node(start_node):
        dest_node = edge.get_destination().get_name()
        if dest_node not in path:
            if path_dist[1] <= max_dist_outdoors and (best_dist == None or path_dist[0] < best_dist):
                get_all_paths(digraph, dest_node, end, path, max_dist_outdoors, path_list, best_dist)
            
    path.pop()


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
    distance = [0,0]
    if path == None:
        return distance
    path_length = len(path)
    if path_length == (0 or 1 or None):
        return distance
    else:
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
                    

# Problem 3c: Implement directed_dfs
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
    #Initialisation of variables
    path = []
    best_path = None
    best_dist = None
    
    best_journey = get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_path)
    if best_journey == None:
        raise ValueError
    best_journey_dist = get_path_length(digraph, best_journey)[0]
    if best_journey_dist > max_total_dist:
        raise ValueError
    return best_journey
    
    
    
    
    
    

#'''
# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
#'''