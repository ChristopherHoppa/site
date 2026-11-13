from django.urls import path
from . import views


urlpatterns = [

    
    path("", views.home, name="home"),
    path("portfolio/", views.portfolio, name="portfolio"),

    path(
        "get-started/",
        views.get_started,
        name="get_started",
    ),

    path(
        "collaborate/",
        views.collaborate,
        name="collaborate",
    ),

    path(
    "logo.png",
    views.public_logo,
    name="public_logo",
)

]