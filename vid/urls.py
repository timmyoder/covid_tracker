from django.urls import path
from vid.views import somerset, philly, home, king, kane, dupage, okc, cleveland

urlpatterns = [
    path("", home, name="home"),
    path("somerset/", somerset, name="somerset"),
    path("philly/", philly, name="philly"),
    path("king/", king, name="king"),
    path("kane/", kane, name="kane"),
    path("oklahoma/", okc, name="oklahoma"),
    path("dupage/", dupage, name="dupage"),
    path("cleveland/", cleveland, name="cleveland"),
]
