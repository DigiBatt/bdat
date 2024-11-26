import numpy as np
import pandas as pd
import pytest

from bdat.dataimport.normalize import normalize, normalize_column
from bdat.entities.dataspec.charge_spec import Calculate
from bdat.entities.dataspec.column_spec import ColumnSpec, TimeColumnSpec, Unit
from bdat.entities.dataspec.data_spec import DataSpec
from bdat.entities.dataspec.time_format import Datetime, Seconds, Timestamp


def test_normalize_column():
    columnIn = pd.Series([1, 2, 3, np.nan, np.inf, -np.inf])
    sourceSpec = ColumnSpec("in", Unit.BASE)
    targetSpec = ColumnSpec("out", Unit.MILLI)
    columnOut = normalize_column(columnIn, sourceSpec, targetSpec)
    assert np.array_equal(
        columnOut.to_numpy(),
        np.array([1000, 2000, 3000, np.nan, np.inf, -np.inf]),
        equal_nan=True,
    )


def test_normalize():
    dfIn = pd.DataFrame(
        {
            "t": [
                pd.Timestamp(1679828119, unit="s"),
                pd.Timestamp(1679828120, unit="s"),
            ],
            "i": [2.2, 2.7],
            "v": [3305, 4120],
        }
    )
    sourceDuration = TimeColumnSpec("t", Timestamp())
    sourceCurrent = ColumnSpec("i")
    sourceSpec = DataSpec(
        "testspec",
        sourceDuration,
        sourceCurrent,
        ColumnSpec("v", Unit.MILLI),
        Calculate(sourceCurrent, sourceDuration),
    )
    targetDuration = TimeColumnSpec("Duration", Seconds())
    targetCurrent = ColumnSpec("Current", Unit.MILLI)
    targetSpec = DataSpec(
        "testspec",
        targetDuration,
        targetCurrent,
        ColumnSpec("Voltage"),
        Calculate(targetCurrent, targetDuration),
    )
    dfOut = normalize(dfIn, sourceSpec, targetSpec)
    assert list(dfOut.columns) == ["Duration", "Current", "Voltage"]
    assert np.array_equal(
        dfOut["Duration"].to_numpy(), np.array([1679828119, 1679828120])
    )
    assert np.array_equal(dfOut["Current"].to_numpy(), np.array([2200, 2700]))
    assert np.array_equal(dfOut["Voltage"].to_numpy(), np.array([3.305, 4.12]))

    sourceSpec.durationColumn.timeFormat = Datetime()
    with pytest.raises(NotImplementedError):
        normalize(dfIn, sourceSpec, targetSpec)

    sourceSpec.durationColumn.timeFormat = Timestamp()
    targetSpec.durationColumn.timeFormat = Datetime()
    with pytest.raises(NotImplementedError):
        normalize(dfIn, sourceSpec, targetSpec)
