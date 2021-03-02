from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    # A category for types of auctions, users can create new ones
    category = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.category}'

class Auction(models.Model):
    # Each Auction instance is an item listed for auction
    
    # These are the ones a user would add up front to create the auction
    title = models.CharField(max_length=64)
    description = models.TextField()
    # Optional fields
    image = models.CharField(max_length=64, blank=True)
    category = models.ManyToManyField(Category, blank=True, related_name='auctions')
    
    # This is not an actual bid, but a "threshold" for allowable bids later on
    opening_bid = models.DecimalField(max_digits=10, decimal_places=2)
    
    # For whether a listing is active or closed
    LISTING_STATUS = (
        ("A", 'Active'),
        ("C", "Closed")
    )
    status = models.CharField(max_length=1, choices=LISTING_STATUS)
    
    # These will be inherited from other classes
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='auctions') 
    watchlist = models.ManyToManyField(User, blank=True, related_name='watchlist' )

    def __str__(self):
        return f'{self.title} listed by {self.user}'

class Bid(models.Model):
    # A record of every bid. Each bid needs:
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')

class Comment(models.Model):
    # Each comment is tied to exactly one auction and one user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
