bdat
====

Battery Data Analysis Toolkit

Setup
=====

Installation
------------

The required dependencies and the package itself can be installed using pip:

    pip install -r requirements.txt
    pip install -e .

Documentation
-------------

The documentation is built using the script

    ./build_docs.sh

Configuration
-------------

Configuration parameters can be provided in a JSON file.
Bdat will try to read the configuration from the following locations, from top to bottom:

- The path that is passed using the -c / --config option, if it is specified.
- ./config.json
- ~/.config/bdat/config.json

The config file contains information about the database(s) that bdat interacts with.
An example config looks like this:

    {
        "databases": {
            "kadi": {
                "type": "kadi",
                "url": "https://example.org",
                "token": "pat_xxxxxxxxxxxxx"
            }
        }
    }
