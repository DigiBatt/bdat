import altair_theme

import altair as alt

brush = alt.selection_interval(empty=True, resolve="union")
color = alt.condition(brush, alt.Color("cell:N", legend=None), alt.value("lightgray"))
scatter = (
    alt.Chart("example.json")
    .mark_circle()
    .encode(
        x=alt.X("start:Q", title="time / days"),
        y=alt.Y("aging_rate:Q", title="aging rate", scale=alt.Scale(zero=False)),
        color=color,
        detail="cell:N",
        tooltip=["cell:N"],
    )
    .add_params(brush)
    .properties(height=270, width=480)
)
hist = (
    alt.Chart("example.json")
    .mark_bar()
    .encode(
        x=alt.X("aging_rate:Q", title="aging rate").bin(step=0.0001, extent=[0, 0.005]),
        y=alt.Y("count()", title="count", scale=alt.Scale(domain=[0, 100])),
    )
    .transform_filter(brush)
    .properties(height=270, width=480)
)
chart = scatter | hist
print(chart.to_json())
