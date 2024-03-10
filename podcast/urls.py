from django.urls import path
from .views import (
    PodcastListCreateView,
    PodcastRetrieveUpdateDestroyView,
    BulkCreatePodcastView,
)


urlpatterns = [
    path("", PodcastListCreateView.as_view(), name="podcast-list-create"),
    path("bulk/", BulkCreatePodcastView.as_view(), name="podcast-bulk-create"),
    path(
        "<str:pk>/",
        PodcastRetrieveUpdateDestroyView.as_view(),
        name="podcast-retrieve-update-destroy",
    ),
]
