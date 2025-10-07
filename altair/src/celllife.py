import altair_theme

import altair as alt

capchart = (
    alt.Chart("capacity.json")
    .mark_point(size=150)
    .encode(
        # alt.X("age:Q", title="age"),
        alt.Y("y:Q", title="capacity / Ah", scale=alt.Scale(zero=True)),
        # color=alt.value("red"),
        alt.Color(
            "absCurrent:Q",
            title="current / A",
            scale=alt.Scale(scheme="goldred", zero=True),
        ),
        tooltip=["y:Q", "dischargeCurrent:Q", "starttime:T"],
    )
    .transform_calculate(
        y="-datum.capacity",
        absCurrent="abs(datum.dischargeCurrent)",
        ageDays="datum.age / (3600 * 24)",
    )
)
reschart = (
    alt.Chart("resistance.json")
    .mark_point(size=100)
    .encode(
        # alt.X("age:Q", title="age"),
        alt.Y("impedance:Q", title="impedance / Ohm"),
        alt.Color(
            "absCurrent:Q",
            title="current / A",
            scale=alt.Scale(scheme="blues", zero=True),
        ),
        # shape=alt.value("triangle-up"),
        shape=alt.condition(
            alt.datum.current > 0, alt.value("triangle-up"), alt.value("triangle-down")
        ),
        tooltip=["impedance:Q", "current:Q", "starttime:T"],
    )
    .transform_calculate(
        absCurrent="abs(datum.current)", ageDays="datum.age / (3600 * 24)"
    )
)

layerchart = alt.layer(capchart, reschart).resolve_scale(
    y="independent", color="independent"
)

timechart = layerchart.encode(
    alt.X("ageDays:Q", title="time / days")
)  # .transform_calculate(ageDays="datum.age")
chargechart = layerchart.encode(
    alt.X("chargeThroughput:Q", title="charge throughput / Ah")
)

chart = alt.vconcat(timechart, chargechart)

print(chart.to_json())
