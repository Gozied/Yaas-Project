from django.db import models
from datetime import datetime, timedelta, timezone
from django.conf import settings



def get_deadline():
    return datetime.now(timezone.utc) + timedelta(seconds=10)

    

class Auction(models.Model):
    
    AUCTION_LIFECYCLE_CHOICES = [
        ("active", "Active"),
        ("banned", "Banned"),
        ("due", "Due"),
        ("resolved", "Resolved")
        
    ]
    CURRENCIES_CHOICES = [
        ('eur', 'EUR '),
        ('usd', 'USD'),
        ('gbp', 'GBP'),
        ('ngn', 'NGN')

    ]


    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='latest_bidder', default=1)
    bidders=models.ManyToManyField(settings.AUTH_USER_MODEL)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='seller', default=1)
    title = models.CharField(max_length=255)
    description=models.TextField()
    minimum_price = models.DecimalField(max_digits=7, decimal_places=2,default=1)
    price=models.DecimalField(max_digits=7, decimal_places=2)
    display_price=models.DecimalField(max_digits=7, decimal_places=2,default=0)
    deadline= models.DateTimeField(default=get_deadline)
    created_date= models.DateTimeField(auto_now_add=True)
    latest_bid_date_time= models.DateTimeField(auto_now=True)
    seller_total_bids =models.IntegerField(default=0)
    currency=models.CharField(max_length=3, choices= CURRENCIES_CHOICES, default='usd')
    status = models.CharField(
        max_length=8,
        choices=AUCTION_LIFECYCLE_CHOICES,
        default='active'
    )
    








