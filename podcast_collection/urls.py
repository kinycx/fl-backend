from django.urls import path

from .views import PodcastCollectionListCreateView

urlpatterns = [
    path(
        "",
        PodcastCollectionListCreateView.as_view(),
        name="podcast-collection-list-create",
    )
]
