from django.urls import include, path
from testapp.api import urls

urlpatterns = [
    path('', include('testapp.api.urls'))
]