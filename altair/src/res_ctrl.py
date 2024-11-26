import altair_theme

import altair as alt

chart = (
    alt.Chart("plotdata_resistance.json")
    .mark_line(point=True)
    .encode(
        alt.X("specimen:O", title="cell"),
        alt.Y("ctp:Q", title="charge throughput / Ah", scale=alt.Scale(zero=False)),
        color=alt.Color("time:T"),
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
        ],
        row=alt.Row("current:O", title="current / A"),
        column=alt.Column("duration:O", title="duration / s"),
    )
)
print(chart.to_json())
