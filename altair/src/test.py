import altair_theme

import altair as alt

currentColor = "#f58518"
voltageColor = "#4c78a8"

basechart = alt.Chart("data.json").mark_line()
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
temperature = basechart.encode(
    x=alt.X("time:Q", title="time / s"),
    y=alt.Y("temperature:Q", title="temperature / °C", scale=alt.Scale(zero=False)),
    color=alt.value("#e45756"),
)
chart = (
    (current + voltage).resolve_scale(y="independent").properties(height=340)
    & temperature.properties(height=200)
).resolve_scale(x="shared")
print(chart.to_json())
