""" Test the ParMOO MDML extension, reload, and plot existing data set.

Create a start up MDML client and optimize the producer using the ParMOO
generator as the consumer.

Unless HOST ID is properly configured, this file will only replay existing
experiments and generate plots of the data.

"""

# This value must be set to a valid MDML host for anything other than replaying
# past experiments
HOST_ID = 'ENTER A VALID MDML HOST IP ADDRESS HERE'

# These are config/data files
INIT_FILE  = 'tfmc-manufacture-config.json'       # Path to config file
RELD_FILE  = 'results/tfmc-manufacture-data.json' # Path to data file
TOPIC      = 'mdml-CFR-experiment-01'             # Topic for MDML broadcasts

# Determines how to run
RELOAD = True   # Reload data
RESTART = False # Do not restart the experiment, i.e., 


# ------------ Function definitions and driver code starts below -------------


def parmoo_funcx(initializer=None, reloader=None, budget=10):
    """ This is an interface through which the ParMOO solver can be registered
    as a funcx service and run remotely.

    Args:
        initializer (str, optional, default: None): An optional config file
            to initialize the ParMOO solver from a JSON instead of manually
            building through ParMOO's standard API

        reloader (str, optional, default: None): An optional data file
            to relaod past experiment data (recorded by MDML) into the
            ParMOO solver

        budget (int, optional, default: 10): The number of ParMOO iterations
            to run, after the initial search. The total budget will be
            budget * number of acquisition functions + initial search budget.

    """

    import numpy as np
    import logging
    from parmoo_mdml_extension import MDML_MOOP
    import mdml_client as mdml

    # Turn on logging
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    # Create and load/reload the MOOP
    moop = MDML_MOOP(HOST_ID, topic=TOPIC)
    if initializer is not None:
        moop.load_definition(initializer)
    if reloader is not None:
        moop.reload_results(reloader)
    ## Checkpointing is off, uncomment below to turn it on
    # moop.setCheckpoint(True)

    ## Run ParMOO -- if the HOST_ID environment variable is set, then uncomment
    ## below to start solving via MDML consumer/producer requests
    # moop.solve(budget)
    return moop.getSimulationData()


if __name__ == "__main__":
    """ Driver code running that creats a ParMOO/MDML solver, replays results,
    and plots them with pyplot.

    """

    import json
    import numpy as np

    # Read environment variables from the top of the file
    if RELOAD:
        reloader = open(RELD_FILE)
        data = json.load(reloader)
        reloader.close()
    else:
        data = None
    if RESTART:
        initializer = open(INIT_FILE)
        config = json.load(initializer)
        initializer.close()
    else:
        config = None

    # Fix the random seed
    np.random.seed(10252021)


    # Call a ParMOO/MDML funcx service locally and load its database
    sim_db = parmoo_funcx(initializer=config, reloader=data, budget=0)


    # Plot the results with Pyplot
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap

    # Get figure handle
    fig = plt.figure()

    # Set the font styles
    plt.rc('text', usetex=True)
    plt.rc('font', size=12)
    plt.rc('legend', fontsize=12)

    # Build a color map
    colors = np.linspace(0.0, 1.0, sim_db['cfr_out'].shape[0])
    colors[:] = 0.6 - (colors[:] * 0.6)
    colorarray = []
    for color in colors:
        colorarray.append([color, color, color])
    cmap = ListedColormap(colorarray)
    t = np.arange(sim_db['cfr_out'].shape[0])

    # Scatter plot of the data
    plt.scatter(sim_db['cfr_out']['out'][:, 1],
                sim_db['cfr_out']['out'][:, 0],
                s = 20,
                c = t,
                cmap=cmap)

    # Generate axis labels and legends
    plt.xlabel("NMR peak area -- TFMC (product)")
    plt.ylabel("NMR peak area -- TFE (byproduct)")
    plt.colorbar(label = "Experiment index")

    # Set the margins and save the figure output to eps file
    fig.set_figheight(3)
    fig.set_figwidth(6)
    plt.tight_layout()
    plt.savefig("tfmc-tradeoff.eps", format="eps")
