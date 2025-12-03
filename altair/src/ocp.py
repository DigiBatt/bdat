import altair_theme

import altair as alt

chart = (
    alt.Chart("data.csv")
    .mark_line(strokeWidth=0.5)
    .encode(
        x=alt.X("soc:Q", title="SOC / %"),
        y=alt.Y(
            "potential:Q",
            title="electrode potential / V",
            scale=alt.Scale(zero=False),
        ),
    )
)
print(chart.to_json())
