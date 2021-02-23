from django.urls import path
# For redirecting the random page to the actual entry page
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("edit_entry_return", views.edit_entry_return, name="edit_entry_return"),
    path("testing", views.testing, name="testing"),
    path("<str:title>", views.page, name="page"),
]
