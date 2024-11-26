import altair_theme

import altair as alt

currentColor = "#f58518"
voltageColor = "#4c78a8"

basechart = alt.Chart("example.json").mark_line()
current = basechart.encode(
    x=alt.X("time:Q", title="time / s"),
    y=alt.Y(
        "current:Q",
        title="current / A",
        scale=alt.Scale(zero=False),
        axis=alt.Axis(labelColor=currentColor, titleColor=currentColor),
    ),
    color=alt.value(currentColor),
    detail="eval:N",
    tooltip=["specimen:N"],
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
    detail="eval:N",
    tooltip=["specimen:N"],
)
chart = voltage & current
print(chart.to_json())
