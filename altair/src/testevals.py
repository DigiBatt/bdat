import altair_theme

import altair as alt

currentColor = "#f58518"
voltageColor = "#4c78a8"
ocvColor = "#4c78a8"
dvaColor = "#f58518"

evalDomain = [
    "DischargeCapacityEval",
    "PulseEval",
    "ChargeQOCVEval",
    "DischargeQOCVEval",
    "UniformCyclingEval",
    "CPChargeQOCVEval",
    "CPDischargeQOCVEval",
]

basechart = alt.Chart("plotdata_test.json").mark_line()
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
    alt.Chart("plotdata_evals.json")
    .mark_rect()
    .encode(
        x=alt.X("start:Q", scale=alt.Scale(zero=False)),
        x2="end:Q",
        color=alt.Color("type:N", scale=alt.Scale(scheme="set2", domain=evalDomain)),
        opacity=alt.value(0.5),
        tooltip=["type:N", "start:Q", "end:Q", "firstStep:O", "lastStep:O"],
    )
)

qocvchart = (
    alt.Chart("plotdata_qocv.json")
    .mark_line()
    .encode(
        x=alt.X("charge:Q", title="capacity / Ah"),
        y=alt.Y(
            "voltage:Q",
            title="voltage / V",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(labelColor=ocvColor, titleColor=ocvColor),
        ),
        color=alt.value(ocvColor),
    )
)

dvachart = (
    alt.Chart("plotdata_qocv.json")
    .mark_line()
    .encode(
        x=alt.X("dvaX:Q", title="capacity / Ah"),
        y=alt.Y(
            "dvaY:Q",
            title="diff. voltage / (V/Ah)",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(labelColor=dvaColor, titleColor=dvaColor),
        ),
        color=alt.value(dvaColor),
    )
)

# chart = alt.vconcat(
#     evalchart + alt.layer(current, voltage).resolve_scale(y="independent"),
#     alt.layer(qocvchart, dvachart).resolve_scale(y="independent"),
# )
chart = evalchart + alt.layer(current, voltage).resolve_scale(y="independent")
print(chart.to_json())
