from django.urls import path
from vid.views import somerset, philly, home

urlpatterns = [
    path("", home, name="home"),
    path("somerset/", somerset, name="somerset"),
    path("philly/", philly, name="philly"),
]
