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
    from constants import WHEEL, NODE, EDGE
    #
    # Ignore matplotlib and numpy warnings
    import warnings
    warnings.filterwarnings("ignore")
    #
    # Define paramts
    perturbation_types = [NODE, EDGE]
    spokes_list = [
        5, 10, 20, 50, 100
    ]
    num_samples = 100
    #
    # Iterate over options
    for p in perturbation_types:
        for s in spokes_list:
            args_dict = {
                "num_spokes": s,
                "perturbation_type": p,
                "graph_family": WHEEL
            }
            #
            # Define experiment
            print(f"Kicking off {num_samples} experiments of {p} perturbations on n={s}")
            try:
                exp = experiment(**args_dict)
                exp.perform(num_samples)
            except:
                print("...FAILED.")
        #
    #
