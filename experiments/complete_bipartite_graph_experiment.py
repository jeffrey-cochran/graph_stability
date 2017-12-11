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
    from constants import COMPLETE_BIPARTITE, NODE, EDGE
    #
    # Ignore matplotlib and numpy warnings
    import warnings
    warnings.filterwarnings("ignore")
    #
    # Define paramts
    perturbation_types = [NODE, EDGE]
    node_list = [
        (5, 5), (5, 10), (5, 20), (5, 50), (5, 100),
        (10, 10), (10, 20), (10, 50), (10, 100),
        (20, 20), (20, 50), (20, 100),
        (50, 50), (50, 100),
        (100, 100),
    ]
    num_samples = 100
    #
    # Iterate over options
    for p in perturbation_types:
        for n in node_list:
            args_dict = {
                "num_nodes_C1": n[0],
                "num_nodes_C2": n[1],
                "perturbation_type": p,
                "graph_family": COMPLETE_BIPARTITE
            }
            #
            # Define experiment
            print(f"Kicking off {num_samples} experiments of {p} perturbations on n={n[0]} and m={n[1]}...")
            try:
                exp = experiment(**args_dict)
                exp.perform(num_samples)
            except:
                print("...FAILED.")
        #
    #
