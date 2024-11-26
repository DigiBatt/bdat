import os

import requests
from mvl.storage.resource_id import CollectionId, DatabaseId, ResourceId
from mvl.storage.storage import Storage

import bdat.entities
import bdat.functions as functions
import prefect.runtime.flow_run
from bdat.exceptions.missing_dependency_exception import MissingDependencyException
from prefect import flow
from prefect.blocks.system import Secret


async def get_config():
    os.environ["PREFECT_FLOW_ID"] = prefect.runtime.flow_run.get_id()
    kadi_url = await Secret.load("bdat-database-url")
    kadi_token = await Secret.load("bdat-database-token")
    return {
        "kadi": {
            "type": "kadi",
            "url": kadi_url.get(),
            "token": kadi_token.get(),
        }
    }


def signal_flow_result(config, status=None, dependencies=None):
    data = {}
    if status:
        data["status"] = status
    if dependencies:
        data["dependencies"] = dependencies
    requests.post(
        config["kadi"]["url"] + "/api/flows/" + prefect.runtime.flow_run.get_id(),
        headers={"Authorization": f"Bearer {config['kadi']['token']}"},
        json=data,
    )


@flow
async def steps(record_id: int, replace_id: int | None = None):
    config = await get_config()
    storage = Storage(config, "bdat.entities")
    res_id = ResourceId(
        CollectionId(DatabaseId("kadi"), "cycling"), record_id, bdat.entities.Cycling
    )
    replace: ResourceId | bool = True
    if replace_id is not None:
        replace = ResourceId(
            CollectionId(DatabaseId("kadi"), "steplist"),
            replace_id,
            bdat.entities.Steplist,
        )
    try:
        result = functions.steps(
            storage,
            res_id,
            CollectionId(res_id.collection.database, "steplist"),
            replace,
        )
    except requests.HTTPError as e:
        signal_flow_result(config, status="retry")
        raise e
    except Exception as e:
        signal_flow_result(config, status="error")
        raise e

    if result is None:
        signal_flow_result(config, status="no_result")
    elif result.state != "finished":
        signal_flow_result(config, status=result.state)


@flow
async def patterns(record_id: int, replace_id: int | None = None):
    config = await get_config()
    storage = Storage(config, "bdat.entities")
    res_id = ResourceId(
        CollectionId(DatabaseId("kadi"), "steplist"), record_id, bdat.entities.Steplist
    )
    db = res_id.collection.database
    replace: ResourceId | bool = True
    if replace_id is not None:
        replace = ResourceId(
            CollectionId(DatabaseId("kadi"), "testeval"),
            replace_id,
            bdat.entities.TestEval,
        )
    try:
        result = functions.patterns(
            storage,
            res_id,
            CollectionId(db, "testeval"),
            debug=False,
            patterntype=None,
            replace=replace,
        )
        dependencies = None
        if result and result.previous:
            dependencies = [record_id, result.previous.res_id_or_raise().id]
    except requests.HTTPError as e:
        signal_flow_result(config, status="retry")
        raise e
    except MissingDependencyException as e:
        if e.missing_type == bdat.entities.Steplist:
            previous_id = f"{e.missing_link.res_id_or_raise().id}#steps#patterns"
        else:
            previous_id = f"{e.missing_link.res_id_or_raise().id}#patterns"
        dependencies = [record_id, previous_id]
        signal_flow_result(config, status="pending", dependencies=dependencies)
        return
    except Exception as e:
        signal_flow_result(config, status="error")
        raise e

    if result is None:
        signal_flow_result(config, status="no_result")
    elif result.state != "finished" or dependencies is not None:
        signal_flow_result(config, status=result.state, dependencies=dependencies)


@flow
async def plot(record_id, plot_type):
    config = await get_config()
    storage = Storage(config, "bdat.entities")
    res_id = ResourceId(
        CollectionId(DatabaseId("kadi"), "cycling"), record_id, bdat.entities.Cycling
    )
    return functions.plot(
        storage,
        res_id,
        plot_type,
        CollectionId(res_id.collection.database, "plotdata"),
        True,
    )


@flow
async def update(record_id):
    config = await get_config()
    storage = Storage(config, "bdat.entities")
    res_id = ResourceId(
        CollectionId(DatabaseId("kadi"), "cycling"), record_id, bdat.entities.Cycling
    )
    return functions.update(storage, res_id)
