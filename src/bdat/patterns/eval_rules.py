from typing import Type

from bdat.entities.steps import Steplist
from bdat.resources.patterns.eval_pattern import EvalPattern

# TODO: temporary solution, this should be configured by database entities


def get_pattern_args(steps: Steplist, evaltype: Type[EvalPattern]) -> dict:
    if steps.test.set is not None and steps.test.set.project.title == "e production":
        if evaltype.__name__ == "Captest":
            return {
                # "chargeCurrent": 2.05,
                "dischargeCurrent": (-2.1, -0.9),
                "eocVoltage": 4.1,
                "eodVoltage": 3.0,
            }
        elif evaltype.__name__ == "DischargeQOCV":
            return {
                "dischargeCurrent": (-0.55, 0.0),
                "eocVoltage": 4.1,
                "eodVoltage": 3.0,
            }
        elif evaltype.__name__ == "ChargeQOCV":
            return {
                "chargeCurrent": (0.0, 0.55),
                "eocVoltage": 4.1,
                "eodVoltage": 3.0,
            }
    if (
        steps.test.object.type is not None
        and steps.test.object.type.title == "ARTS Energy VREDL5500AVGCFG"
    ):
        if evaltype.__name__ == "Captest":
            return {
                "eocVoltage": (1.4, 1.5),
                "dischargeCurrent": 2.0,
                "eodVoltage": (0.8, 1.1),
            }
        elif evaltype.__name__ == "DischargeQOCV":
            return {
                "eocVoltage": (1.4, 1.5),
                "dischargeCurrent": (-0.3, 0.0),
            }
        elif evaltype.__name__ == "ChargeQOCV":
            return {"eocVoltage": (1.4, 1.5), "chargeCurrent": (0, 0.4)}
    elif (
        steps.test.object.type is not None
        and steps.test.object.type.title == "Panasonic BK120AAHU"
    ):
        if evaltype.__name__ == "Captest":
            return {
                "eocVoltage": (1.4, 1.5),
                "eodVoltage": (0.95, 1.1),
                "ccDuration": 57600,
            }
        elif evaltype.__name__ == "DischargeQOCV":
            return {
                "eocVoltage": (1.4, 1.5),
                "ccDuration": 28800,
            }
        elif evaltype.__name__ == "ChargeQOCV":
            return {"eocVoltage": (1.4, 1.5), "chargeCurrent": (0, 0.1)}
    elif (
        steps.test.object.type is not None
        and steps.test.object.type.title == "Goldencell JGPFR26650"
    ):
        if evaltype.__name__ == "Captest":
            return {
                "eocVoltage": (3.63, 3.67),
                "eodVoltage": (2.45, 2.54),
            }
    elif (
        steps.test.object.type is not None
        and steps.test.object.type.title == "Lithium Werks ANR26650M1B"
    ):
        if evaltype.__name__ == "Captest":
            return {
                "eocVoltage": (3.57, 3.62),
                "eodVoltage": (1.94, 2.15),
            }
    elif (
        steps.test.object.type is not None
        and steps.test.object.type.title == "Samsung INR18650-25R (Tentative)"
    ):
        if evaltype.__name__ == "Captest":
            return {
                "eodVoltage": (2.45, 2.56),
            }

    if (
        evaltype.__name__ == "Captest"
        and steps.test.project is not None
        and steps.test.project.title == "J8027_DigiBatt"
    ):
        return {
            "dischargeCurrent": (-1e9, -0.2),
        }

    if (
        steps.test.object.project is not None
        and steps.test.object.project.title == "J4043_MaCy_KiloCycling"
    ):
        if evaltype.__name__ == "CPDischargeQOCV":
            return {
                "dischargePower": (-1e9, 0.0),
                "numSamples": None,
                "makeDerivatives": False,
            }
        elif evaltype.__name__ == "CPChargeQOCV":
            return {
                "chargePower": (0.0, 1e9),
                "numSamples": None,
                "makeDerivatives": False,
            }
        elif evaltype.__name__ == "DischargeQOCV":
            return {
                "dischargeCurrent": (-1e9, 0.0),
                "numSamples": None,
                "makeDerivatives": False,
            }
        elif evaltype.__name__ == "ChargeQOCV":
            return {
                "chargeCurrent": (0.0, 1e9),
                "numSamples": None,
                "makeDerivatives": False,
            }

    return {}
