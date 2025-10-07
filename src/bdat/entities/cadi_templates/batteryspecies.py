import typing
from dataclasses import dataclass

from . import geometry, material
from .typeofobject import TypeOfObject


@dataclass
class BatterySpecies(TypeOfObject):
    parent: "BatterySpecies | None"
    geometry: "geometry.Geometry | None"
    anodeChemistry: "material.Material | None"
    cathodeChemistry: "material.Material | None"
    manufacturer: "str | None"
    typename: "str | None"
    version: "str | None"
    capacity: "float | None"
    minimumVoltage: "float | None"
    maximumVoltage: "float | None"
    endOfDischargeVoltage: "float | None"
    endOfChargeVoltage: "float | None"
    internalResistance: "float | None"
    countinuousChargeCurrent: "float | None"
    peakChargeCurrent: "float | None"
    continuousDischargeCurrent: "float | None"
    peakDischargeCurrent: "float | None"
    nominalCurrent: "float | None"
    minimumChargeTemperature: "float | None"
    maximumChargeTemperature: "float | None"
    minimumDischargeTemperature: "float | None"
    maximumDischargeTemperature: "float | None"
    weight: "float | None"
    energyDensity: "float | None"
