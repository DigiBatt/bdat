from abc import ABC, abstractmethod
from dataclasses import dataclass

from bdat.database.storage.entity import Entity
from bdat.entities.aging.aging_conditions import AgingConditions


class CellState:
    pass


@dataclass
class AgingModel(Entity[int], ABC):
    pass

    @abstractmethod
    def predict(
        self, before: CellState, conditions: AgingConditions, duration: float
    ) -> CellState:
        pass
