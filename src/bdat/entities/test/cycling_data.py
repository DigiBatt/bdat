import typing

import numpy as np
import pandas as pd

import bdat.entities as entities
from bdat.entities.cadi_templates import Cycling
from bdat.entities.dataspec.data_spec import CyclingDataSpec
from bdat.entities.dataspec.unit import Unit
from bdat.entities.steps.step import CyclingStep, Step


class CyclingData:
    test: Cycling
    df: pd.DataFrame
    dataSpec: CyclingDataSpec

    duration: np.ndarray  # test duration in seconds
    time: np.ndarray | None  # time as unix timestamp in seconds
    current: np.ndarray  # current in Ampere
    voltage: np.ndarray  # voltage in Volt
    charge: np.ndarray  # cumulative sum of charge over all tests for this battery in Ah
    discharge: (
        np.ndarray
    )  # cumulative sum of discharge over all tests for this battery in Ah
    diffcharge: np.ndarray  # difference between charge and discharge in Ah
    temperature: np.ndarray | None  # temperature in degrees Celsius
    power: np.ndarray  # power in Watt
    stepNumber: np.ndarray | None  # index of the current program step
    cycleNumber: np.ndarray | None  # index of the current cycle
    ambientTemperature: np.ndarray | None  # temperature in degrees Celsius

    def __init__(
        self,
        test: Cycling,
        df: pd.DataFrame,
        dataSpec: CyclingDataSpec,
        initialCharge: float = 0,
        initialDischarge: float = 0,
    ):
        df = self.__sort_df(df, dataSpec)

        self.test = test
        self.df = df
        self.dataSpec = dataSpec

        self.duration = dataSpec.durationColumn.timeFormat.toSeconds(
            df[dataSpec.durationColumn.name].to_numpy()
        )
        self.time = None
        if dataSpec.timeColumn is not None:
            self.time = dataSpec.timeColumn.timeFormat.toTimestamp(
                df[dataSpec.timeColumn.name].to_numpy()
            )
        self.current = dataSpec.currentColumn.from_df(df, Unit.BASE)
        self.voltage = dataSpec.voltageColumn.from_df(df, Unit.BASE)
        self.charge = dataSpec.chargeSpec.getChargeAh(df) + initialCharge
        self.discharge = dataSpec.chargeSpec.getDischargeAh(df) + initialDischarge
        self.diffcharge = (
            dataSpec.chargeSpec.getDiffAh(df) + initialCharge - initialDischarge
        )
        self.temperature = None
        self.stepNumber = None
        self.cycleNumber = None
        self.ambientTemperature = None
        if dataSpec.temperatureColumn is not None:
            self.temperature = dataSpec.temperatureColumn.from_df(df, Unit.BASE)
        if dataSpec.powerColumn is not None:
            self.power = dataSpec.powerColumn.from_df(df, Unit.BASE)
        else:
            self.power = self.current * self.voltage
        if dataSpec.stepNumberColumn is not None:
            self.stepNumber = df[dataSpec.stepNumberColumn.name].to_numpy(
                dtype=np.int32
            )
        if dataSpec.cycleNumberColumn is not None:
            self.cycleNumber = df[dataSpec.cycleNumberColumn.name].to_numpy(
                dtype=np.int32
            )
        if dataSpec.ambientTemperatureColumn is not None:
            self.ambientTemperature = dataSpec.ambientTemperatureColumn.from_df(
                df, Unit.BASE
            )

    def __sort_df(self, df: pd.DataFrame, dataSpec: CyclingDataSpec) -> pd.DataFrame:
        t = dataSpec.durationColumn.timeFormat.toSeconds(
            df[dataSpec.durationColumn.name].to_numpy()
        )
        current = df[dataSpec.currentColumn.name].to_numpy()
        dupes = np.nonzero(np.diff(t) == 0)
        index = np.arange(len(df))
        for idx in dupes[0]:
            if idx < 1 or idx > len(df) - 3:
                continue
            if np.abs(current[idx] - current[idx - 1]) > np.abs(
                current[idx] - current[idx + 2]
            ) and np.abs(current[idx + 1] - current[idx + 2]) > np.abs(
                current[idx + 1] - current[idx - 1]
            ):
                index[idx] = idx + 1
                index[idx + 1] = idx
        df = df.iloc[index]
        return df
