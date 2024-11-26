import altair_theme

import altair as alt

chart = (
    alt.Chart("plotdata_capacity.json")
    .mark_circle()
    .encode(
        alt.X("date:T", title="time"),
        alt.Y("specimen:O"),
        color=alt.Color(
            "current:O", title="current / A", scale=alt.Scale(scheme="category10")
        ),
        size=alt.Size("capacity:Q", scale=alt.Scale(zero=False)),
        tooltip=["specimen:O", "date:T", "current:O", "capacity:Q"],
    )
)
print(chart.to_json())
