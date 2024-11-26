from dataclasses import dataclass

from bdat.entities.aging.models.aging_model import AgingModel
from bdat.entities.aging.models.schmalstieg_model import SchmalstiegCellState


@dataclass
class AlphaParameters:
    a1: float
    a2: float
    a3: float
    a_e: float


@dataclass
class BetaParameters:
    b1: float
    b2: float
    b3: float
    b4: float
    b5: float
    b6: float
    b_e: float


@dataclass
class ExtendedSchmalstiegModel(AgingModel):
    # alpha(V, T) = (a1 V - a2) * exp(- a3 / T)
    # beta(meanV, dod, T, cRate) = (b1 * (meanV - b2)^2 + b3 * deltaDOD + b4 * cRate + b5) * exp(- b6 / T)
    # C = 1 - alpha_cap * t ^ a_e - beta_cap * Q ^ b_e
    # R = 1 + alpha_res * t ^ a_e + beta_res * Q ^ b_e

    alpha_cap: AlphaParameters
    alpha_res: AlphaParameters
    beta_cap: BetaParameters
    beta_res: BetaParameters
