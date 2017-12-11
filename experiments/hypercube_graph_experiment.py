'''
Created on Dec 11, 2017

@author: Jeff
'''
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
    from constants import HYPER_CUBE, NODE, EDGE
    #
    # Ignore matplotlib and numpy warnings
    import warnings
    warnings.filterwarnings("ignore")
    #
    # Define paramts
    perturbation_types = [NODE, EDGE]
    cube_degree_list = [
        2, 3, 4, 5, 6, 7
    ]
    num_samples = 100
    #
    # Iterate over options
    for p in perturbation_types:
        for c in cube_degree_list:
            args_dict = {
                "cube_degree": c,
                "perturbation_type": p,
                "graph_family": HYPER_CUBE
            }
            #
            # Define experiment
            print(f"Kicking off {num_samples} experiments of {p} perturbations on n={c}")
            try:
                exp = experiment(**args_dict)
                exp.perform(num_samples)
            except:
                print("...FAILED.")
        #
    #
