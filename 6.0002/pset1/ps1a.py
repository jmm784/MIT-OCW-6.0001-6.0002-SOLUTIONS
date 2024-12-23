###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
from cow_class import Cow

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    
    myfile = open(filename)
    myline = myfile.readline()
    cow_list = []
    cow_dict = {}

    while myline:
        myline = myline.rstrip('\n')
        myline_list = myline.split(',')
        cow_list.append(myline_list)
        cow_dict[myline_list[0]] = myline_list[1]
        myline = myfile.readline()
    
    myfile.close()    
    
    return cow_dict
    

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    
    cows_order = dict(sorted(cows.items(), key=lambda item:item[1], reverse=True))
    
    total_trips = []
    
    while len(cows_order) > 0:
        
        name_list = list(cows_order.keys())
        
        trip = []
        w = 0
        
        for i in name_list:
            val = int(cows_order[i])
            
            if (val + w) <= limit:
                trip.append(i)
                w += val
                del cows_order[i]
            
        total_trips.append(trip)
    
    return total_trips
    


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    
    cows_copy = cows
    
    cows_names = list(cows_copy.keys())
    all_partitions = list(get_partitions(cows_names))
    all_partitions_ordered = sorted(all_partitions, key=len)
    
    
    for partition in all_partitions_ordered:
        parts_dict = {}
        for trip in partition:
            trip = tuple(trip)
            w = 0
            for cow in trip:
                w += int(cows_copy[cow])
            parts_dict[trip] = w
        parts_dict = dict(sorted(parts_dict.items(), key=lambda item:item[1], reverse=True))
        trip_list = list(parts_dict.keys())
        if parts_dict[trip_list[0]] <= limit:
            return partition

        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    file_name = 'ps1_cow_data.txt'
    start = time.time()
    print(greedy_cow_transport(load_cows(file_name)))
    end = time.time()
    total_time = end-start
    print('Time taken for greedy:', total_time)
    
    print('\n')
    
    start = time.time()
    print(brute_force_cow_transport(load_cows(file_name)))
    end = time.time()
    total_time = end-start
    print('Time taken for brute force:', total_time)




compare_cow_transport_algorithms()



