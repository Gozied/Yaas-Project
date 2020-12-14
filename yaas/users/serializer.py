from rest_framework import serializers
from users.models import User
from yauctions.models import Auction



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model= User
        fields = '__all__'

class AuctionSerializer(serializers.ModelSerializer):

    class Meta:
        model= Auction
        fields = '__all__'
        read_only_fields = ['bidder','seller','deadline','latest_bid_date_time' ,'seller_total_bids','bidders','display_currency_value']