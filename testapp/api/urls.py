from django.urls import path
from .views import ActorAPIView

urlpatterns = [
    path('actor-list/', ActorAPIView.as_view())
]