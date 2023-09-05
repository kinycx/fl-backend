from django.urls import path
from .views.podcast import PodcastListCreateView, PodcastRetrieveUpdateDestroyView

urlpatterns = [
    path('', PodcastListCreateView.as_view(), name='podcast-list-create'),
    path('<int:pk>/', PodcastRetrieveUpdateDestroyView.as_view(), name='podcast-retrieve-update-destroy'),
]