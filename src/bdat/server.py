from flask import Flask, Response, render_template, request, url_for

import bdat.functions
from bdat import entities
from bdat.database.storage.resource_param import ResourceIdParam
from bdat.database.storage.storage import Storage

storage: Storage

app = Flask(
    "bdat",
    static_folder="../../altair",
    static_url_path="/static",
    template_folder="../../altair/template",
)


@app.route("/plot/<resource_id>", methods=["GET"])
def show_plot(resource_id):
    return render_template(
        "plot.html",
        chart_script=url_for("get_script", resource_id=resource_id),
    )


@app.route("/script/<resource_id>", methods=["GET"])
def get_script(resource_id):
    plot_id = ResourceIdParam(entities.plots.Plotdata).convert(resource_id, None, None)
    plottype = request.args.get("plottype", None)
    if plottype is None:
        plotdata = storage.get_as_doc(plot_id)
        plottype = plotdata["plottype"]
    data_endpoint = request.args.get("data_endpoint", None)
    if data_endpoint is None:
        data_endpoint = "get_plotdata"
    script = f"const chartspec_url = '/static/out/{plottype}.json';\n"
    script += f"const data_url = '{url_for(data_endpoint, resource_id=resource_id, dataset='')}';\n"
    script += """
        function insertDataUrl(spec, data_url) {
            Object.keys(spec).some(function(k) {
                if (k === 'data') {
                    spec[k].url = data_url + spec[k].url;
                }
                if (spec[k] && typeof spec[k] === 'object') {
                    spec[k] = insertDataUrl(spec[k], data_url);
                }
            });
            return spec;
        }

        function showChart(spec, data_url) {
            spec = insertDataUrl(spec, data_url);
            var opt = { "renderer": "canvas", "actions": true };
            vegaEmbed("#vis", spec, opt);
        }

        fetch(chartspec_url).then(res => res.json()).then(spec => showChart(spec, data_url));
    """
    return Response(script, mimetype="application/javascript")


@app.route("/data/plot/<resource_id>/<dataset>", methods=["GET"])
def get_plotdata(resource_id, dataset):
    plot_id = ResourceIdParam(entities.plots.Plotdata).convert(resource_id, None, None)
    plotdata = storage.get_as_doc(plot_id)
    if dataset == "example.json":
        return plotdata["data"]
    else:
        return plotdata["data"][dataset]


@app.route("/stepsplot/<resource_id>", methods=["GET"])
def get_stepsplot(resource_id):
    return render_template(
        "plot.html",
        chart_script=url_for(
            "get_script",
            resource_id=resource_id,
            plottype="steps",
            data_endpoint="get_stepsdata",
        ),
    )


@app.route("/data/steps/<resource_id>/<dataset>", methods=["GET"])
def get_stepsdata(resource_id, dataset):
    test_id = ResourceIdParam(entities.test.Test).convert(resource_id, None, None)
    steps = bdat.functions.steps(storage, test_id)
    plot = bdat.functions.plot(storage, steps, "steps")
    return plot.data[dataset]


@app.route("/steps/<resource_id>", methods=["GET"])
def get_steps(resource_id):
    group_id = ResourceIdParam(entities.group.TestGroup).convert(
        resource_id, None, None
    )
    group = storage.get_as_doc(group_id)
    return render_template(
        "plotgroup.html",
        plot_url=url_for("get_stepsplot", resource_id=""),
        items=group["tests"],
    )
