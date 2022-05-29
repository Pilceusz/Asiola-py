import stripe

import smtplib
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from django.core.mail import send_mail
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
            productsList.append(
                f"Nazwa:{item.get('product').name} ID:({item.get('product').id}) - Rozmiar:{item.get('size')} - Ilość:{item.get('quantity')}")
            shipmentList.append(item.get('shipment'))
            paymentList.append(item.get('payment'))

        try:
            stripe.Charge.create(
                amount=int(paid_amount * 100),
                currency='PLN',
                description='Płatność Asiolabutik',
                source=serializer.validated_data['stripe_token']
            )

            serializer.save(user=request.user, paid_amount=paid_amount, products=productsList, size=sizeList,
                            ilosc=ilosc, payment=paymentList, shipment=shipmentList)

            sending_mail(productsList, shipmentList, serializer, request.user, paid_amount, paymentList)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def sending_mail(product, shipment, serializer, user, paid_amount, payment):
    send_mail('Zamówienie',
              f"Zarejestrowano nowe zamówienie.#{{ order.id }} \n"
              f"Produkt: {product} \n"
              f"Sposób dostawy: {shipment[0]} \n"
              f"Imie: {serializer.validated_data['first_name']} \n"
              f"Nazwisko: {serializer.validated_data['last_name']} \n"
              f"E-mail: {serializer.validated_data['email']} \n"
              f"Adre: {serializer.validated_data['address']} \n"
              f"Kod pocztowy: {serializer.validated_data['zipcode']} \n"
              f"Miasto: {serializer.validated_data['place']} \n"
              f"Telefon: {serializer.validated_data['phone']} \n"
              f"Użytkownik: {user} \n"
              f"Kwota: {paid_amount} \n"
              f"Sposób płatności: {payment[0]} \n",
              'asiolabutikpl@gmail.com',
              ['asiolabutikpl@gmail.com'],
              fail_silently=False)


class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
