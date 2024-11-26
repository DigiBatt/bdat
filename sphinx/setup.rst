Setup
=====

Installation
------------

Packaged version
^^^^^^^^^^^^^^^^

A prepackaged version can be installed from the ISEA Gitlab server:

.. code-block:: bash

    pip install --index-url https://token:glpat-usE95KpsDqnxVyuzGUTT@git.isea.rwth-aachen.de/api/v4/projects/2305/packages/pypi/simple bdat

Development vesion
^^^^^^^^^^^^^^^^^^

The source code of the project can be found in its `GitLab repository <https://git.isea.rwth-aachen.de/Personal-Projects/ESS/eba/idap/bdat>`__.
The required dependencies and the package itself can be installed using pip:

.. code-block:: bash

    pip install -r requirements.txt
    pip install -e .

Configuration
-------------

Configuration parameters can be provided in a JSON file.
Bdat will try to read the configuration from the following locations, from top to bottom:

- The path that is passed using the -c / --config option, if it is specified.
- ./config.json
- ~/.config/bdat/config.json

The config file contains information about the database(s) that bdat interacts with.
An example config looks like this:

.. code-block:: json

    {
        "databases": {
            "kadi": {
                "type": "kadi",
                "url": "https://cadi.isea.rwth-aachen.de",
                "token": "pat_xxxxxxxxxxxxx"
            }
        }
    }
