import altair_theme

import altair as alt

opacity = alt.condition(alt.datum.has_eval, alt.value(1), alt.value(0.5))

chart = (
    alt.Chart("plotdata_tests.json")
    .mark_bar()
    .encode(
        alt.X("start:T", title="time"),
        alt.X2("end:T", title="time"),
        alt.Y("cell:O"),
        alt.Href("link:N"),
        tooltip=[
            "cell:O",
            "circuit:N",
            "start:T",
            "end:T",
            "title:N",
            "has_eval:N",
            "program:N",
        ],
        color=alt.Color(
            "program:N", title="program", scale=alt.Scale(scheme="tableau20")
        ),
        opacity=opacity,
    )
    .properties(height=3500, width=1920)
    .configure_axis(labelFontSize=11)
)
print(chart.to_json())
