from django.contrib.auth.models import User
from django.db import models

from product.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    size = models.CharField(max_length=100, default='Chose size')
    payment_type = models.CharField(max_length=100, default='Payment')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    stripe_token = models.CharField(max_length=100)
    INP = 'INPOST 48'
    ODB = 'ODBIÓR OSOBISTY'
    PAC = 'PACZKOMAT'
    TRIP_CHOICES = [
        ('INP', 'Inpost'),
        ('ODB', 'Odbiór'),
        ('PAC', 'Paczkomat')

    ]
    trip = models.CharField(
        max_length=10,
        choices=TRIP_CHOICES,
        default='None',
    )


    class Meta:
        ordering = ['-created_at',]
    
    def __str__(self):
        return self.first_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id