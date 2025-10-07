import typing

import numpy as np
import pandas as pd

import altair as alt
from bdat import entities
from bdat.database.storage.entity import Entity
from bdat.database.storage.storage import Storage
from bdat.entities.patterns import TestinfoEval
from bdat.entities.plots import Plotdata
from bdat.plots.plot import plot

from .plot_steps import plot_steps


@plot("testevals")
def plot_testevals(
    storage: Storage,
    testeval: Entity,
    df: pd.DataFrame | None = None,
    timerange: typing.Tuple[float, float] | None = None,
) -> Plotdata:
    if not isinstance(testeval, entities.patterns.TestEval):
        raise Exception("Invalid resource type")

    dfEvals = pd.DataFrame.from_records(
        [
            {
                "type": e.__class__.__name__,
                "firstStep": e.firstStep,
                "lastStep": e.lastStep,
                "start": e.start,
                "end": e.end,
            }
            for e in testeval.evals
            if not isinstance(e, TestinfoEval)
        ]
    )
    if timerange is not None:
        dfEvals = dfEvals[
            (dfEvals.start <= timerange[1]) & (dfEvals.end >= timerange[0])
        ]

    if testeval.steps.plotdata is None:
        dfTest = plot_steps(storage, testeval.steps, df, None, timerange).data["test"]
    else:
        dfTest = pd.DataFrame.from_records(testeval.steps.plotdata["test"])

    currentColor = "#f58518"
    voltageColor = "#4c78a8"

    evalDomain = [
        "DischargeCapacityEval",
        "PulseEval",
        "ChargeQOCVEval",
        "DischargeQOCVEval",
        "UniformCyclingEval",
        "CPChargeQOCVEval",
        "CPDischargeQOCVEval",
    ]

    basechart = alt.Chart(dfTest).mark_line()
    current = basechart.encode(
        x=alt.X("time:Q", title="time / s"),
        y=alt.Y(
            "current:Q",
            title="current / A",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(labelColor=currentColor, titleColor=currentColor),
        ),
        color=alt.value(currentColor),
    )
    voltage = basechart.encode(
        x=alt.X("time:Q", title="time / s"),
        y=alt.Y(
            "voltage:Q",
            title="voltage / V",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(labelColor=voltageColor, titleColor=voltageColor),
        ),
        color=alt.value(voltageColor),
    )

    evalchart = (
        alt.Chart(dfEvals)
        .mark_rect()
        .encode(
            x=alt.X("start:Q", scale=alt.Scale(zero=False)),
            x2="end:Q",
            color=alt.Color(
                "type:N", scale=alt.Scale(scheme="set2", domain=evalDomain)
            ),
            opacity=alt.value(0.5),
            tooltip=["type:N", "start:Q", "end:Q", "firstStep:O", "lastStep:O"],
        )
    )

    chart = evalchart + alt.layer(current, voltage).resolve_scale(y="independent")

    return Plotdata(
        f"testevals plot - {testeval.title}",
        testeval,
        "testevals",
        {"test": dfTest, "evals": dfEvals},
        chart.to_dict(),
    )
