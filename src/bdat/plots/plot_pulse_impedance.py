import pandas as pd

from bdat.database.storage.entity import Entity
from bdat.database.storage.storage import Storage
from bdat.entities.group import EvalGroup
from bdat.entities.patterns import PulseEval
from bdat.entities.plots import Plotdata
from bdat.plots.plot import plot
from bdat.tools.misc import make_round_function


@plot("pulse_impedance")
def plot_pulse_impedance(storage: Storage, evalgroup: Entity) -> Plotdata:
    if not isinstance(evalgroup, EvalGroup):
        raise Exception("Invalid resource type")
    data = []

    round_duration = lambda x: round(x * 2, -1) / 2
    round_current = lambda x: round(x, 1)

    if evalgroup.unique_key:
        for k in evalgroup.unique_key:
            if k.startswith("duration"):
                round_duration = make_round_function(k, getattr)
            elif k.startswith("current"):
                round_current = make_round_function(k, getattr)

    for pe in evalgroup.evaldata:
        if not isinstance(pe, PulseEval):
            continue
        speciesName = None
        e = pe.testEval
        if e is None:
            raise Exception("Missing TestEval in PatternEval")
        species = e.test.object.type
        if species:
            speciesName = f"{species.manufacturer} {species.typename}"
            if species.version:
                speciesName += f" ({species.version})"
        duration = round_duration(pe)
        current = round_current(pe)
        if (duration == 0) or (abs(current) < 0.5):
            continue
        data.append(
            {
                "duration": duration,
                "current": current,
                "impedance": pe.impedance,
                "specimen": e.test.object.title,
                "species": speciesName,
                "test": e.test.title,
                "date": e.test.start,
                "eval": pe.res_id_or_raise().to_str(),
            }
        )

    df = pd.DataFrame.from_records(data)
    return Plotdata(
        "pulses", evalgroup, "pulse_impedance", {"pulses": df.to_dict(orient="records")}
    )
