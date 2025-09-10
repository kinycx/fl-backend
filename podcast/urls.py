from django.urls import path

from .views import (
    BulkCreatePodcastView,
    PodcastListByCollectionCreateView,
    PodcastListCreatePaginatedView,
    PodcastRetrieveUpdateDestroyView,
    RandomPodcastView,
)

urlpatterns = [
    path("", PodcastListCreatePaginatedView.as_view(), name="podcast-list-create"),
    path(
        "collection/<str:collection>/",
        PodcastListByCollectionCreateView.as_view(),
        name="podcast-list-by-collection-create",
    ),
    path("bulk/", BulkCreatePodcastView.as_view(), name="podcast-bulk-create"),
    path("random/", RandomPodcastView.as_view(), name="podcast-random"),
    path(
        "<str:pk>/",
        PodcastRetrieveUpdateDestroyView.as_view(),
        name="podcast-retrieve-update-destroy",
    ),
]
