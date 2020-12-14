from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from datetime import datetime, timedelta, timezone
import pytz
from users.serializer import AuctionSerializer
from yauctions.models import Auction

class SameSellerException(APIException):
    status_code = 500
    default_detail = 'Seller cannot bid on own auction'
    default_code = 'seller_cannot_bid'

class WinningBidderException(APIException):
    status_code = 500
    default_detail = 'You cannot bid on an auction you"re already winning'
    default_code = 'winning_bidder_cannot_bid'


class BidTooLowException(APIException):
    status_code = 500
    default_detail = 'Current bid must be greater than previous bid'
    default_code = 'seller_cannot_bid_lesseer_amount'

class BannedAuctionException(APIException):
    status_code = 500
    default_detail = 'You cannot bid on a banned'
    default_code = 'can not bid banned auction'




class AuctionView(APIView):
    
    serializer_class = AuctionSerializer
    
    def get_auction(self, id):
        try:
            auction = Auction.objects.get(id= id)
            return auction
        except Auction.DoesNotExist:
            return

    def auction_conditions(self, request, id):
        
        instance=self.get_auction(id=id)
        
        if float(request.data["price"]) <=instance.price:
            raise BidTooLowException
        
        instance.seller = request.user
        if instance.seller==request.user:
            raise SameSellerException
        
        instance.bidder = request.user   
        if instance.bidder.id == int(request.user.id):
            raise WinningBidderException
        
        bid_time = datetime.now(timezone.utc)
        minutes_apart = instance.deadline - bid_time
        if (minutes_apart.seconds % 3600 / 60.0) <= 20:
            instance.deadline = instance.deadline + timedelta(minutes=5)
        
        instance.seller_total_bids=instance.seller_total_bids + 1
        user=request.user
        instance.bidders.add(user)
        instance.bidders.values_list()
        
        return instance

    
    def get(self, request, id):
        if not self.get_auction(id):
            Response('Auction Not Found in database', status=status.HTTP_404_NOT_FOUND)
        serializer = AuctionSerializer(self.get_auction(id))
        return Response(serializer.data)
    
    def put(self, request, id):
        instance=self.auction_conditions(request, id)
        serializer= AuctionSerializer(instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
       
    
    def delete(self, request, id):
        user=self.get_auction(id)
        user.delete()
        return Response("Auction deleted",status=status.HTTP_204_NO_CONTENT)

   


class CreateAndListAuctions(ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer

    def post(self, request):
        serializer =AuctionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
