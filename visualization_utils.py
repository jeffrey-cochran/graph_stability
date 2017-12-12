from graph_wrappers import graph_wrapper_dict, get_complete_bipartite_graph
from utils import get_data_dir
from os.path import join
from constants import EDGE, COMPLETE, STAR, NODE, CYCLE, PATH, WHEEL, HYPER_CUBE,\
    RANDOM_BINOMIAL, REDUCED_SPECTRAL_SIMILARITY, TOTAL_SPECTRAL_SIMILARITY,\
    metric_color_maps, IRRECONCILABLE_SPECTRAL_DIFFERENCE, COMPLETE_BIPARTITE,\
    misc_color_maps, TARGET
from numpy import mean, var, linspace, asarray, std
from collections import namedtuple
import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np

experimental_data = namedtuple("experimental_data", ["experiment_name", "expected_fractional_axis", "rss", "isd", "tss"])

def load_experiment(graph_family=None, perturbation_type=None, **kwargs):
        '''
        Different graph families take different optional kwargs:
            - complete <== num_nodes
            - complete_bipartite <== num_nodes_C1, num_nodes_C2
            - star <== num_leaves
            - path <== num_nodes
            - cycle <== num_nodes
            - hyper_cube <== cube_degree
            - random_binomial <== num_nodes, edge_prob
            - wheel <== num_spokes
        '''
        #
        # Set defining options
        graph_generator = graph_wrapper_dict[graph_family]
        graph_wrapper = graph_generator(**kwargs)
        experiment_name = graph_wrapper.name
        data_dir = get_data_dir(graph_family, graph_wrapper.name, perturbation_type)
        #
        # Define files where data will be stored
        rss_file = join(data_dir, "rss.csv")
        tss_file = join(data_dir, "tss.csv")
        isd_file = join(data_dir, "isd.csv")
        #
        # Get max columns
        rss_cols = list(range(get_max_number_columns(rss_file)))
        tss_cols = list(range(get_max_number_columns(tss_file)))
        isd_cols = list(range(get_max_number_columns(isd_file)))
        #
        # Retrieve data
        rss_data = pd.read_csv(rss_file, delimiter=',', header=None, names=rss_cols).fillna(value=0).as_matrix()
        tss_data = pd.read_csv(tss_file, delimiter=',', header=None, names=tss_cols).fillna(value=0).as_matrix()
        isd_data = pd.read_csv(isd_file, delimiter=',', header=None, names=isd_cols).fillna(value=1).as_matrix()
        #
        # Get normalized axis
        divisor = graph_wrapper.expected_nodes if perturbation_type == NODE else graph_wrapper.expected_edges
        expected_fractional_axis = asarray(list(range(rss_data.shape[1]))) / float(divisor)
        #
        # ["experiment_name", "expected_fractional_axis", "rss", "isd", "tss"]
        return experimental_data(
            experiment_name=experiment_name,
            expected_fractional_axis=expected_fractional_axis,
            rss=rss_data,
            isd=isd_data,
            tss=tss_data
        )

def get_max_number_columns(file_name):
    #
    max_cols = 0
    with open(file_name, "r") as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if len(row) > max_cols:
                max_cols = len(row)
            #
        #
    #
    return max_cols

def compare_experiments(graph_families=None, perturbation_type=None, measure=None, keyword_args=None, ax=None):
    #
    if ax is None:
        ax = plt.gca()
    #
    # ["experiment_name", "expected_fractional_axis", "rss", "isd", "tss"]
    num_graphs = len(graph_families)
    #
    # Set color scheme for graph
    cm = metric_color_maps[measure] 
    cNorm  = colors.Normalize(vmin=-1, vmax=num_graphs)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    #
    for i in range(num_graphs):
        colorVal = scalarMap.to_rgba(i)
        kw = keyword_args[i]
        exp_data = load_experiment(graph_family=graph_families[i], perturbation_type=perturbation_type, **kw)
        exp_name = getattr(exp_data, "experiment_name")
        x = getattr(exp_data, "expected_fractional_axis")
        y = mean(getattr(exp_data, measure), axis=0)
        ax.plot(x, y, color=colorVal, label=exp_name)
    #
    # Set conditional titles
    perturbed_obj = 'nodes' if perturbation_type == NODE else 'edges'
    x_label = f'Fraction of Perturbed {perturbed_obj}'
    y_label = f'E[{measure.upper()}]'
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(f'{measure.upper()} vs. {x_label}')
    ax.legend()
    return


