import functools
import os
import typing

import requests
from mvl.exceptions.missing_attribute_exception import MissingAttributeException
from mvl.exceptions.unexpected_value_exception import UnexpectedValueException
from mvl.storage.resource_id import CollectionId, DatabaseId, ResourceId
from mvl.storage.storage import Storage

import bdat.entities
import bdat.functions as functions
import prefect.runtime.flow_run
from bdat.exceptions import (
    MissingDataspecException,
    MissingDependencyException,
    NoCyclingDataException,
    NoDatafileException,
    ParquetFormatException,
)
from prefect import flow
from prefect.blocks.system import Secret


def handle_errors(config, e: Exception):
    if isinstance(e, requests.HTTPError):
        if e.response.status_code == 400:
            signal_flow_result(config, status="no_result", statuscode=2)
        else:
            signal_flow_result(config, status="retry")
            raise e
    elif isinstance(e, MissingDataspecException):
        signal_flow_result(config, status="no_result", statuscode=1)
    elif isinstance(e, NoCyclingDataException):
        signal_flow_result(config, status="no_result", statuscode=3)
    elif isinstance(e, NoDatafileException):
        signal_flow_result(config, status="no_result", statuscode=4)
    elif isinstance(e, ParquetFormatException):
        signal_flow_result(config, status="error", statuscode=3)
    elif isinstance(e, MissingAttributeException):
        signal_flow_result(config, status="error", statuscode=4)
    elif isinstance(e, UnexpectedValueException):
        signal_flow_result(config, status="error", statuscode=5)
    else:
        signal_flow_result(config, status="error")
        raise e


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


def signal_flow_result(
    config, status=None, dependencies=None, statuscode=None, record_id=None
):
    data = {}
    if status:
        data["status"] = status
    if dependencies:
        data["dependencies"] = dependencies
    if statuscode:
        data["statuscode"] = statuscode
    if record_id:
        data["record_id"] = record_id
    requests.post(
        config["kadi"]["url"] + "/api/flows/" + prefect.runtime.flow_run.get_id(),
        headers={"Authorization": f"Bearer {config['kadi']['token']}"},
        json=data,
    )


def get_record_status(config, record_id: int | str) -> str:
    r = requests.get(
        config["kadi"]["url"]
        + "/api/coeus/dependencygraph/"
        + str(record_id).replace("#", "%23")
        + "/status",
        headers={"Authorization": f"Bearer {config['kadi']['token']}"},
    )
    return r.json()["status"]


@flow
async def steps(record_id: int, replace_id: int | None = None):
    config = await get_config()
    storage = Storage(config, "bdat.entities")
    res_id = ResourceId(
        CollectionId(DatabaseId("kadi"), "cycling"), record_id, bdat.entities.Cycling
    )
    test = storage.get_or_raise(res_id)
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
    except Exception as e:
        if test.end is None:
            if isinstance(e, MissingAttributeException):
                signal_flow_result(config, status="retry")
            else:
                signal_flow_result(config, status="preliminary")
        else:
            handle_errors(config, e)
        return

    if result is None:
        if test.end is None:
            signal_flow_result(config, status="preliminary")
        else:
            signal_flow_result(config, status="no_result")
    else:
        signal_flow_result(
            config, status=result.state, record_id=result.res_id_or_raise().id
        )


@flow
async def patterns(
    record_id: int,
    replace_id: int | None = None,
):
    config = await get_config()
    replace: ResourceId | bool = True
    if replace_id is not None:
        replace = ResourceId(
            CollectionId(DatabaseId("kadi"), "testeval"),
            replace_id,
            bdat.entities.TestEval,
        )
    try:
        result = _patterns(config, record_id, replace)
        dependencies = None
        if result and result.previous:
            dependencies = [record_id, result.previous.res_id_or_raise().id]
    except MissingDependencyException as e:
        if e.missing_type == bdat.entities.Steplist:
            previous_id = f"{e.missing_link.res_id_or_raise().id}#steps#patterns"
        else:
            previous_id = f"{e.missing_link.res_id_or_raise().id}#patterns"
        dependencies = [record_id, previous_id]
        signal_flow_result(config, status="pending", dependencies=dependencies)
        return
    except Exception as e:
        handle_errors(config, e)
        return

    if result is None:
        signal_flow_result(config, status="no_result")
    else:
        signal_flow_result(
            config,
            status=result.state,
            dependencies=dependencies,
            record_id=result.res_id_or_raise().id,
        )


def _patterns(
    config: typing.Dict,
    record_id: int,
    replace: ResourceId | bool,
    ignore_test: typing.List[ResourceId] = [],
):
    storage = Storage(config, "bdat.entities")
    res_id = ResourceId(
        CollectionId(DatabaseId("kadi"), "steplist"), record_id, bdat.entities.Steplist
    )
    db = res_id.collection.database
    try:
        return functions.patterns(
            storage,
            res_id,
            CollectionId(db, "testeval"),
            debug=False,
            patterntype=None,
            replace=replace,
            ignore_test=ignore_test,
        )
    except MissingDependencyException as e:
        if e.missing_type == bdat.entities.Steplist:
            if (
                get_record_status(
                    config, f"{e.missing_link.res_id_or_raise().id}#steps"
                )
                == "no_result"
            ):
                ignore_test.append(e.missing_link.res_id_or_raise())
                return _patterns(config, record_id, replace, ignore_test)
        raise e


