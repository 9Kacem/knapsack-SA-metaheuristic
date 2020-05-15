#coding: utf-8
import argparse
from functools import partial
from time import time

from sa import annealing_algorithm

def parse_data(inst_file):
    """Data files line parsing method
    :param line: line from input file
    :return: list of tuples like: [(weight of item 0, cost of item 0), (weight1, cost1), ...])
    """
    # Skip comment lines
    inst_file.readline()
    inst_file.readline()
    inst_file.readline()

    # Get number items (count)
    # parts = [int(value) for value in line.split()]
    number = int(inst_file.readline().split()[1])
    
    # Get sack capacity
    inst_file.readline()
    capacity = int(inst_file.readline().split()[1])

    # Skip blank spaces
    inst_file.readline()
    inst_file.readline()
    
    # Get weights and costs
    weight_cost = []
    for line in inst_file:
        if line[0] < 'a':
            parts = [int(value) for value in line.split()]
            weight_cost.append((parts[0], parts[1]))

    return number, capacity, weight_cost


def solver(method, inst_file_path, solution_file_path):
    """
    :param inst_file_path: path to file with input instances
    :param solution_file_path: path to file where solver should write output data
    """
    inst_file = open(inst_file_path, "r")
    sol_file = open(solution_file_path, "w")
    

    number, capacity, weight_cost = parse_data(inst_file)
 
    # get best cost and variables combination
    best_cost, best_combination = method(number, capacity, weight_cost)

    # write best combinaison to file    
    # sol_file.write("%s  %s\n" % (best_cost, best_combination))

    print ("Our best cost: %s" % best_cost)
    inst_file.close()
    sol_file.close()

if __name__ == "__main__":
    #Get program arugments
    parser = argparse.ArgumentParser(description='Script solving the 0/1 knapsack problem')
    parser.add_argument('-f', '--inst-file', type=str, dest="inst_file_path", default="datasets/Facile/Petite/FacilePetite.txt", 
                        help='Path to inst *.dat file')
    parser.add_argument('-o', type=str, dest="solution_file_path", default="output",
                        help='Path to file where solutions will be saved. Default value: output.sol.dat')
    parser.add_argument('-t', type=int, dest="temperature", default=100,
                        help='Initial temperature for annealing approach. Default value: 100')
    parser.add_argument('-n', type=int, dest="steps", default=100,
                        help='Number of steps for annealing approach iteration. Default value: 100')
    parser.add_argument('-r', type=int, dest="repeat", default=1,
                        help='Number of repetitions. Default value: 1')
    args = parser.parse_args()

    if args.temperature < 1:
        raise Exception("Initial temperature for annealing approach must be greater than 0")
    if args.steps < 1:
        raise Exception("Number of steps for annealing approach iteration must be greater than 0")
    method = partial(annealing_algorithm, init_temp=args.temperature, steps=args.steps)

    solving_time = 0
    
    # repeating "repeat" time to get average solving time
    for i in range(args.repeat):
        t_start = time()
        solver(method, args.inst_file_path, args.solution_file_path)
        t_finish = time()
        solving_time += (t_finish - t_start)

    print ("Average solving time: %s sec." % (solving_time / args.repeat))