def compare_all_metrics(graph_families=None, perturbation_type=None, keyword_args=None):
    f, (ax1, ax2, ax3) = plt.subplots(1, 3)
    compare_experiments(
        graph_families=graph_families,
        perturbation_type=perturbation_type,
        measure=IRRECONCILABLE_SPECTRAL_DIFFERENCE,
        keyword_args=keyword_args,
        ax=ax1
    )
    compare_experiments(
        graph_families=graph_families,
        perturbation_type=perturbation_type,
        measure=REDUCED_SPECTRAL_SIMILARITY,
        keyword_args=keyword_args,
        ax=ax2
    )
    compare_experiments(
        graph_families=graph_families,
        perturbation_type=perturbation_type,
        measure=TOTAL_SPECTRAL_SIMILARITY,
        keyword_args=keyword_args,
        ax=ax3
    )
    return


def display_centrality(graph_family=None, keyword_args=None, ax=None):
    #
    if ax is None:
        ax = plt.gca()
    #
    # Get graph wrapper
    graph_generator = graph_wrapper_dict[graph_family]
    graph_wrapper = graph_generator(**keyword_args)
    eigencentrality = graph_wrapper.get_normalized_eigencentrality()
    #
    # Generate indices
    eigencentrality_indices = list(range(1, len(eigencentrality) + 1))
    #
    # Make stem plots
    (markerline, stemlines, baseline) = ax.stem(eigencentrality_indices, eigencentrality, 'm', markerfmt='mo')
    plt.setp(baseline, visible=False)
    step_size = max([1, int(len(eigencentrality_indices) / float(20))])
    ax.set_xlabel("Node Number")
    ax.set_ylabel("Normalized Eigencentrality")
    plt.xticks(eigencentrality_indices[::step_size], rotation=45)
    kl_divergence = graph_wrapper.get_KL_divergence_from_uniformity(graph_choice=TARGET)
    ax.set_title(f"Distribution of Normalized Eigencentralities in {graph_wrapper.name},\nUniform KL-Divergence = {kl_divergence:1.2e}")
    #
    return


def display_uncertainty(graph_family=None, perturbation_type=None, measure=None, keyword_args=None, ax=None, deviations=2):
    #
    if ax is None:
        ax = plt.gca()
    #
    # Set color scheme for graph
    cm = metric_color_maps[measure]
    cNorm = colors.Normalize(vmin=-1, vmax=3)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    #
    # Plot the mean
    kw = keyword_args
    exp_data = load_experiment(graph_family=graph_family, perturbation_type=perturbation_type, **kw)
    exp_name = getattr(exp_data, "experiment_name")
    x = getattr(exp_data, "expected_fractional_axis")
    y = mean(getattr(exp_data, measure), axis=0)
    colorVal = scalarMap.to_rgba(1)
    ax.plot(x, y, color=colorVal, label=exp_name)
    #
    # Plot the upper bound
    y_plus = y + deviations * std(getattr(exp_data, measure), axis=0)
    colorValPlus = scalarMap.to_rgba(2)
    ax.plot(x, y_plus, color=colorValPlus, label=f'{exp_name} (+{deviations} std.)', linestyle='--')
    #
    # Plot the lower bound
    y_minus = y - deviations * std(getattr(exp_data, measure), axis=0)
    colorValMinus = scalarMap.to_rgba(0)
    ax.plot(x, y_minus, color=colorValMinus, label=f'{exp_name} (-{deviations} std.)', linestyle='--')
    #
    # Set conditional titles
    perturbed_obj = 'Nodes' if perturbation_type == NODE else 'Edges'
    x_label = f'Fraction of Perturbed {perturbed_obj}'
    y_label = f'E[{measure.upper()}]'
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(f'{measure.upper()} vs. {x_label}')
    ax.legend()
    return


def display_all_uncertainty(graph_family=None, perturbation_type=None, keyword_args=None, deviations=2):
    #
    f, (ax1, ax2, ax3) = plt.subplots(1, 3)
    display_uncertainty(graph_family=graph_family, perturbation_type=perturbation_type, measure=IRRECONCILABLE_SPECTRAL_DIFFERENCE, keyword_args=keyword_args, ax=ax1, deviations=deviations)
    display_uncertainty(graph_family=graph_family, perturbation_type=perturbation_type, measure=REDUCED_SPECTRAL_SIMILARITY, keyword_args=keyword_args, ax=ax2, deviations=deviations)
    display_uncertainty(graph_family=graph_family, perturbation_type=perturbation_type, measure=TOTAL_SPECTRAL_SIMILARITY, keyword_args=keyword_args, ax=ax3, deviations=deviations)
    #
    return


