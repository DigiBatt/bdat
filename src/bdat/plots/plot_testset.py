import pandas as pd

from bdat import entities
from bdat.database.storage.entity import Entity
from bdat.database.storage.storage import Storage
from bdat.entities.patterns import TestinfoEval
from bdat.entities.plots import Plotdata
from bdat.plots.plot import plot


@plot("testset")
def plot_testset(storage: Storage, testset: Entity) -> Plotdata:
    if not isinstance(testset, entities.ActivitySet):
        raise Exception("Invalid resource type")

    tests = storage.find(
        None, entities.Cycling, {"set": testset.res_id_or_raise().to_str()}
    )

    df = pd.DataFrame.from_records(
        [get_test_info(storage, t) for t in tests if t.parent is None]
    )

    return Plotdata(
        f"testset plot - {testset.title}", testset, "testset", {"tests": df}
    )


def get_test_info(storage: Storage, test: entities.Cycling):
    testeval = None
    evals = storage.find(
        None, entities.TestEval, {"test": test.res_id_or_raise().to_str()}
    )
    if len(evals) > 0:
        testeval = evals[0]
    if testeval is None:
        children = storage.find(
            None, entities.Cycling, {"parent": test.res_id_or_raise().to_str()}
        )
        for c in children:
            evals = storage.find(
                None, entities.TestEval, {"test": test.res_id_or_raise().to_str()}
            )
            if len(evals) > 0:
                testeval = evals[0]
                break

    if testeval is None:
        link = f"/records/{test.res_id_or_raise().id}"
    else:
        link = f"/records/{testeval.res_id_or_raise().id}"

    return {
        "circuit": test.tool.title if test.tool else None,
        "cell": test.object.title,
        "start": test.start,
        "end": test.end,
        "link": link,
        "title": test.title,
        "has_eval": testeval is not None,
    }
