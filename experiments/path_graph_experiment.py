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
    from constants import PATH, NODE, EDGE
    #
    # Ignore matplotlib and numpy warnings
    import warnings
    warnings.filterwarnings("ignore")
    #
    # Define params
    perturbation_types = [NODE, EDGE]
    nodes_list = [
        5, 10, 20, 50, 100
    ]
    num_samples = 100
    #
    # Iterate over options
    for p in perturbation_types:
        for n in nodes_list:
            args_dict = {
                "num_nodes": n,
                "perturbation_type": p,
                "graph_family": PATH
            }
            #
            # Define experiment
            print(f"Kicking off {num_samples} experiments of {p} perturbations on n={n}")
            try:
                exp = experiment(**args_dict)
                exp.perform(num_samples)
            except:
                print("...FAILED.")
        #
    #
