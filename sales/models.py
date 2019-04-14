from django.db import models
from django.conf import settings

from core.models import BaseModel
from companies.models import Company
from inventory.models import ProductVariants, Products
from customers.models import Customers, CustomerPets
from services.models import Services


class Orders(BaseModel):
    company = models.ForeignKey(Company, related_name='orders', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, related_name='orders', on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time', null=True)
    total_duration = models.IntegerField('total duration', null=True)
    total_price = models.DecimalField('total price', max_digits=10, decimal_places=2, null=True)
    status = models.CharField('status', default='booked', max_length=50)
    note = models.TextField('booking note', null=True)
    payment_status = models.CharField('payment status', default='pending', max_length=50)
    payment_reference = models.CharField('payment reference', null=True, max_length=100)


class OrderServices(BaseModel):
    order = models.ForeignKey(Orders, related_name='services', on_delete=models.SET_NULL, null=True)
    pet = models.ForeignKey(CustomerPets, related_name='services', on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField('price', max_digits=10, decimal_places=2, null=True)
    start_time = models.DateTimeField('start time')
    duration = models.IntegerField('duration')
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='booked_services', null=True,
                              on_delete=models.SET_NULL)


class OrderProducts(BaseModel):
    order = models.ForeignKey(Orders, related_name='products', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(ProductVariants, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField('quantity', default=1)
    unit_price = models.DecimalField('price', max_digits=10, decimal_places=2, null=True)

    @property
    def total_price(self):
        return self.quantity * int(self.unit_price)
