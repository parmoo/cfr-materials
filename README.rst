============================================
A framework for fully autonomous design of materials via multiobjective optimization and active learning: challenges and next steps
============================================

This repository contains several scripts for optimizing the production of
the electrolyte 2,2,2-trifluoroethyl Methyl carbonate (TFMC) on a
continuous-flow reactor using the ParMOO solver with the MDML to distribute
experiment requests.
We have also included experimental data and a script for relplaying this
data and plotting it, using our ParMOO-MDML extension.

Setup and Running
-----------------

The requirements for this directory are:

 - parmoo_ (v 0.1.0),
 - mdml-client_, and
 - matplotlib_.

To try running these solvers your self, clone this directory and install
the requirements, or use the included ``REQUIREMENTS.txt`` file.

.. code-block:: bash

    python3 -m pip install -r REQUIREMENTS.txt

To replay the experiment and generate the results graph from Figure 1 in
the paper, run the following.

.. code-block:: bash

    cd parmoo-mdml-experiments && python3 cfr-tfmc-solver.py

To fully recreate our experiments, one would need to recreate the automated
CFR/NMR setup described in Appendix B of the paper, [create a valid MDML Host](MDML_HOST_SETUP.rst),
then uncomment the solve command in our script.

Directory Structure
-------------------

The base directory contains the ``README.rst`` and ``REQUIREMENTS.txt`` files.

The subdirectory ``parmoo-mdml-experiments`` contains:

 - ``__init__.py`` (package setup);
 - ``parmoo_mdml_extension.py`` (ParMOO ext using MDML to send experiments);
 - ``results`` (directory containing data from our 41 experiment run);
 - ``cfr-tfmc-solver.py`` (script for replaying the experiment in ``results`` and plotting); and
 - ``tfmc-manufacture-config.json`` (config file for our TFMC-making solver).

Citing this work
----------------

To cite this work, use the following:

.. code-block:: bibtex

    @misc{cfr-tfmc,
        title   = {A framework for fully autonomous design of materials via multiobjective optimization and active learning: challenges and next steps},
        author  = {Anonymous Authors},
        note    = {Under Review}
    }


.. _parmoo: https://parmoo.readthedocs.io
.. _matplotlib: https://matplotlib.org/
.. _mdml-client: https://mdml-client.readthedocs.io
