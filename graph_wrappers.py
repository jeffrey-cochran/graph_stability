from graph_wrapper_def import graph_wrapper
from constants import COMPLETE, COMPLETE_BIPARTITE, WHEEL, RANDOM_BINOMIAL,\
    HYPER_CUBE, CYCLE, PATH, STAR


def get_complete_graph(num_nodes=None):
    #
    name = "K_{0}".format(num_nodes)
    #
    return graph_wrapper(
        graph_family=COMPLETE,
        args=[num_nodes],
        name=name,
    )


def get_complete_bipartite_graph(num_nodes_C1=None, num_nodes_C2=None):
    #
    name = f'K_{num_nodes_C1}_{num_nodes_C2}'
    #
    return graph_wrapper(
        graph_family=COMPLETE_BIPARTITE,
        args=[num_nodes_C1, num_nodes_C2],
        name=name,
    )


def get_star_graph(num_leaves=None):
    #
    name = f'S_{num_leaves}'
    #
    return graph_wrapper(
        graph_family=STAR,
        args=[num_leaves],
        name=name,
    )


def get_path_graph(num_nodes=None):
    #
    name = f'P_{num_nodes}'
    #
    return graph_wrapper(
        graph_family=PATH,
        args=[num_nodes],
        name=name,
    )


def get_cycle_graph(num_nodes=None):
    #
    name = f'C_{num_nodes}'
    #
    return graph_wrapper(
        graph_family=CYCLE,
        args=[num_nodes],
        name=name,
    )


def get_hyper_cube_graph(cube_degree=None):
    #
    name = f'Q_{cube_degree}'
    #
    return graph_wrapper(
        graph_family=HYPER_CUBE,
        args=[cube_degree],
        name=name,
    )


def get_random_binomial_graph(num_nodes=None, edge_prob=None):
    #
    name = f'B_{num_nodes}_{edge_prob}'
    #
    return graph_wrapper(
        graph_family=RANDOM_BINOMIAL,
        args=[num_nodes, edge_prob],
        name=name,
    )


def get_wheel_graph(num_spokes=None):
    #
    name = f'W_{num_spokes}'
    #
    return graph_wrapper(
        graph_family=WHEEL,
        args=[num_spokes],
        name=name,
    )


#
# Construct graph wrapper dictionary
# for easy graph generation
graph_wrapper_dict = {
    "complete": get_complete_graph,
    "complete_bipartite": get_complete_bipartite_graph,
    "star": get_star_graph,
    "path": get_path_graph,
    "cycle": get_cycle_graph,
    "hyper_cube": get_hyper_cube_graph,
    "random_binomial": get_random_binomial_graph,
    "wheel": get_wheel_graph
}
