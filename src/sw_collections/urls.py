from django.urls import path
from sw_collections import views
from sw_collections.views import CollectionsDetailView

app_name = "sw-collections"

urlpatterns = [
    path("", views.CollectionsView.as_view(), name="list"),
    path("<int:pk>/", views.CollectionsDetailView.as_view(), name="detail"),
    path("fetch/", views.CollectionsFetchView.as_view(), name="fetch"),
]
