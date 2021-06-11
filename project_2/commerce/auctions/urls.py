from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:auction_id>", views.listing, name="listing"),
    path("new", views.new, name="new"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("bid", views.bid, name="bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("close", views.close, name="close"),
    path("add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("comment", views.comment, name="comment"),
    path("<str:category>", views.category, name="category")
]
