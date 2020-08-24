from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, View

from sw_collections.models import Collection
from sw_collections.services import CollectionsDisplayService, CollectionsFetchService


class CollectionsView(ListView):
    model = Collection
    template_name = "sw_collections/list.html"


class CollectionsDetailView(DetailView):
    model = Collection
    template_name = "sw_collections/detail.html"

    paginate_rows_by = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collections_service = CollectionsDisplayService()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        limit = int(self.request.GET.get("limit", self.paginate_rows_by))

        context.update(
            {
                "limit": limit + self.paginate_rows_by,
                "headers": self.collections_service.headers,
                "people": self.collections_service.display(self.get_object(), limit),
            }
        )
        return context


class CollectionsFetchView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collections_service = CollectionsFetchService()

    def get(self, *args, **kwargs):
        self.collections_service.fetch()
        return redirect("sw-collections:list")
