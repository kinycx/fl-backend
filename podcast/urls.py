from django.urls import path
from .views import (
    PodcastListCreateView,
    PodcastRetrieveUpdateDestroyView,
    BulkCreatePodcastView,
    ServeAudioView,
    ServeRSSView,
)


urlpatterns = [
    path("", PodcastListCreateView.as_view(), name="podcast-list-create"),
    path("bulk/", BulkCreatePodcastView.as_view(), name="podcast-bulk-create"),
    path(
        "<str:pk>/",
        PodcastRetrieveUpdateDestroyView.as_view(),
        name="podcast-retrieve-update-destroy",
    ),
    path("podcast.rss", ServeRSSView.as_view(), name="serve_rss"),
    path("<str:filename>.mp3", ServeAudioView.as_view(), name="serve_audio"),
]
