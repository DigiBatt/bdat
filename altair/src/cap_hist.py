import altair_theme

import altair as alt

# chart = (
#     alt.Chart("plotdata_capacity.json")
#     .mark_bar()
#     .encode(
#         alt.X("capacity:Q", title="capacity / Ah").bin(maxbins=30),
#         alt.Y("count()", title="number of cells", stack=None),
#         alt.Color("testset:N"),
#     )
#     .facet(row="species:N")
# )
chart = (
    alt.Chart("plotdata_capacity.json")
    .mark_circle()
    .encode(
        alt.X("specimen:O", title="cell"),
        alt.Y("capacity:Q", title="capacity / Ah", scale=alt.Scale(zero=False)),
        alt.Color("testset:N"),
        tooltip=["specimen:O", "capacity:Q", "testset:N"],
    )
    .properties(height=100, width=1500)
    .facet(row="species:N")
    .resolve_scale(x="independent", y="independent")
)
print(chart.to_json())
