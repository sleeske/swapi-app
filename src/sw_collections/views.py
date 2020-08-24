from typing import List

from django.shortcuts import redirect, render
from django.views.generic import DetailView, FormView, ListView, View

from sw_collections.forms import ColumnsForm
from sw_collections.models import Collection
from sw_collections.services import (
    CollectionsDisplayService,
    CollectionsFetchService,
    CollectionsValueCountService,
)


class CollectionsView(ListView):
    model = Collection
    template_name = "sw_collections/list.html"


class CollectionsDetailView(DetailView):
    model = Collection
    template_name = "sw_collections/detail.html"

    default_limit_param = "limit"
    paginate_rows_by = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._display_service = CollectionsDisplayService()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        limit = int(
            self.request.GET.get(self.default_limit_param, self.paginate_rows_by)
        )

        context.update(
            {
                "limit": limit + self.paginate_rows_by,
                "headers": self._display_service.headers,
                "rows": self._display_service.display(self.get_object(), limit),
            }
        )
        return context


class CollectionsValueCountsView(DetailView, FormView):
    model = Collection
    template_name = "sw_collections/value_counts.html"
    form_class = ColumnsForm
    aggr_name = "count"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value_count_service = CollectionsValueCountService()

    def form_valid(self, form):
        columns: List[str] = form.cleaned_data["columns"]

        context = {
            "form": form,
            "headers": columns + [self.aggr_name],
            "rows": self._value_count_service.count_values(
                self.get_object(), columns, self.aggr_name
            ),
        }
        return render(self.request, self.template_name, context)


class CollectionsFetchView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fetch_service = CollectionsFetchService()

    def get(self, *args, **kwargs):
        self._fetch_service.fetch()
        return redirect("sw-collections:list")
