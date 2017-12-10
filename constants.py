import networkx as nx
from os.path import dirname, join, abspath

#
# Construct graph family dict
# for easy graph generation
graph_dict = {
    "complete": nx.complete_graph,
    "complete_bipartite": nx.complete_bipartite_graph,
    "star": nx.star_graph,
    "path": nx.path_graph,
    "cycle": nx.cycle_graph,
    "hyper_cube": nx.hypercube_graph,
    "random_binomial": nx.gnp_random_graph
}
#
# Construct layout dict
# for easy changese to layout
layout_dict = {
    "kawada": nx.kamada_kawai_layout,
    "fruchterman": nx.fruchterman_reingold_layout,
    "spring": nx.spring_layout
}
#
# Matrix specifications
LAPLACIAN = "laplacian"
ADJACENCY = "adjacency"
#
# Perturbations specifications
NODE = "node"
EDGE = "edge"
#
# Graph specifications
TARGET = "target"
PERTURBED = "perturbed"
#
# Layout specifications
SPRING = "spring"
KAWADA = "kawada"
FRUCHTERMAN = "fruchterman"
#
# Create relative absolute path
# to data dir for easy read/write
root_dir = dirname(abspath(__file__))
data_dir = join(root_dir, "data")