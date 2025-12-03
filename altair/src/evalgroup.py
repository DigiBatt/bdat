import altair_theme

import altair as alt

selection = alt.selection_interval(
    empty=True, resolve="union", name="selection"  # , fields=["test:N"]
)

capchart = (
    alt.Chart("plotdata_capacity.json")
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
        y="abs(datum.capacity)",
        absCurrent="abs(datum.current)",
        ageDays="datum.age / (3600 * 24)",
    )
    .transform_filter(selection)
)
reschart = (
    alt.Chart("plotdata_resistance.json")
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
    .transform_filter(selection)
)

layerchart = alt.layer(capchart, reschart).resolve_scale(
    y="independent", color="independent"
)

timechart = layerchart.encode(
    alt.X("ageDays:Q", title="time / days")
)  # .transform_calculate(ageDays="datum.age")
chargechart = layerchart.encode(alt.X("ctp:Q", title="charge throughput / Ah"))

qocvchart = (
    alt.Chart("plotdata_qocv.json")
    .mark_line(strokeWidth=0.5)
    .encode(
        x=alt.X("chargePercentage:Q", title="capacity / %"),
        y=alt.Y(
            "voltage:Q",
            title="voltage / V",
            scale=alt.Scale(zero=False),
        ),
        detail="qocvId:N",
        color=alt.Color(
            "absCurrent:Q",
            title="current / A",
            scale=alt.Scale(scheme="blues", zero=True),
        ),
        tooltip=["specimen:N", "current:Q"],
    )
    .transform_calculate(absCurrent="abs(datum.current)")
    .transform_filter(selection)
)

ctpchart = (
    alt.Chart("plotdata_ctp.json")
    .mark_line(strokeWidth=0.5, point=True)
    .encode(
        x=alt.X("ageDays:Q", title="time / days"),
        y=alt.Y("ctp:Q", title="charge throughput / Ah"),
        detail="specimen:O",
        tooltip=["specimen:N"],
    )
    .transform_calculate(ageDays="datum.age / (3600 * 24)")
    .add_params(selection)
)


chart = alt.vconcat(timechart, chargechart, qocvchart, ctpchart)

print(chart.to_json())
