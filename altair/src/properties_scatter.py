# import altair_theme

import altair as alt

chart = (
    alt.Chart("plotdata_properties.json")
    .mark_circle()
    .encode(
        alt.X("xValue:Q", title=None, scale=alt.Scale(zero=False)),
        alt.Y("yValue:Q", title=None, scale=alt.Scale(zero=False)),
        color=alt.Color("species:N", title="battery species"),
        column="xName:N",
        row="yName:N",
    )
    .resolve_scale(x="independent", y="independent")
    .properties(height=150, width=150)
)
print(chart.to_json())
