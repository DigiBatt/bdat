Structure
=========

.. image:: images/bdat_structure.svg

Data analysis is divided into multiple steps that are described in more detail in the sections below.
A simple example of using these steps on a data file is given in the Jupyter notebook :doc:`examples/simple.ipynb`.

Import test data
----------------

.. image:: images/bdat_test_data.svg

In order to import test data from a file, the structure of the data must be known. This is encapsulated in the :py:class:`~bdat.entities.dataspec.data_spec.DataSpec` class.
By default, bdat will attempt to parse a file using a list of known data formats, including the `Battery Data Format <https://github.com/battery-data-alliance/battery-data-format>`__.
Additional formats can be added by extending the function :py:func:`bdat.dataimport.import_rules.get_dataspec`.
For files using one of the known formats, the DataSpec object can be created by calling :py:func:`~bdat.dataimport.import_rules.get_dataspec`:

.. code-block:: python

    import pandas as pd

    batterytype = bdat.BatterySpecies("My Battery Type", capacity=1.0)
    battery = bdat.Battery("Cell 0001", type=batterytype)
    cycling = bdat.Cycling("Initial checkup", object=battery)
    df = pd.read_parquet("testdata.parquet")
    dataspec = bdat.get_dataspec(cycling, df)
    data = bdat.CyclingData(cycling, df, dataspec)

Alternatively, a custom data format can also be constructed before importing the data:

.. code-block:: python

    import pandas as pd

    batterytype = bdat.BatterySpecies("My Battery Type", capacity=1.0)
    battery = bdat.Battery("Cell 0001", type=batterytype)
    cycling = bdat.Cycling("Initial checkup", object=battery)
    df = pd.read_parquet("testdata.parquet")
    dataspec = bdat.DataSpec(
        "neware-converted",
        durationColumn=bdat.TimeColumnSpec("Time##T_+01_00", bdat.Timestamp()),
        currentColumn=bdat.ColumnSpec("Current#A#D"),
        voltageColumn=bdat.ColumnSpec("Voltage#V#D"),
        chargeSpec=bdat.SeparateColumns(
            bdat.ColumnSpec("Charge Capacity#Ah#D"), bdat.ColumnSpec("Discharge Capacity#Ah#D")
        ),
    )
    data = bdat.CyclingData(cycling, df, dataspec)

Segment data into steps
-----------------------

.. image:: images/bdat_test_steps.svg

The first analysis step after importing the data is to separate it into steps.
This is done using :py:func:`bdat.steps.find_steps`.
The function returns a :py:class:`~bdat.entities.steps.steplist.Steplist` object that containst a list of steps with metadata such as duration, current, and voltage:

.. code-block:: python

    steplist = bdat.steps.find_steps(data)

Find and evaluate patterns
--------------------------

.. image:: images/bdat_patterns_eval.svg

In a second step, the list of steps is searched for patterns that correspond to specific test sequences.
A list of available patterns can be seen in the :py:mod:`bdat.resources.patterns` documentation.
The :py:func:`bdat.patterns.find_patterns` function will search a :py:class:`~bdat.entities.steps.steplist.Steplist` object for a list of patterns and return results for all matches:

.. code-block:: python

    patterntypes = [
        bdat.patterns.Captest(),
        bdat.patterns.Testinfo(),
        bdat.patterns.UniformCycling(),
    ]
    testeval = bdat.patterns.find_patterns(steplist, patterntypes, data)

This returns a :py:class:`~bdat.entities.patterns.test_eval.TestEval` object containing a list of :py:class:`~bdat.entities.patterns.pattern_eval.PatternEval` instances that hold information about the detected matches.
Examples for further usage of this data are given in the example notebooks.
