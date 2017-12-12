from numpy.random import randint
from collections import namedtuple
from os.path import exists, join
from os import makedirs
from constants import data_dir
from os import remove
import csv
import errno

subplot_indices = namedtuple("subplot_indices", ["grid_size", "graph", "matrix", "spectrum"])

def write_rand_seeds(n, low=0, high=10000000, file_name="seeds.csv"):
    #
    rand_seeds = randint(size=n, low=low, high=high)
    with open(file_name, "w") as f:
        writer = csv.writer(f, delimiter='\n')
        writer.writerow(rand_seeds)
    #
    return


def read_rand_seeds(file_name):
    #
    with open(file_name, "r") as f:
        reader = csv.reader(f, delimiter='\n')
        rand_seeds = []
        for row in reader:
            rand_seeds += row
    #
    return [int(s) for s in rand_seeds]


def get_subplot_indices(include_graph=None,
                        include_matrix=None,
                        include_spectrum=None):
    #
    if include_graph and include_matrix and include_spectrum:
        grid_size = (2, 4)
        graph_index = ((0, 1), 2)
        matrix_index = ((1, 2), 2)
        spectrum_index = ((1, 0), 2)
    elif include_graph and include_matrix:
        grid_size = (2, 1)
        graph_index = ((0, 0), 1)
        matrix_index = ((1, 0), 1)
        spectrum_index = 0
    elif include_graph and include_spectrum:
        grid_size = (2, 1)
        graph_index = ((0, 0), 1)
        matrix_index = 0
        spectrum_index = ((1, 0), 1)
    elif include_matrix and include_spectrum:
        grid_size = (1, 2)
        graph_index = 0
        matrix_index = ((0, 1), 1)
        spectrum_index = ((0, 0), 1)
    elif include_graph:
        grid_size = (1, 1)
        graph_index = ((0, 0), 1)
        matrix_index = 0
        spectrum_index = 0
    elif include_matrix:
        grid_size = (1, 1)
        graph_index = 0
        matrix_index = ((0, 0), 1)
        spectrum_index = 0
    elif include_spectrum:
        grid_size = (1, 1)
        graph_index = 0
        matrix_index = 0
        spectrum_index = ((0, 0), 1)
    else:
        raise Exception("No content was specified for inclusion")
    #
    return subplot_indices(grid_size=grid_size, graph=graph_index, matrix=matrix_index, spectrum=spectrum_index)


def dump_one_d_data(file_name, data):
    #
    with open(file_name, 'a') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(data)
    #
    return


def dump_two_d_data(file_name, data):
    #
    # Assumes data is a list, but that
    # each item in the list may have a 
    # different number of columns
    with open(file_name, 'w') as f:
        writer = csv.writer(f, delimiter=",")
        for row in data:
            writer.writerow(row)
    #
    return


def get_data_dir(graph_family, graph_name, perturbation_type):
    #
    # Search for dir
    parent_dir = join(data_dir, graph_family)
    desired_parent_dir = join(parent_dir, perturbation_type)
    if not exists(desired_parent_dir):
        makedirs(desired_parent_dir)
    #
    desired_dir = join(desired_parent_dir, graph_name)
    if not exists(desired_dir):
        makedirs(desired_dir)
    #
    return desired_dir


def remove_file(file_name):
    #
    try:
        remove(file_name)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e
    #
    return
