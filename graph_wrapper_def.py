import networkx as nx
import matplotlib.pyplot as plt
from numpy.random import choice
from numpy.linalg import norm
from numpy import asarray, sum, log2, ones
from numpy import float64 as npfloat64
from constants import graph_dict, layout_dict, LAPLACIAN, ADJACENCY, NODE, EDGE,\
    TARGET, PERTURBED, SPRING, KAWADA, FRUCHTERMAN, BULK_INDICES,\
    NORMALIZED_EIGENCENTRALITIES, SPECTRA, REDUCED_SPECTRAL_SIMILARITY,\
    IRRECONCILABLE_SPECTRAL_DIFFERENCE, TOTAL_SPECTRAL_SIMILARITY
from utils import get_subplot_indices
from scipy.stats import moment


class graph_wrapper(object):

    def __init__(self,
                 graph_family=None,
                 args=[],
                 kwargs={},
                 layout=KAWADA,
                 name="G",
                 ):
        #
        # Create graph data structure
        self.graph = graph_dict[graph_family](*args, **kwargs)
        self.name = name
        #
        # Relabel to guarantee integer labels
        mapping = dict(zip(self.graph.nodes(), list(range(len(self.graph.nodes())))))
        self.graph = nx.relabel_nodes(self.graph, mapping)
        #
        # Set default layout
        self.set_layout(layout)
        #
        # Establish visualization bounds for Laplacian matrix
        self.degree_sequence = sorted([d for n, d in self.graph.degree()], reverse=True)
        self.max_cmap_val = self.degree_sequence[0]
        self.min_cmap_val = -1
        #
        # Init spectra
        self.target_spectrum = self.get_spectrum(graph_choice=TARGET, matrix=LAPLACIAN)
        self.target_bulk_index = self.get_bulk_index(self.target_spectrum)
        self.target_eigencentrality = self.get_normalized_eigencentrality(graph_choice=TARGET)
        self.target_spectrum_norm = norm(self.target_spectrum)
        #
        # Init perturbed graph
        self.init_perturbed_graph()
        #
        return

    def apply_perturbation(self, perturbation_type=NODE):
        #
        # Don't perturb degenerate graphs
        if self.is_degenerate(self.perturbed_graph):
            print("Cannot perturb a degenerate graph. Aborting!")
            return
        #
        # Make sure valid choice
        if perturbation_type not in [NODE, EDGE]:
            raise Exception("Invalid perturbation type, %s, specified. Must be either %s or %s." % (perturbation_type, LAPLACIAN, ADJACENCY))
        #
        if perturbation_type == NODE:
            #
            # Randomly select a node
            node_choice = choice(self.perturbed_graph.nodes())
            #
            # Record neighbors
            node_neighbors = nx.neighbors(self.perturbed_graph, node_choice)
            #
            # Remove selected node
            self.perturbed_graph.remove_node(node_choice)
            #
            # Remove isolated nodes
            for n in node_neighbors:
                if nx.degree(self.perturbed_graph, n) == 0:
                    self.perturbed_graph.remove_node(n)
            #
        elif perturbation_type == EDGE:
            #
            # Randomly select an edge
            edge_index_choice = choice(len(self.perturbed_edge_list))
            edge_choice = self.perturbed_edge_list.pop(edge_index_choice)
            #
            # Remove selected edge
            self.perturbed_graph.remove_edge(*edge_choice)
            #
            # Remove isolated nodes
            for edge_node in edge_choice:
                #
                if self.perturbed_graph.degree(edge_node) == 0:
                    self.perturbed_graph.remove_node(edge_node)
                #
            #
        #
        return

    def apply_perturbation_sequence(self, perturbation_type=NODE):
        #
        # Reinitialize the perturbed graph
        self.init_perturbed_graph()
        #
        # Iterate
        while not self.perturbed_graph_is_degenerate:
            self.apply_perturbation(perturbation_type)
            self.assess_similarity()
        #
        return

    def assess_similarity(self):
        #
        # Make sure perturbed graph is not degenerate
        self.perturbed_graph_is_degenerate = self.is_degenerate(self.perturbed_graph)
        if self.perturbed_graph_is_degenerate:
            perturbed_spectrum = [0]
            perturbed_bulk_index = [0]
            perturbed_normalized_eigencentrality = [0]
            rss = 0
            isd = 1.0
            tss = 0
        else:
            #
            # Determine the minimal index containing 90% of eigenvalue sum
            perturbed_spectrum = self.get_spectrum(graph_choice=PERTURBED, matrix=LAPLACIAN)
            perturbed_bulk_index = self.get_bulk_index(perturbed_spectrum)
            #
            # Calculate eigencentrality
            perturbed_normalized_eigencentrality = self.get_normalized_eigencentrality(graph_choice=PERTURBED)
            #
            # Calculate Irreconcilable Spectral Dissimilarity
            rss = self.get_rss(perturbed_spectrum, self.target_spectrum, perturbed_bulk_index)
            #
            # Calculate Reduced Spectral Similarity
            isd = self.get_isd(perturbed_spectrum, self.target_spectrum, bulk_index=perturbed_bulk_index)
            #
            # Calculate Total Spectral Similarity
            tss = (1.0 - isd) * rss
        #
        # Update data
        self.update_perturbed_spectra_info(
            perturbed_spectrum=perturbed_spectrum,
            perturbed_normalized_eigencentrality=perturbed_normalized_eigencentrality,
            perturbed_bulk_index=perturbed_bulk_index,
            rss=rss,
            isd=isd,
            tss=tss
        )
        #
        return

    def calc_normalized_entropy(self, normalized_eigencentrality):
        #
        n = normalized_eigencentrality.shape[0]
        entropy = -sum(normalized_eigencentrality * log2(normalized_eigencentrality))
        #
        return entropy / log2(n)

    def calc_KL_divergence_from_uniformity(self, normalized_eigencentrality):
        #
        n = normalized_eigencentrality.shape[0]
        uni = ones(n) / n
        kl_div = -sum(normalized_eigencentrality * log2((uni / normalized_eigencentrality)))
        #
        return kl_div

    def get_bulk_index(self, spectrum):
        spectral_sum = sum(spectrum)
        cut_off = 0.95 * spectral_sum
        running_sum = 0
        #
        for i in range(spectrum.shape[0]):
            running_sum += spectrum[i]
            if running_sum > cut_off:
                return i
            #
        #
        return spectrum.shape[0]

    def get_isd(self, perturbed_spectrum, target_spectrum, bulk_index=-1):
        #
        # Irreconcilable Spectral Dissimilarity
        # num_perturbed_eigenvalues = perturbed_spectrum.shape[0]
        remaining_data = self.target_spectrum[:bulk_index]
        #
        return 1 - (norm(remaining_data) / self.target_spectrum_norm)

    def get_matrix(self, graph_choice=TARGET, matrix=LAPLACIAN):
        #
        graph = self.return_valid_graph_choice(graph_choice)
        #
        if matrix == LAPLACIAN:
            out_matrix = nx.laplacian_matrix(graph)
        else:
            out_matrix = nx.adjacency_matrix(graph)
        #
        return out_matrix.toarray()

    def get_normalized_eigencentrality(self, graph_choice=TARGET):
        #
        G = self.return_valid_graph_choice(graph_choice)
        #
        if G.number_of_edges() < 2:
            centralities = [0.5, 0.5]
        else:
            centralities = nx.eigenvector_centrality_numpy(G).values()
        #
        e = asarray(list(centralities))
        #
        return e / sum(e)

    def get_normalized_entropy(self, graph_choice=TARGET):
        #
        normalized_eigencentrality = self.get_normalized_eigencentrality(graph_choice=graph_choice)
        normalized_entropy = self.calc_normalized_entropy(normalized_eigencentrality)
        #
        return normalized_entropy

    def get_rss(self, perturbed_spectrum, target_spectrum, bulk_index):
        #
        # Reduced Spectral Similarity
        reduced_perturbed_eigenvalues = perturbed_spectrum[:bulk_index]
        reduced_target_eigenvalues = target_spectrum[:bulk_index]
        discrepancy = reduced_perturbed_eigenvalues - reduced_target_eigenvalues
        norm_reduced_target_eigenvalues = norm(reduced_target_eigenvalues)
        #
        # Avoid div by zero
        if norm_reduced_target_eigenvalues > 0.0:
            rss = 1.0 - norm(discrepancy) / norm_reduced_target_eigenvalues
        else:
            rss = 0
        #
        return rss

    def get_spectrum(self, graph_choice=TARGET, matrix=LAPLACIAN):
        #
        graph = self.return_valid_graph_choice(graph_choice)
        #
        if matrix == LAPLACIAN:
            spectrum = nx.laplacian_spectrum(graph)
        else:
            spectrum = nx.adjacency_spectrum(graph)
        #
        return asarray(sorted(spectrum, reverse=True))

