import altair_theme

import altair as alt

chart = (
    alt.Chart("plotdata_pulses.json")
    .mark_circle()
    .encode(
        alt.X("specimen:O", title="cell"),
        alt.Y("impedance:Q", title=None, scale=alt.Scale(zero=False)),
        color=alt.Color("testset:N"),
        row=alt.Row("current:O", title=["current / A", "", "impedance / Ohm"]),
        column=alt.Column("duration:O", title="duration / s"),
    )
    .properties(height=100, width=1500)
    # .facet("current:N")
)
print(chart.to_json())
