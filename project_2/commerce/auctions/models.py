from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Auction(models.Model):
    # Each Auction instance is an item listed for auction

    # User specified fields up front to create the auction
    title = models.CharField(max_length=64)
    description = models.TextField()
    opening_bid = models.DecimalField(max_digits=10,decimal_places=2)

    # Optional fields
    image = models.CharField(max_length=64,blank=True)
    category = models.CharField(max_length=64,blank=True)

    # User - a many to one....a user can create many auctions, but auction
    # may only have one user that created it
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    # Another one to many, but will start as blank
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default=None, 
    null=True, related_name='won')

    # For closing auctions
    LISTING_STATUS = (
        ("A",'Active'),
        ("C","Closed")
    )
    status = models.CharField(max_length=1, choices=LISTING_STATUS, default="A")

    # Watchlist...specify which users have this auction on their watchlist
    watchlist = models.ManyToManyField(User, blank=True, related_name='watchlist', 
    default=None)

    # current price...this will get calculated each time the field is generated?
    ### I don't think this is needed as a field. We can just display either the opening-bid
    ### or the highest of the current bids...and the error handling will be in the creation of a new bid

    def __str__(self):
        return self.title


class Bid(models.Model):
    # Each bid will have one user and one auction, but many bids can be associted with a user/auction
    # so both will be many to one relationships
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user}'s bid of ${self.amount} on {self.auction}"

class Comment(models.Model):
    # similiar to bids but with a text field 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self):
        return f"{self.user}'s comment #{self.id} on {self.auction}"


