import typing
from dataclasses import dataclass

from .typeofobject import TypeOfObject


@dataclass
class Geometry(TypeOfObject):
    type: "str | None"
    height: "float | None"
    length: "float | None"
    width: "float | None"
    diameter: "float | None"
