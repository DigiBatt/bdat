import pandas as pd

import altair as alt
from bdat.database.storage.entity import Entity
from bdat.database.storage.storage import Storage
from bdat.dataimport import import_rules
from bdat.entities.dataspec.column_spec import Unit
from bdat.entities.plots import Plotdata
from bdat.entities.steps.step import CCStep
from bdat.entities.steps.steplist import Steplist
from bdat.plots.plot import plot

from . import altair_theme


@plot("steps")
def plot_steps(
    storage: Storage, steps: Entity, df: pd.DataFrame | None = None
) -> Plotdata:
    if not isinstance(steps, Steplist):
        raise Exception("Invalid resource type")
    test = steps.test
    if df is None:
        datafile = storage.get_file(test.res_id_or_raise())
        if datafile is None:
            raise Exception("Test has no data")
        df = pd.read_parquet(datafile)
    dataspec = import_rules.get_dataspec(test, df)
    duration = dataspec.durationColumn.timeFormat.toSeconds(
        df[dataspec.durationColumn.name].to_numpy()
    )
    timeBins = pd.cut(duration, 1000, labels=False)
    columns = [
        (dataspec.currentColumn, "current"),
        (dataspec.voltageColumn, "voltage"),
    ]
    if dataspec.temperatureColumn:
        columns.append((dataspec.temperatureColumn, "temperature"))
    dfValues = df[[spec.name for spec, _ in columns]].copy()
    dfValues["time"] = duration
    dfValues = dfValues.groupby(timeBins).mean()
    for spec, _ in columns:
        dfValues[spec.name] = spec.unit.convert(
            dfValues[spec.name].to_numpy(), Unit.BASE
        )
    dfValues.rename(
        columns={spec.name: title for spec, title in columns},
        inplace=True,
    )

    dfSteps = pd.DataFrame.from_records(
        [
            {
                "step": s.stepId,
                "steptype": s.get_type(),
                "start": s.start,
                "end": s.end,
                "duration": s.duration,
                "charge": s.charge,
                "startCurrent": s.getStartCurrent(),
                "endCurrent": s.getEndCurrent(),
                "startVoltage": s.getStartVoltage(),
                "endVoltage": s.getEndVoltage(),
            }
            for s in steps
        ]
    )

    currentColor = "#f58518"
    voltageColor = "#4c78a8"

    stepDomain = ["Pause", "CCStep", "CVStep", "CPStep"]

    basechart = alt.Chart(dfValues).mark_line()
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

    stepchart = (
        alt.Chart(dfSteps)
        .mark_rect()
        .encode(
            x=alt.X("start:Q", scale=alt.Scale(zero=False)),
            x2="end:Q",
            color=alt.Color(
                "steptype:N", scale=alt.Scale(scheme="set2", domain=stepDomain)
            ),
            opacity=alt.value(0.5),
            tooltip=[
                "steptype:N",
                "step:O",
                "start:Q",
                "end:Q",
                "duration:Q",
                "charge:Q",
                "startCurrent:Q",
                "endCurrent:Q",
                "startVoltage:Q",
                "endVoltage:Q",
            ],
        )
    )

    chart = stepchart + alt.layer(current, voltage).resolve_scale(y="independent")

    return Plotdata(
        f"plot {steps.title}",
        steps,
        "steps",
        {"test": dfValues, "steps": dfSteps},
        plot=chart.to_dict(),
    )
