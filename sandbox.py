from graph_wrapper_def import graph_wrapper
from constants import COMPLETE, NODE, PERTURBED, RANDOM_BINOMIAL, HYPER_CUBE,\
    SPRING, COMPLETE_BIPARTITE, FRUCHTERMAN, KAWADA, CYCLE, WHEEL, STAR


g = graph_wrapper(graph_family=WHEEL, args=[5])
g.visualize()