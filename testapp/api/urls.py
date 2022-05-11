from django.urls import path
from .views import ActorAPIView, MovieAPIView

urlpatterns = [
    path('actor-list/', ActorAPIView.as_view()),
    path('actor-list/<int:pk>/', ActorAPIView.as_view()),
    path('movie-list/', MovieAPIView.as_view()),
]