from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django import forms

from .models import *

############################## Forms
class NewAuction(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'image', 'opening_bid', 'category']

############################## Views
def index(request):
    return render(request, "auctions/index.html", {
        "auctions":Auction.objects.all()
    })

def categories(request):
    return render(request, "auctions/categories.html")

def listing(request, auction_id):
    # Renders a page for each specific auction
    auction = Auction.objects.get(pk=auction_id)
    return render(request, "auctions/listing.html", {
        "auction":auction
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def new(request):
    if request.method == "POST":

        # Get form data
        title = request.POST['title']
        description = request.POST['description']
        opening_bid = request.POST['opening_bid']
        #image = request.POST['image']

        new_auction = Auction(
            title=title, 
            description=description, 
            opening_bid=opening_bid, 
            #image=image
        )
        new_auction.save()

        return render(request, "auctions/listing.html", {
            "auction":new_auction
        })

    user = request.user
    return render(request, "auctions/new.html", {
        "user":user, "newauction":NewAuction()
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def watchlist(request):
    # Takes a logged in user to their watchlist page
    return render(request, "auctions/watchlist.html")
