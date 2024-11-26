import altair_theme

import altair as alt

ctp_chart = (
    alt.Chart("plotdata_capacity.json")
    .mark_line(point=True)
    .encode(
        alt.X("specimen:O", title="cell"),
        alt.Y("ctp:Q", title="charge throughput / Ah", scale=alt.Scale(zero=False)),
        color=alt.Color("time:T"),
        tooltip=[
            "specimen:O",
            "time:T",
            "capacity:Q",
            "age:Q",
            "ctp:Q",
            "test:O",
            "testeval:O",
            "steplist:O",
            "cycling:O",
        ],
    )
)
time_chart = (
    alt.Chart("plotdata_capacity.json")
    .mark_line(point=True)
    .encode(
        alt.X("specimen:O", title="cell"),
        alt.Y("time:T", title="date"),
        color=alt.Color("time:T"),
        tooltip=[
            "specimen:O",
            "time:T",
            "capacity:Q",
            "age:Q",
            "ctp:Q",
            "test:O",
            "testeval:O",
            "steplist:O",
            "cycling:O",
        ],
    )
)
chart = alt.vconcat(ctp_chart, time_chart)
print(chart.to_json())
