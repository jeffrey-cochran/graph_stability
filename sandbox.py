from graph_wrapper_def import graph_wrapper
from constants import COMPLETE, NODE, PERTURBED


g = graph_wrapper(graph_family=COMPLETE, args=[10])
g.visualize(include_matrix=True, include_spectrum=True, include_labels=True)
g.apply_perturbation(perturbation_type=NODE)
g.visualize(graph_choice=PERTURBED, include_matrix=True, include_spectrum=True, include_labels=True)