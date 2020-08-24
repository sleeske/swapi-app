from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Response:
    results: Optional[List[Dict]] = None
    next_page: Optional[str] = None


@dataclass
class Planet:
    PREFIX = "planet_"

    class Columns:
        NAME = "name"
        URL = "url"

    @classmethod
    def prefix_value(cls, value: str):
        return cls.PREFIX + value


@dataclass
class Person:
    class Columns:
        NAME = "name"
        HEIGHT = "height"
        MASS = "mass"
        HAIR_COLOR = "hair_color"
        SKIN_COLOR = "skin_color"
        EYE_COLOR = "eye_color"
        BIRTH_YEAR = "birth_year"
        GENDER = "gender"
        HOMEWORLD = "homeworld"
        EDITED = "edited"

    class RenamedColumns:
        DATE = "date"
