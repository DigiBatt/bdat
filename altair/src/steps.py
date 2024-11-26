import altair_theme

import altair as alt

currentColor = "#f58518"
voltageColor = "#4c78a8"

stepDomain = ["Pause", "CCStep", "CVStep", "CPStep"]

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

stepchart = (
    alt.Chart("plotdata_steps.json")
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
print(chart.to_json())
