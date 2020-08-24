from django.shortcuts import redirect
from django.views.generic import ListView, View

from sw_collections.models import Collection
from sw_collections.services import CollectionsService


class CollectionsView(ListView):
    model = Collection
    template_name = "sw_collections/list.html"


class FetchCollectionsView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collections_service = CollectionsService()

    def get(self, *args, **kwargs):
        self.collections_service.fetch()
        return redirect("sw-collections:list")