@flow
async def plot(record_id, plot_type, replace_id: int | None = None):
    config = await get_config()
    storage = Storage(config, "bdat.entities")
    res_id = ResourceId(
        CollectionId(DatabaseId("kadi"), "entity"), record_id, bdat.entities.Entity
    )
    replace: ResourceId | bool = True
    if replace_id is not None:
        replace = ResourceId(
            CollectionId(DatabaseId("kadi"), "plotdata"),
            replace_id,
            bdat.entities.Plotdata,
        )
        if plot_type is None:
            plotdata = storage.get_or_raise(replace)
            plot_type = plotdata.plottype
    try:
        if plot_type is None:
            raise Exception("Plot type must be specified")
        result = functions.plot(
            storage,
            res_id,
            plot_type,
            CollectionId(res_id.collection.database, "plotdata"),
            replace,
            return_str=False,
        )
    except Exception as e:
        handle_errors(config, e)

    signal_flow_result(
        config, status=result.state, record_id=result.res_id_or_raise().id
    )


@flow
async def update(record_id):
    config = await get_config()
    storage = Storage(config, "bdat.entities")
    res_id = ResourceId(
        CollectionId(DatabaseId("kadi"), "cycling"), record_id, bdat.entities.Cycling
    )
    try:
        result = functions.update(storage, res_id, False, return_str=False)
    except Exception as e:
        handle_errors(config, e)

    signal_flow_result(
        config, status=result.state, record_id=result.res_id_or_raise().id
    )


@flow
async def evalgroup(record_id, replace_id: int | None = None):
    config = await get_config()
    storage = Storage(config, "bdat.entities")
    res_id = ResourceId(
        CollectionId(DatabaseId("kadi"), "testeval"), record_id, bdat.entities.TestEval
    )
    try:
        if replace_id is None:
            res = storage.get(res_id)
            if not isinstance(res, bdat.entities.TestEval):
                raise Exception(f"Could not find record with id {res_id.to_str()}")
            r = requests.get(
                config["kadi"]["url"] + "/api/flows/evalgroups",
                headers={"Authorization": f"Bearer {config['kadi']['token']}"},
                json={
                    "testset": None if res.test.set is None else res.test.set.id,
                    "project": (
                        None if res.test.project is None else res.test.project.id
                    ),
                    "species": (
                        None
                        if res.test.object.type is None
                        else res.test.object.type.id
                    ),
                    "specimen": res.test.object.id,
                    "test": res.test.id,
                    "evaltype": list(set([e.get_type() for e in res.evals])),
                },
            )
            r.raise_for_status()
            dependencies = [
                record_id,
                *[[record_id, group_id] for group_id in r.json()],
            ]
            signal_flow_result(config, status="no_result", dependencies=dependencies)
        else:
            group_id = ResourceId(
                CollectionId(DatabaseId("kadi"), "evalgroup"),
                replace_id,
                bdat.entities.EvalGroup,
            )
            group = functions.update(storage, group_id, False, False)
            dependencies = [
                record_id,
                *[[e.id, replace_id] for e in group.evals],
            ]
            signal_flow_result(
                config,
                status=group.state,
                dependencies=dependencies,
                record_id=group.res_id_or_raise().id,
            )

    except Exception as e:
        handle_errors(config, e)


@flow
async def cell_life(record_id: int, replace_id: int | None = None):
    config = await get_config()
    storage = Storage(config, "bdat.entities")
    res_id = ResourceId(
        CollectionId(DatabaseId("kadi"), "battery"), record_id, bdat.entities.Battery
    )
    replace: ResourceId | bool = True
    if replace_id is not None:
        replace = ResourceId(
            CollectionId(DatabaseId("kadi"), "celllife"),
            replace_id,
            bdat.entities.CellLife,
        )
    try:
        eval_ids = storage.query_ids(
            CollectionId(DatabaseId("kadi"), "testeval"),
            int,
            bdat.entities.TestEval,
            {
                "outgoing": [
                    {
                        "name": "test",
                        "to": {
                            "type": "cycling",
                            "outgoing": [
                                {
                                    "name": "object",
                                    "to": {
                                        "type": "battery",
                                        "outgoing": [
                                            {"name": "project", "to": {"id": record_id}}
                                        ],
                                    },
                                }
                            ],
                        },
                    }
                ]
            },
        )
        result = functions.cell_life(
            storage,
            res_id,
            CollectionId(res_id.collection.database, "celllife"),
            False,
            replace=replace,
            return_str=False,
        )
        dependencies = [res_id.id for res_id in eval_ids]
        signal_flow_result(
            config,
            status=result.state,
            dependencies=dependencies,
            record_id=result.res_id_or_raise().id,
        )
    except Exception as e:
        handle_errors(config, e)


@flow
async def aging_data(record_id: int, replace_id: int | None = None):
    config = await get_config()
    storage = Storage(config, "bdat.entities")
    replace: ResourceId | bool = True
    if replace_id is None:
        raise Exception("Aging data can only be updated")
    else:
        replace = ResourceId(
            CollectionId(DatabaseId("kadi"), "celllife"),
            replace_id,
            bdat.entities.CellLife,
        )
    try:
        agingdata = functions.update(storage, replace, False, False)
        dependencies = [cl.res_id_or_raise().id for cl in agingdata.data]
        signal_flow_result(
            config,
            status=agingdata.state,
            dependencies=dependencies,
            record_id=agingdata.res_id_or_raise().id,
        )
    except Exception as e:
        handle_errors(config, e)
