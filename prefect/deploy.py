#! /usr/bin/env python3

import flows

import bdat
import prefect

prefect.deploy(
    flows.steps.to_deployment("steps"),
    flows.patterns.to_deployment("patterns"),
    flows.plot.to_deployment("plot"),
    flows.update.to_deployment("update"),
    flows.evalgroup.to_deployment("evalgroup"),
    flows.cell_life.to_deployment("celllife"),
    flows.aging_data.to_deployment("agingdata"),
    work_pool_name="bdat",
    image=f"git.isea.rwth-aachen.de:5050/personal-projects/ess/eba/idap/bdat:{bdat.get_version()}-prefect",
    build=False,
    push=False,
)
