from dataclasses import dataclass

import numpy as np

from bdat.entities.aging.aging_conditions import AgingConditions
from bdat.entities.aging.models.aging_model import AgingModel, CellState


@dataclass
class AlphaParameters:
    a1: float
    a2: float
    a3: float


@dataclass
class BetaParameters:
    b1: float
    b2: float
    b3: float
    b4: float


@dataclass
class SchmalstiegCellState(CellState):
    age: float
    chargeThroughput: float
    capacity: float
    resistance: float


@dataclass
class SchmalstiegModel(AgingModel):
    # alpha(V, T) = (a1 V - a2) * exp(- a3 / T)
    # beta(meanV, dod) = b1 * (meanV - b2)^2 + b3 * deltaDOD + b4
    # C = 1 - alpha_cap * t ^ 0.75 - beta_cap * Q ^ 0.5
    # R = 1 + alpha_res * t ^ 0.75 + beta_res * Q

    alpha_cap: AlphaParameters
    alpha_res: AlphaParameters
    beta_cap: BetaParameters
    beta_res: BetaParameters

    def predict(
        self,
        before: CellState,
        conditions: AgingConditions,
        duration: float,
    ) -> SchmalstiegCellState:
        if not isinstance(before, SchmalstiegCellState):
            raise RuntimeError()

        if conditions.temperature is None:
            raise RuntimeError()
        if conditions.meanVoltage is None:
            raise RuntimeError()
        if conditions.dod is None:
            raise RuntimeError()

        temp_kelvin = conditions.temperature + 273.15
        alpha_cap = (
            self.alpha_cap.a1 * conditions.meanVoltage - self.alpha_cap.a2
        ) * np.exp(-self.alpha_cap.a3 / temp_kelvin)
        alpha_res = (
            self.alpha_res.a1 * conditions.meanVoltage - self.alpha_res.a2
        ) * np.exp(-self.alpha_res.a3 / temp_kelvin)
        beta_cap = (
            self.beta_cap.b1 * (conditions.meanVoltage - self.beta_cap.b2) ** 2
            + self.beta_cap.b3 * conditions.dod
            + self.beta_cap.b4
        )
        beta_res = (
            self.beta_res.b1 * (conditions.meanVoltage - self.beta_res.b2) ** 2
            + self.beta_res.b3 * conditions.dod
            + self.beta_res.b4
        )

        return before
