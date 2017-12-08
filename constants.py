import networkx as nx

graph_dict = {
    "complete": nx.complete_graph,
    "complete_bipartite": nx.complete_bipartite_graph,
    "star": nx.star_graph,
    "path": nx.path_graph,
    "cycle": nx.cycle_graph,
    "hyper_cube": nx.hypercube_graph
}