from django.urls import path
# For redirecting the random page to the actual entry page
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("edit_page_return", views.edit_page_return, name="edit_page_return"),
    path("random", views.random, name="random"),
    path("<str:title>", views.page, name="page"),
]