#     def get_third_moment

    def init_perturbed_graph(self):
        #
        self.perturbed_graph = self.graph.copy()
        self.perturbed_graph_is_degenerate = False
        self.perturbed_edge_list = list(self.perturbed_graph.edges())
        rss = self.get_rss(self.target_spectrum, self.target_spectrum, self.target_bulk_index)
        isd = self.get_isd(self.target_spectrum, self.target_spectrum)
        tss = (1 - isd) * rss
        self.perturbed_spectra_info = {
            SPECTRA: [
                self.target_spectrum,
            ],
            NORMALIZED_EIGENCENTRALITIES: [
                self.target_eigencentrality
            ],
            BULK_INDICES: [
                self.target_bulk_index,
            ],
            REDUCED_SPECTRAL_SIMILARITY: [
                rss
            ],
            IRRECONCILABLE_SPECTRAL_DIFFERENCE: [
                isd
            ],
            TOTAL_SPECTRAL_SIMILARITY: [
                tss
            ],
        }
        #
        return

    def is_degenerate(self, graph):
        return len(list(graph.nodes())) < 2

    def return_valid_graph_choice(self, graph_choice):
        #
        # Make sure valid choice
        if graph_choice not in [TARGET, PERTURBED]:
            raise Exception("Invalid graph choice, %s, specified. Must be either %s or %s." % (graph_choice, TARGET, PERTURBED))
        #
        return self.graph if graph_choice == TARGET else self.perturbed_graph

    def set_layout(self, layout):
        #
        self.pos = layout_dict[layout](self.graph)
        #
        return

    def update_perturbed_spectra_info(
            self,
            perturbed_spectrum=None,
            perturbed_normalized_eigencentrality=None,
            perturbed_bulk_index=None,
            rss=None,
            isd=None,
            tss=None):
        #
        self.perturbed_spectra_info[SPECTRA].append(perturbed_spectrum)
        self.perturbed_spectra_info[NORMALIZED_EIGENCENTRALITIES].append(perturbed_normalized_eigencentrality)
        self.perturbed_spectra_info[BULK_INDICES].append(perturbed_bulk_index)
        self.perturbed_spectra_info[REDUCED_SPECTRAL_SIMILARITY].append(rss)
        self.perturbed_spectra_info[IRRECONCILABLE_SPECTRAL_DIFFERENCE].append(isd)
        self.perturbed_spectra_info[TOTAL_SPECTRAL_SIMILARITY].append(tss)
        #
        return

    def visualize(self,
                  edge_color='c',
                  node_color='c',
                  edge_width=3,
                  node_size=500,
                  edge_alpha=0.5,
                  node_alpha=0.8,
                  spectrum_color='y',
                  outline_reduction=3.0,
                  graph_choice=TARGET,
                  include_labels=False,
                  include_outline=True,
                  include_matrix=False,
                  include_spectrum=False,
                  include_graph=True,
                  ):
        #
        # Include perturbed in the titles?
        graph_title_prefix = "Perturbed " if graph_choice == PERTURBED else ""
        #
        # Select graph
        graph_to_visualize = self.return_valid_graph_choice(graph_choice)
        #
        # Cannot visualize a degenrate graph
        if self.is_degenerate(graph_to_visualize):
            print("Cannot visualize a degenerate graph. Aborting!")
            return
        #
        # Determine subplot arrangement
        indices = get_subplot_indices(include_graph=include_graph, include_matrix=include_matrix, include_spectrum=include_spectrum)
        #
        # Plot graph
        if include_graph:
            plt.subplot2grid(indices.grid_size, indices.graph[0], colspan=indices.graph[1])
            #
            # Displays transparent black beneath
            if include_outline:
                nx.draw_networkx_edges(graph_to_visualize, pos=self.pos, width=(edge_width / outline_reduction), alpha=edge_alpha, edge_color='k')
                nx.draw_networkx_nodes(graph_to_visualize, pos=self.pos, node_color='k', node_size=(node_size / outline_reduction), alpha=node_alpha)
            #
            # Display labels
            if include_labels:
                nx.draw_networkx_labels(graph_to_visualize, pos=self.pos)
            #
            # Overlay transparent, colored layer
            nx.draw_networkx_edges(graph_to_visualize, pos=self.pos, width=edge_width, alpha=edge_alpha, edge_color=edge_color)
            nx.draw_networkx_nodes(graph_to_visualize, pos=self.pos, node_color=edge_color, node_size=node_size, alpha=node_alpha)
            plt.axis('off')
            plt.title("%s%s" % (graph_title_prefix, self.name))
        #
        # Plot matrix
        if include_matrix:
            plt.subplot2grid(indices.grid_size, indices.matrix[0], colspan=indices.matrix[1])
            #
            # Get matrix
            matrix = self.get_matrix(graph_choice=graph_choice)
            plt.axis('off')
            plt.imshow(matrix, interpolation='nearest', cmap=plt.get_cmap('BuPu'), aspect='auto')
            plt.clim(vmin=self.min_cmap_val, vmax=self.max_cmap_val)
            plt.colorbar()
            plt.title("Laplacian of %s%s" % (graph_title_prefix, self.name))
        #
        # Plot spectrum
        if include_spectrum:
            plt.subplot2grid(indices.grid_size, indices.spectrum[0], colspan=indices.spectrum[1])
            #
            # Get spectrum
            spectrum = self.get_spectrum(graph_choice=graph_choice)
            #
            # Generate indices
            spectrum_indices = list(range(1, len(spectrum) + 1))
            #
            # Make stem plots
            (markerline, stemlines, baseline) = plt.stem(spectrum_indices, spectrum, spectrum_color, markerfmt=spectrum_color + 'o')
            plt.setp(baseline, visible=False)
            plt.xticks(spectrum_indices, rotation=45)
            plt.title("Spectrum of Eigenvalues for %s%s" % (graph_title_prefix, self.name))
        #
        plt.show()
        #
        return
#
