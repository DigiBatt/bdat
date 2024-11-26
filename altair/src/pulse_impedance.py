import altair_theme

import altair as alt

chart = (
    alt.Chart()
    .mark_circle()
    .encode(
        alt.X("specimen:O", title="cell"),
        alt.Y("impedance:Q", title="impedance / Ohm", scale=alt.Scale(zero=False)),
        color=alt.Color(
            "duration:O", title="duration / s", scale=alt.Scale(scheme="category10")
        ),
        tooltip=[
            "specimen:N",
            "impedance:Q",
            "test:N",
            "date:N",
            "duration:Q",
            "current:Q",
            "eval:N",
        ],
    )
    # + alt.Chart()
    # .mark_text(align="left", fontSize=10, baseline="top")
    # .encode(x=alt.value(0), y=alt.value(0), text=alt.value("abc123"))
    .properties(height=200, width=1200)
).facet(row=alt.Row("current:O", title="current / A"), data="example.json")

print(chart.to_json())
