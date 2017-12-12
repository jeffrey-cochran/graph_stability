#
#
if __name__ == "__main__":
    #
    # Get utility libs
    import sys
    import os
    #
    # Add main folder to path dynamically
    x = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(x)
    #
    from experiment_def import experiment
    from constants import RANDOM_BINOMIAL, NODE, EDGE
    #
    # Ignore matplotlib and numpy warnings
    import warnings
    warnings.filterwarnings("ignore")
    #
    # Define paramts
    perturbation_types = [NODE, EDGE]
    nodes_list = [
        20, 50, 100
    ]
    prob_list = [
        0.05, 0.10, 0.25, 0.5, 0.75, 0.90, 0.95
    ]
    num_samples = 100
    #
    # Iterate over options
    for p in perturbation_types:
        for n in nodes_list:
            for q in prob_list:
                args_dict = {
                    "num_nodes": n,
                    "edge_prob": q,
                    "perturbation_type": p,
                    "graph_family": RANDOM_BINOMIAL
                }
                #
                # Define experiment
                print(f"Kicking off {num_samples} experiments of {p} perturbations on n={n} and p={q}")
                try:
                    exp = experiment(**args_dict)
                    exp.perform(num_samples)
                except:
                    print("...FAILED.")
        #
    #
