'''
Created on Dec 10, 2017

@author: Jeff
'''
import errno
from constants import COMPLETE, EDGE, COMPLETE_BIPARTITE,\
    REDUCED_SPECTRAL_SIMILARITY, IRRECONCILABLE_SPECTRAL_DIFFERENCE,\
    TOTAL_SPECTRAL_SIMILARITY, SPECTRA, NORMALIZED_EIGENCENTRALITIES, STAR, NODE
from graph_wrappers import graph_wrapper_dict
from utils import get_data_dir, dump_one_d_data, dump_two_d_data, remove_file
from os.path import join


class experiment(object):
    #
    #
    def __init__(self, graph_family=None, perturbation_type=None, **kwargs):
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
        self.graph_family = graph_family
        self.perturbation_type = perturbation_type
        self.graph_generator = graph_wrapper_dict[graph_family]
        self.kwargs = kwargs
        self.graph_wrapper = self.graph_generator(**self.kwargs)
        self.data_dir = get_data_dir(self.graph_family, self.graph_wrapper.name, self.perturbation_type)
        #
        # Define files where data will be stored
        self.initialize_files()
        #
        return

    def initialize_files(self):
        #
        self.rss_file = join(self.data_dir, "rss.csv")
        self.isd_file = join(self.data_dir, "isd.csv")
        self.tss_file = join(self.data_dir, "tss.csv")
        self.bulk_indices_file = join(self.data_dir, "bulk_indices.csv")
        self.spectra_file_base = join(self.data_dir, "spectra_sample_")
        self.normalized_eigencentralities_file_base = join(self.data_dir, "normalized_eigencentralities_sample_")
        #
        # Remove since these file are opened with 'append' command
        remove_file(self.rss_file)
        remove_file(self.isd_file)
        remove_file(self.tss_file)
        remove_file(self.bulk_indices_file)
        #
        # NOTE: not necessary to remove spectra/centrality files, which
        # are opened with a 'write' command
        return

    def perform(self, num_samples=None):
        #
        # Perform the experiment num_samples times
        for i in range(num_samples):
            #
            # Apply the chosen perturbation until the graph becomes degenerate
            self.graph_wrapper = self.graph_generator(**self.kwargs)
            self.graph_wrapper.apply_perturbation_sequence(perturbation_type=self.perturbation_type)
            #
            # Record the data in the chosen files (appends)
            dump_one_d_data(self.rss_file, self.graph_wrapper.perturbed_spectra_info[REDUCED_SPECTRAL_SIMILARITY])
            dump_one_d_data(self.isd_file, self.graph_wrapper.perturbed_spectra_info[IRRECONCILABLE_SPECTRAL_DIFFERENCE])
            dump_one_d_data(self.tss_file, self.graph_wrapper.perturbed_spectra_info[TOTAL_SPECTRAL_SIMILARITY])
            #
            # (writes)
            dump_two_d_data(
                self.spectra_file_base + f'{i}.csv',
                self.graph_wrapper.perturbed_spectra_info[SPECTRA]
            )
            dump_two_d_data(
                self.normalized_eigencentralities_file_base + f'{i}.csv',
                self.graph_wrapper.perturbed_spectra_info[NORMALIZED_EIGENCENTRALITIES]
            )
        #
        return
#
