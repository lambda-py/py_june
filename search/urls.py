from django.urls import path

from search import views

app_name = "search"

urlpatterns = [
    path("", views.search, name="search"),
    path("header/", views.search_header, name="search_header"),
]
