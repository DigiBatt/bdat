import altair_theme

import altair as alt

brush = alt.selection_interval(empty=True, resolve="union", encodings=["x"])

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
    # .add_params(brush)
    .transform_calculate(
        y="abs(datum.capacity)",
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
    # .add_params(brush)
    .transform_calculate(
        absCurrent="abs(datum.current)", ageDays="datum.age / (3600 * 24)"
    )
)

layerchart = alt.layer(capchart, reschart).resolve_scale(
    y="independent", color="independent"
)

timechart = layerchart.encode(alt.X("ageDays:Q", title="time / days")).add_params(
    brush
)  # .transform_calculate(ageDays="datum.age")
chargechart = layerchart.encode(
    alt.X("chargeThroughput:Q", title="charge throughput / Ah")
).add_params(brush)

ocvBase = (
    alt.Chart("plotdata_ocv.json")
    .mark_line()
    .encode(
        x=alt.X("charge:Q", title="capacity / Ah"),
        y=alt.Y(
            "voltage:Q",
            title="voltage / V",
            scale=alt.Scale(zero=False),
        ),
        color=alt.Color(
            "ageDays:Q",
            title="age / days",
            scale=alt.Scale(scheme="blues", reverse=True),
        ),
    )
    .transform_calculate(ageDays="datum.age / (3600 * 24)")
    .transform_filter(brush)
)
dvaBase = (
    alt.Chart("plotdata_dva.json")
    .mark_line()
    .encode(
        x=alt.X("dvaX:Q", title="capacity / Ah"),
        y=alt.Y(
            "smoothDvaY:Q",
            title="diff. voltage / (V / Ah)",
            scale=alt.Scale(zero=False),
        ),
        color=alt.Color(
            "ageDays:Q",
            title="age / days",
            scale=alt.Scale(scheme="reds", reverse=True),
        ),
    )
    .transform_filter(alt.datum.smoothDvaY < 3)
    .transform_calculate(ageDays="datum.age / (3600 * 24)")
    .transform_filter(brush)
)
icaChart = (
    alt.Chart("plotdata_ica.json")
    .mark_line()
    .encode(
        x=alt.X(
            "smoothIcaY:Q",
            title="inc. capacity / (Ah / V)",
            scale=alt.Scale(zero=False),
        ),
        y=alt.Y("icaX:Q", title="voltage / V", scale=alt.Scale(zero=False)),
        color=alt.Color(
            "ageDays:Q",
            title="age / days",
            scale=alt.Scale(scheme="greens", reverse=True),
        ),
        order="icaX:Q",
    )
    .transform_calculate(ageDays="datum.age / (3600 * 24)")
    .transform_filter(brush)
)

qocvChartCharge = alt.layer(
    alt.layer(
        ocvBase.transform_filter(alt.datum.direction == "charge"),
        dvaBase.transform_filter(alt.datum.direction == "charge"),
    ).resolve_scale(y="independent", color="independent"),
    icaChart.transform_filter(alt.datum.direction == "charge"),
).resolve_scale(x="independent", color="independent")

qocvChartDischarge = alt.layer(
    alt.layer(
        ocvBase.transform_filter(alt.datum.direction == "discharge"),
        dvaBase.transform_filter(alt.datum.direction == "discharge"),
    ).resolve_scale(y="independent", color="independent"),
    icaChart.transform_filter(alt.datum.direction == "discharge"),
).resolve_scale(x="independent", color="independent")

chart = alt.vconcat(timechart, chargechart, qocvChartCharge, qocvChartDischarge)

print(chart.to_json())
