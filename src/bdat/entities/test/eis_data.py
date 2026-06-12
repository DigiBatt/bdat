import numpy as np
import pandas as pd

import bdat.entities as entities
from bdat.entities.cadi_templates import Cycling
from bdat.entities.dataspec.data_spec import EISDataSpec
from bdat.entities.dataspec.unit import Unit


class EISData:
    test: Cycling
    df: pd.DataFrame
    dataSpec: EISDataSpec

    duration: np.ndarray  # test duration in seconds
    time: np.ndarray | None  # time as unix timestamp in seconds
    batteryVoltage: np.ndarray
    frequency: np.ndarray
    real: np.ndarray
    imaginary: np.ndarray
    amplitude: np.ndarray
    phase: np.ndarray
    excitationAmplitude: np.ndarray
    temperature: np.ndarray | None

    def __init__(
        self,
        test: Cycling,
        df: pd.DataFrame,
        dataSpec: EISDataSpec,
    ):
        self.test = test
        self.df = df
        self.dataSpec = dataSpec

        self.duration = dataSpec.durationColumn.timeFormat.toSeconds(
            df[dataSpec.durationColumn.name].to_numpy()
        )
        self.batteryVoltage = dataSpec.batteryVoltageColumn.from_df(df, Unit.BASE)
        self.frequency = dataSpec.frequencyColumn.from_df(df, Unit.BASE)
        self.real = dataSpec.realColumn.from_df(df, Unit.BASE)
        self.imaginary = dataSpec.imaginaryColumn.from_df(df, Unit.BASE)
        self.amplitude = dataSpec.amplitudeColumn.from_df(df, Unit.BASE)
        self.phase = dataSpec.phaseColumn.from_df(df, Unit.BASE)
        self.excitationAmplitude = dataSpec.excitationAmplitudeColumn.from_df(
            df, Unit.BASE
        )
        if dataSpec.timeColumn is not None:
            self.time = dataSpec.timeColumn.timeFormat.toTimestamp(
                df[dataSpec.timeColumn.name].to_numpy()
            )
        else:
            self.time = None
        if dataSpec.temperatureColumn is not None:
            self.temperature = dataSpec.temperatureColumn.from_df(df, Unit.BASE)
        else:
            self.temperature = None
