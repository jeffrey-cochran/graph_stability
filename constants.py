import networkx as nx
from os.path import dirname, join, abspath
from matplotlib import pyplot as plt

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
    "random_binomial": nx.gnp_random_graph,
    "wheel": nx.wheel_graph
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
# Graph specifications
COMPLETE = "complete"
COMPLETE_BIPARTITE = "complete_bipartite"
STAR = "star"
PATH = "path"
CYCLE = "cycle"
HYPER_CUBE = "hyper_cube"
RANDOM_BINOMIAL = "random_binomial"
WHEEL = "wheel"
#
# Create relative absolute path
# to data dir for easy read/write
root_dir = dirname(abspath(__file__))
data_dir = join(root_dir, "data")
#
# Perturbed Data Keys
BULK_INDICES = "bulk_indices"
NORMALIZED_EIGENCENTRALITIES = "normalized_eigencentralities"
SPECTRA = "spectra"
REDUCED_SPECTRAL_SIMILARITY = "rss"
IRRECONCILABLE_SPECTRAL_DIFFERENCE = "isd"
TOTAL_SPECTRAL_SIMILARITY = "tss"
#
# Color maps for different metrics
metric_color_maps = {
    REDUCED_SPECTRAL_SIMILARITY: plt.get_cmap('PuBu'),
    IRRECONCILABLE_SPECTRAL_DIFFERENCE: plt.get_cmap('YlGn'),
    TOTAL_SPECTRAL_SIMILARITY: plt.get_cmap('YlOrRd')    
}
