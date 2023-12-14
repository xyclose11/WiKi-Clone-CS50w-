from django.urls import path

from . import views

app_name="encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entryName>", views.display, name="display"),
    path("search/", views.search, name="search"),
    path("newEntry/", views.newentry, name="newEntry"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.save, name="save"),
    path("random/", views.randomentry, name="randomentry")
]
