from django.urls import path
from sw_collections import views

app_name = "sw-collections"

urlpatterns = [
    path("", views.CollectionsView.as_view(), name="list"),
    path("<int:pk>/", views.CollectionsDetailView.as_view(), name="detail"),
    path(
        "<int:pk>/value-counts/",
        views.CollectionsValueCountsView.as_view(),
        name="value-counts",
    ),
    path("fetch/", views.CollectionsFetchView.as_view(), name="fetch"),
]
