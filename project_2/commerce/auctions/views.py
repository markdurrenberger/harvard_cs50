from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django.forms import ModelForm

from .models import User, Auction, Bid, Comment

################### Forms
class NewAuction(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'image', 'opening_bid', 'category']

class NewBid(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

class NewComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

################### Views
def index(request):
    prices = []
    
    auctions = Auction.objects.filter(status="A")
    for auction in auctions:
        
        price_dict =  Bid.objects.filter(auction__title=auction.title).aggregate(Max('amount'))
        
        if price_dict['amount__max'] is None:
            prices.append(auction.opening_bid)
        else:
            prices.append(price_dict['amount__max'])

    auction_zip = zip(auctions, prices)

    return render(request, "auctions/index.html", {
        'auctions':auction_zip
    })

# for displaying auction's listing page
def listing(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    price = Bid.objects.filter(auction__title=auction.title).aggregate(Max('amount'))
    comments = Comment.objects.filter(auction__title=auction.title)
    watchlist = Auction.objects.filter(watchlist=request.user)

    if price['amount__max'] is None:
        res = (auction, auction.opening_bid)
    else:
        res = (auction, price['amount__max'])

    return render(request, "auctions/listing.html", {
        "auction":res,
        "newbid":NewBid(), 
        "user":request.user,
        "comments":comments,
        "newcomment":NewComment(),
        "watchlist":watchlist
    })

# for creating a new auction
@login_required
def new(request):
    if request.method == "POST":
        # Get form data
        title = request.POST['title']
        description = request.POST['description']
        opening_bid = request.POST['opening_bid']
        user = request.user

        category = request.POST['category']
        image = request.POST['image']

        new_auction = Auction(
            title=title, description=description, opening_bid=opening_bid,
            user=user, status="A", category=category, image=image
        )

        new_auction.save()

        res = (new_auction,new_auction.opening_bid)

        return render(request, "auctions/listing.html",{
            "auction":res
        })
    user = request.user
    return render(request, "auctions/new.html", {
        "user":user, "newauction":NewAuction()
    })

# for creating a new bid
@login_required
def bid(request):
    if request.method == "POST":
        amount = request.POST['amount']
        user = request.user
        auction_id = request.POST['auction']
        bid_error = False

        auction = Auction.objects.filter(pk=auction_id).first()
        # Get the minimum bid (aka current price)
        price = Bid.objects.filter(auction__title=auction.title).aggregate(Max('amount'))
        if price['amount__max'] is None:
            min_bid = auction.opening_bid
        else:
            min_bid = price['amount__max']

        # If bid is above the min, save it and render page with that as current price
        if float(amount) > float(min_bid):
            new_bid = Bid(
                user=user,
                auction=auction,
                amount=amount
            )

            new_bid.save()

            res = (auction, new_bid.amount)

        # Otherwise, render the page with the old price and an error message
        else:
            bid_error = True

            if price['amount__max'] is None:
                res = (auction, auction.opening_bid)
            else:
                res = (auction, price['amount__max'])

        comments = Comment.objects.filter(auction__title=auction.title)
        watchlist = Auction.objects.filter(watchlist=request.user)
        return render(request, "auctions/listing.html",{
            "auction":res,
            "newbid":NewBid(),
            "comments":comments,
            "newcomment":NewComment(),
            "user":request.user,
            "watchlist":watchlist,
            "bid_error":bid_error
        })

@login_required
def comment(request):
    if request.method == "POST":
        user = request.user
        auction_id = request.POST['auction']
        text = request.POST['text']

        auction = Auction.objects.filter(pk=auction_id).first()

        new_comment = Comment(
            user=user,
            text=text,
            auction=auction
            )

        new_comment.save()

        comments = Comment.objects.filter(auction__title=auction.title)
        price = Bid.objects.filter(auction__title=auction.title).aggregate(Max('amount'))
        watchlist = Auction.objects.filter(watchlist=request.user)
        if price['amount__max'] is None:
            res = (auction, auction.opening_bid)
        else:
            res = (auction, price['amount__max'])

        return render(request, "auctions/listing.html", {
            "auction":res,
            "newbid":NewBid(),
            "newcomment":NewComment(),
            "comments":comments,
            "watchlist":watchlist
        })

# for closing a listing
@login_required
def close(request):
    
    if request.method == "POST":
        auction_id = request.POST['auction']
        auction = Auction.objects.filter(pk=auction_id).first()

        # change the status to "C"
        auction.status = "C"
        
        # Find the high bid and make that user the winner of the auction
        try:
            max_bid = Bid.objects.filter(auction=auction).order_by('-amount')[0]
            winner = max_bid.user
        # If list of bids are empty...no one wins
        except IndexError:
            winner = None
        
        auction.winner = winner

        auction.save()

    price = Bid.objects.filter(auction__title=auction.title).aggregate(Max('amount'))

    if price['amount__max'] is None:
        res = (auction, auction.opening_bid)
    else:
        res = (auction, price['amount__max'])

    return render(request, "auctions/listing.html", {
        "auction":res,
        "user":request.user
    } )

@login_required
def add_watchlist(request):
    if request.method == "POST":
        user = request.user
        auction_id = request.POST['auction']
        auction = Auction.objects.filter(pk=auction_id).first()
        
        auction.watchlist.add(user)

        price = Bid.objects.filter(auction__title=auction.title).aggregate(Max('amount'))
        if price['amount__max'] is None:
            res = (auction, auction.opening_bid)
        else:
            res = (auction, price['amount__max'])

        comments = Comment.objects.filter(auction__title= auction.title)
        watchlist = Auction.objects.filter(watchlist=request.user)

# need to bring in all the 
    return render(request, "auctions/listing.html", {
        "auction":res,
        "comments":comments,
        "watchlist":watchlist,
        "newbid":NewBid(),
        "newcomment":NewComment()
    })

@login_required
def watchlist(request):
    user = request.user

    auctions = Auction.objects.filter(watchlist=user)
    prices = []

    for auction in auctions:
        
        price_dict =  Bid.objects.filter(auction__title=auction.title).aggregate(Max('amount'))
        
        if price_dict['amount__max'] is None:
            prices.append(auction.opening_bid)
        else:
            prices.append(price_dict['amount__max'])

    auction_zip = zip(auctions, prices)

    return render(request, "auctions/watchlist.html", {
        "auctions":auction_zip
    })

def category(request, category):
    ### This returns the page that lists all the auctions in a given category
    auctions = Auction.objects.filter(category=category).filter(status="A")
    prices = []

    for auction in auctions:
        
        price_dict =  Bid.objects.filter(auction__title=auction.title).aggregate(Max('amount'))
        
        if price_dict['amount__max'] is None:
            prices.append(auction.opening_bid)
        else:
            prices.append(price_dict['amount__max'])

    auction_zip = zip(auctions, prices)

    return render(request, "auctions/category.html", {
        "category":category.title(), "auctions":auction_zip
    })


def categories(request):
    ### This returns the categories page (listing all the possible categories)
    categories = Auction.objects.all().values_list('category', flat=True)

    cats = [x for x in categories if x !='']
    cats = set(cats)
        

    return render(request, "auctions/categories.html", {
        "categories":cats
    })



####### Below here were part of file download for login/out
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
