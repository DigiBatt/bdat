import altair_theme

import altair as alt

chart = (
    alt.Chart("plotdata_capacity.json")
    .mark_line(point=True)
    .encode(
        alt.X("time:T", title="date"),
        alt.Y("capacity:Q", title="capacity / Ah", scale=alt.Scale(zero=False)),
        # color=alt.Color(
        #     "current:O", title="current / A", scale=alt.Scale(scheme="category10")
        # ),
        detail="specimen:O",
        tooltip=["specimen:O", "time:T", "current:O", "capacity:Q", "age:Q"],
    )
)
print(chart.to_json())
