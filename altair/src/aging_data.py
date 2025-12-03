import altair_theme

import altair as alt

brush_cal = alt.selection_interval(empty=True, resolve="union")
zoom_cal = alt.selection_interval(bind="scales")
color_cal = alt.condition(
    brush_cal, alt.Color("cell:N", legend=None), alt.value("lightgray")
)
timechart_cal_cap = (
    alt.Chart("plotdata_cal.json")
    .mark_line(point=True)
    .encode(
        x=alt.X("age_c:Q", title="time / days"),
        y=alt.Y("capacity:Q", title="capacity / Ah", scale=alt.Scale(zero=False)),
        color=color_cal,
        detail="cell:N",
        tooltip=["cell:N", "temperature:Q", "soc:Q"],
    )
    .transform_filter(brush_cal)
    .add_params(zoom_cal)
    .properties(height=270, width=480)
)
timechart_cal_res = (
    alt.Chart("plotdata_cal.json")
    .mark_line(point=True)
    .encode(
        x=alt.X("age_r:Q", title="time / days"),
        y=alt.Y("resistance:Q", title="resistance / Ohm", scale=alt.Scale(zero=False)),
        color=color_cal,
        detail="cell:N",
        tooltip=["cell:N", "temperature:Q", "soc:Q"],
    )
    .transform_filter(brush_cal)
    .add_params(zoom_cal)
    .properties(height=270, width=480)
)
paramchart_cal = (
    alt.Chart("plotdata_cal.json")
    .mark_point()
    .encode(
        x=alt.X("meanSoc:Q", title="SOC / %", scale=alt.Scale(zero=False)),
        y=alt.Y("temperature:Q", title="temperature / °C", scale=alt.Scale(zero=False)),
        color=color_cal,
        size=alt.value(100),
        tooltip=["cell:N", "temperature:Q", "soc:Q"],
    )
    .add_params(brush_cal)
    .properties(height=270, width=480)
)

# dropdown_cyc_x = alt.binding_select(
#     options=["ctp_c", "age_c"], name="X axis for cyclic capacity: "
# )
# param_cyc_x = alt.param(value="ctp_c", bind=dropdown_cyc_x)
dropdown_cyc_x = alt.binding_select(
    options=[
        "meanSoc",
        "minSoc",
        "maxSoc",
        "maxVoltage",
        "chargeCurrent",
        "dischargeCurrent",
        "dischargePower",
        "temperature",
    ],
    name="X axis for cyclic test matrix: ",
)
param_cyc_x = alt.param(value="meanSoc", bind=dropdown_cyc_x)

brush_cyc = alt.selection_interval(empty=True, resolve="union")
zoom_cyc = alt.selection_interval(bind="scales")
color_cyc = alt.condition(
    brush_cyc, alt.Color("cell:N", legend=None), alt.value("lightgray")
)
timechart_cyc_cap = (
    alt.Chart("plotdata_cyc.json")
    .mark_line(point=True)
    .encode(
        x=alt.X("ctp_c:Q", title="charge throughput / Ah"),
        y=alt.Y("capacity:Q", title="capacity / Ah", scale=alt.Scale(zero=False)),
        color=color_cyc,
        detail="cell:N",
        tooltip=[
            "cell:N",
            "dod:Q",
            "temperature:Q",
            "chargeCurrent:Q",
            "dischargeCurrent:Q",
            "dischargePower:Q",
            "minVoltage:Q",
            "maxVoltage:Q",
            "meanVoltage:Q",
            "minSoc:Q",
            "maxSoc:Q",
            "meanSoc:Q",
        ],
    )
    .transform_calculate(x=f"datum[{param_cyc_x.name}]")
    .transform_filter(brush_cyc)
    .add_params(zoom_cyc, param_cyc_x)
    .properties(height=270, width=480)
)
timechart_cyc_res = (
    alt.Chart("plotdata_cyc.json")
    .mark_line(point=True)
    .encode(
        x=alt.X("ctp_r:Q", title="charge throughput / Ah"),
        y=alt.Y("resistance:Q", title="resistance / Ohm", scale=alt.Scale(zero=False)),
        color=color_cyc,
        detail="cell:N",
        tooltip=[
            "cell:N",
            "dod:Q",
            "temperature:Q",
            "chargeCurrent:Q",
            "dischargeCurrent:Q",
            "dischargePower:Q",
            "minVoltage:Q",
            "maxVoltage:Q",
            "meanVoltage:Q",
            "minSoc:Q",
            "maxSoc:Q",
            "meanSoc:Q",
        ],
    )
    .transform_calculate(x=f"datum[{param_cyc_x.name}]")
    .transform_filter(brush_cyc)
    .add_params(zoom_cyc)
    .properties(height=270, width=480)
)
paramchart_cyc = (
    alt.Chart("plotdata_cyc.json")
    .mark_point()
    .encode(
        x=alt.X("x:Q", title=None, scale=alt.Scale(zero=False)),
        y=alt.Y("dod:Q", title="DOD / %", scale=alt.Scale(zero=False)),
        color=color_cyc,
        size=alt.value(100),
        detail="meanSoc:Q",
        tooltip=[
            "cell:N",
            "dod:Q",
            "temperature:Q",
            "chargeCurrent:Q",
            "dischargeCurrent:Q",
            "dischargePower:Q",
            "minVoltage:Q",
            "maxVoltage:Q",
            "meanVoltage:Q",
            "minSoc:Q",
            "maxSoc:Q",
            "meanSoc:Q",
        ],
    )
    .transform_calculate(x=f"datum[{param_cyc_x.name}]")
    .add_params(brush_cyc)
    .properties(height=270, width=480)
)

chart = (paramchart_cal | timechart_cal_cap | timechart_cal_res) & (
    paramchart_cyc | timechart_cyc_cap | timechart_cyc_res
)
print(chart.to_json())
