import stripe

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        productsList = []
        sizeList = []
        shipmentList = []
        paymentList = []
        stripe.api_key = settings.STRIPE_SECRET_KEY
        paid_amount = sum(
            item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
        ilosc = sum(item.get('quantity') for item in serializer.validated_data['items'])

        for item in serializer.validated_data['items']:
            sizeList.append(item.get('size'))
            productsList.append(f"{item.get('product').name} ({item.get('product').id}) - {item.get('size')} - {item.get('quantity')}")
            shipmentList.append(item.get('shipment'))
            paymentList.append(item.get('payment'))
        try:
            charge = stripe.Charge.create(
                amount=int(paid_amount * 100),
                currency='USD',
                description='Charge from Djackets',
                source=serializer.validated_data['stripe_token']
            )

            serializer.save(user=request.user, paid_amount=paid_amount, products=productsList, size=sizeList, ilosc=ilosc, payment=paymentList, shipment=shipmentList)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)