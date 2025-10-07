import altair_theme

import altair as alt

chart = (
    alt.Chart("plotdata_resistance.json")
    .mark_line(point=True)
    .encode(
        alt.X("time:T", title="date"),
        alt.Y("impedance:Q", title="resistance / Ohm", scale=alt.Scale(zero=False)),
        color=alt.Color("soc:O"),
        detail="specimen:O",
        tooltip=[
            "specimen:O",
            "time:T",
            "current:O",
            "impedance:Q",
            "age:Q",
            "ctp:Q",
            "duration:O",
            "test:O",
            "testeval:O",
            "steplist:O",
            "soc:O",
        ],
        row=alt.Row("current:O", title="current / A"),
        column=alt.Column("duration:O", title="duration / s"),
    )
)
print(chart.to_json())
