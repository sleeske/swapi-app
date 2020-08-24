from django.urls import path
from sw_collections import views

app_name = "sw-collections"

urlpatterns = [
    path("collections/", views.CollectionsView.as_view(), name="list"),
    path("collections/fetch/", views.FetchCollectionsView.as_view(), name="fetch"),
]