def visualize_kl_divergence(graph_family=None, perturbation_type=None, measure=None, keyword_args=None, deviations=2):
    #
    f, (ax1, ax2) = plt.subplots(1, 2)
    display_centrality(graph_family=graph_family, keyword_args=keyword_args, ax=ax1)
    display_uncertainty(graph_family=graph_family, perturbation_type=perturbation_type, measure=measure, keyword_args=keyword_args, ax=ax2, deviations=deviations)
    #
    return


def compare_to_uncertainty(
        graph_family_certain=None,
        graph_family_uncertain=None,
        perturbation_type=None,
        measure=None,
        keyword_args_certain=None,
        keyword_args_uncertain=None,
        ax=None,
        deviations=2):
    #
    if ax is None:
        ax = plt.gca()
    #
    # Plot the mean of the certain sequence
    exp_data = load_experiment(graph_family=graph_family_certain, perturbation_type=perturbation_type, **keyword_args_certain)
    exp_name = getattr(exp_data, "experiment_name")
    x = getattr(exp_data, "expected_fractional_axis")
    y = mean(getattr(exp_data, measure), axis=0)
    ax.plot(x, y, 'k-.', label=exp_name)
    #
    # Plot uncertain graph
    display_uncertainty(graph_family=graph_family_uncertain, perturbation_type=perturbation_type, measure=measure, keyword_args=keyword_args_uncertain, ax=ax, deviations=deviations)
    #
    return

# display_all_uncertainty(graph_family=COMPLETE, perturbation_type=NODE, keyword_args={"num_nodes": 5})
# 
# g1 = get_complete_bipartite_graph(num_nodes_C1=5, num_nodes_C2=100)
# g2 = get_complete_bipartite_graph(num_nodes_C1=10, num_nodes_C2=100)
# g3 = get_complete_bipartite_graph(num_nodes_C1=20, num_nodes_C2=100)
# g4 = get_complete_bipartite_graph(num_nodes_C1=50, num_nodes_C2=100)
# g5 = get_complete_bipartite_graph(num_nodes_C1=100, num_nodes_C2=100)
# 
# print(g1.get_KL_divergence_from_uniformity() / g2.get_KL_divergence_from_uniformity())
# print(g1.get_KL_divergence_from_uniformity() / g3.get_KL_divergence_from_uniformity())
# print(g1.get_KL_divergence_from_uniformity() / g4.get_KL_divergence_from_uniformity())
# print(g1.get_KL_divergence_from_uniformity() / g5.get_KL_divergence_from_uniformity())

# compare_to_uncertainty(
#         graph_family_certain=COMPLETE,
#         graph_family_uncertain=STAR,
#         perturbation_type=NODE,
#         measure=TOTAL_SPECTRAL_SIMILARITY,
#         keyword_args_certain={"num_nodes": 100},
#         keyword_args_uncertain={"num_leaves": 100},
#         ax=None,
#         deviations=3
#     )
# display_uncertainty(graph_family=STAR, perturbation_type=NODE, measure=TOTAL_SPECTRAL_SIMILARITY, keyword_args={"num_leaves": 100}, ax=None, deviations=3)

# compare_all_metrics(
#     graph_families=[
#         COMPLETE,
#     ],
#     perturbation_type=NODE,
#     keyword_args=[
#         {"num_nodes": 5},
#     ]
# )
# visualize_kl_divergence(graph_family=COMPLETE, perturbation_type=NODE, measure=TOTAL_SPECTRAL_SIMILARITY, keyword_args={"num_nodes": 5}, deviations=2)
plt.show()
# n = 100
# 
# dd = load_experiment(graph_family=COMPLETE, perturbation_type=NODE, num_nodes=n)
# d = load_experiment(graph_family=COMPLETE, perturbation_type=NODE, num_nodes=10)
# 
# xd = 1.0 / d.shape[1] * linspace(0, d.shape[1] - 1, d.shape[1])
# xdd = 1.0 / dd.shape[1] * linspace(0, dd.shape[1] - 1, dd.shape[1])
# yd = mean(d, axis=0)
# ydd = mean(dd, axis=0)
# sd = var(d, axis=0)
# yyd = yd + 3.0 * sd
# yyyd = yd - 3.0 * sd
# matplotlib.pyplot.plot(xd, yd, xdd, ydd)
# matplotlib.pyplot.show()

