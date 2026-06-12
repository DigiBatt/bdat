import typing
from dataclasses import dataclass

import pandas as pd

from bdat.database.storage.entity import Entity
from bdat.entities.dataspec.charge_spec import ChargeSpec
from bdat.entities.dataspec.column_spec import ColumnSpec, TimeColumnSpec


@dataclass
class DataSpec(Entity[str]):
    id: str
    durationColumn: TimeColumnSpec
    timeColumn: TimeColumnSpec | None

    @classmethod
    def from_df(cls, df: pd.DataFrame) -> typing.Self:
        raise NotImplementedError()


@dataclass
class CyclingDataSpec(DataSpec):
    currentColumn: ColumnSpec
    voltageColumn: ColumnSpec
    chargeSpec: ChargeSpec
    temperatureColumn: ColumnSpec | None = None
    powerColumn: ColumnSpec | None = None
    stepNumberColumn: ColumnSpec | None = None
    cycleNumberColumn: ColumnSpec | None = None
    ambientTemperatureColumn: ColumnSpec | None = None
    procedureLevelColumn: ColumnSpec | None = None

    def tryOnTest(self, testdata: pd.DataFrame) -> bool:
        if not self.durationColumn.name in testdata.columns:
            # print(f"Missing {self.durationColumn.name}")
            return False
        if not self.currentColumn.name in testdata.columns:
            # print(f"Missing {self.currentColumn.name}")
            return False
        if not self.voltageColumn.name in testdata.columns:
            # print(f"Missing {self.voltageColumn.name}")
            return False
        if not all([c.name in testdata.columns for c in self.chargeSpec.getColumns()]):
            # print(f"Missing {[c.name for c in self.chargeSpec.getColumns()]}")
            return False
        if (
            self.temperatureColumn
            and not self.temperatureColumn.name in testdata.columns
        ):
            # print(f"Missing {self.temperatureColumn.name}")
            return False
        if self.timeColumn and not self.timeColumn.name in testdata.columns:
            return False
        if self.powerColumn and not self.powerColumn.name in testdata.columns:
            return False
        if self.stepNumberColumn and not self.stepNumberColumn.name in testdata.columns:
            return False
        if (
            self.cycleNumberColumn
            and not self.cycleNumberColumn.name in testdata.columns
        ):
            return False
        if (
            self.ambientTemperatureColumn
            and not self.ambientTemperatureColumn.name in testdata.columns
        ):
            return False
        if (
            self.procedureLevelColumn
            and not self.procedureLevelColumn.name in testdata.columns
        ):
            return False
        return True

    def convert(self, data: pd.DataFrame, target: "CyclingDataSpec") -> pd.DataFrame:
        columns = dict(
            [
                entry
                for entry in [
                    CyclingDataSpec.__convert_column(self, target, data, column)
                    for column in self.__dict__.keys()
                ]
                if entry is not None
            ]
        )
        if self.chargeSpec.__class__ == target.chargeSpec.__class__:
            for column in self.chargeSpec.__dict__.keys():
                k, v = CyclingDataSpec.__convert_column(
                    self.chargeSpec, target.chargeSpec, data, column
                )
                columns[k] = v
        return pd.DataFrame(columns)

    @staticmethod
    def __convert_column(
        source: "CyclingDataSpec | ChargeSpec",
        target: "CyclingDataSpec | ChargeSpec",
        data: pd.DataFrame,
        column: str,
    ):
        sourceColumn = getattr(source, column, None)
        targetColumn = getattr(target, column, None)
        if isinstance(sourceColumn, ColumnSpec) and isinstance(
            targetColumn, ColumnSpec
        ):
            return (
                targetColumn.name,
                sourceColumn.convert(data[sourceColumn.name].to_numpy(), targetColumn),
            )
        elif isinstance(sourceColumn, TimeColumnSpec) and isinstance(
            targetColumn, TimeColumnSpec
        ):
            return (
                targetColumn.name,
                sourceColumn.convert(data[sourceColumn.name].to_numpy(), targetColumn),
            )
        else:
            return None


@dataclass
class EISDataSpec(DataSpec):
    batteryVoltageColumn: ColumnSpec
    frequencyColumn: ColumnSpec
    realColumn: ColumnSpec
    imaginaryColumn: ColumnSpec
    amplitudeColumn: ColumnSpec
    phaseColumn: ColumnSpec
    excitationAmplitudeColumn: ColumnSpec
    temperatureColumn: ColumnSpec | None = None

    def tryOnTest(self, testdata: pd.DataFrame) -> bool:
        if not self.durationColumn.name in testdata.columns:
            return False
        if not self.batteryVoltageColumn.name in testdata.columns:
            return False
        if not self.frequencyColumn.name in testdata.columns:
            return False
        if not self.realColumn.name in testdata.columns:
            return False
        if not self.imaginaryColumn.name in testdata.columns:
            return False
        if not self.amplitudeColumn.name in testdata.columns:
            return False
        if not self.phaseColumn.name in testdata.columns:
            return False
        if not self.excitationAmplitudeColumn.name in testdata.columns:
            return False
        if self.timeColumn and not self.timeColumn.name in testdata.columns:
            return False
        if (
            self.temperatureColumn
            and not self.temperatureColumn.name in testdata.columns
        ):
            return False
        return True
