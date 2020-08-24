from typing import Dict, List, Optional

import requests
from django.conf import settings

from sw_collections.providers.swapi.actions import APIAction
from sw_collections.providers.swapi.entities import Response


class FetchDataError(Exception):
    pass


class CollectionDataProvider:
    def __init__(self):
        self.base_url: str = settings.SWAPI_BASE_URL

    def fetch_people(self):
        return self._paginated_get(APIAction.FETCH_PEOPLE)

    def fetch_planets(self):
        return self._paginated_get(APIAction.FETCH_PLANETS)

    def _paginated_get(self, action: APIAction):
        objects: List[Dict] = []

        response: Response = self._get(self._format_url(action))
        if response.results:
            objects.extend(response.results)

        while response.next_page:
            response = self._get(response.next_page)
            if response.results:
                objects.extend(response.results)

        return objects

    def _get(self, url) -> Response:
        response = requests.get(url)
        if not response.ok:
            raise FetchDataError(response.text)

        data = response.json()
        return Response(data.get("results"), data.get("next"))

    def _format_url(self, action: APIAction) -> str:
        return self.base_url + action.value
