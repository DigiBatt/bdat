import typing
from dataclasses import dataclass

from .legalentity import LegalEntity


@dataclass
class Person(LegalEntity):
    firstname: "str | None"
    lastname: "str | None"
    login: "str | None"
