import altair_theme

import altair as alt

chart = (
    alt.Chart("plotdata_qocv.json")
    .mark_line(strokeWidth=0.5)
    .encode(
        x=alt.X("chargePercentage:Q", title="discharged capacity / %"),
        y=alt.Y(
            "voltage:Q",
            title="voltage / V",
            scale=alt.Scale(zero=False),
        ),
        detail="specimen:N",
        color="testset:N",
        tooltip=["specimen:N", "current:Q"],
    )
)  # .facet("species:N")
print(chart.to_json())
