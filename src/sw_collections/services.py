import uuid
from typing import Callable

import petl as etl
from dateutil.parser import parse
from django.core.files.base import ContentFile

from sw_collections.models import Collection
from sw_collections.providers.swapi import CollectionDataProvider
from sw_collections.providers.swapi.entities import Person, Planet
from sw_collections.providers.swapi.exceptions import SWAPIError


class CollectionsService:
    def __init__(self):
        self.provider: CollectionDataProvider = CollectionDataProvider()

    def fetch(self) -> None:
        try:
            raw_planets: etl.Table = self._from_dict(fetch=self.provider.fetch_planets)
            raw_people: etl.Table = self._from_dict(fetch=self.provider.fetch_people)
        except SWAPIError as e:
            return

        data: etl.Table = self._shape_data(raw_planets, raw_people)
        self._persist_data(data)

    def _shape_data(self, raw_planets: etl.Table, raw_people: etl.Table) -> etl.Table:
        planets = etl.cut(raw_planets, (Planet.Columns.NAME, Planet.Columns.URL,))
        people = etl.cut(
            raw_people,
            (
                Person.Columns.NAME,
                Person.Columns.HEIGHT,
                Person.Columns.MASS,
                Person.Columns.HAIR_COLOR,
                Person.Columns.SKIN_COLOR,
                Person.Columns.EYE_COLOR,
                Person.Columns.BIRTH_YEAR,
                Person.Columns.GENDER,
                Person.Columns.HOMEWORLD,
                Person.Columns.EDITED,
            ),
        )

        combined = etl.join(
            planets,
            people,
            lkey=Planet.Columns.URL,
            rkey=Person.Columns.HOMEWORLD,
            lprefix=Planet.PREFIX,
        )

        renamed = etl.rename(
            combined,
            {
                Person.Columns.EDITED: Person.RenamedColumns.DATE,
                Planet.prefix_value(Planet.Columns.NAME): Person.Columns.HOMEWORLD,
            },
        )

        converted = etl.convert(
            renamed, {Person.RenamedColumns.DATE: lambda v: parse(v).date(),}
        )

        return etl.cut(
            converted,
            (
                Person.Columns.NAME,
                Person.Columns.HEIGHT,
                Person.Columns.MASS,
                Person.Columns.HAIR_COLOR,
                Person.Columns.SKIN_COLOR,
                Person.Columns.EYE_COLOR,
                Person.Columns.BIRTH_YEAR,
                Person.Columns.GENDER,
                Person.Columns.HOMEWORLD,
                Person.RenamedColumns.DATE,
            ),
        )

    def _from_dict(self, fetch: Callable) -> etl.Table:
        return etl.fromdicts(fetch())

    def _persist_data(self, data: etl.Table) -> None:
        sink = etl.MemorySource()
        data.tocsv(sink)

        collection: Collection = Collection.objects.create()
        collection.csv_file.save(
            f"{str(uuid.uuid4())}.csv", ContentFile(sink.getvalue())
        )
