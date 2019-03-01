from django.db import models
from djmoney.models.fields import MoneyField
from django.conf import settings
import datetime
import random
import string
from django.core.serializers.json import DjangoJSONEncoder


class BaseModel(models.Model):
    """
    Base model. Other models will inherit from this
    """
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)
    is_active = models.BooleanField('active', default=True)
    delete_status = models.BooleanField('deleted', default=False)

    class Meta:
        abstract = True


class Company(BaseModel):
    company_name = models.CharField('company name', max_length=200, null=False)
    description = models.TextField('description', null=True)
    website = models.CharField('website', max_length=100, null=True)
    contact_number = models.CharField('contact number', max_length=50, null=True)
    time_zone = models.CharField('time zone', max_length=100, null=True)
    time_slot_interval = models.IntegerField('time slot interval', default=15)
    country = models.CharField('country', max_length=100, null=True)
    hours_bookable_in_advance = models.IntegerField('min hours bookable in advance', default=3)
    max_day_bookable_in_advance = models.IntegerField('max days bookable in advance', default=10)
    cancellation_limit = models.IntegerField('max hours to cancellation', default=3)
    opening_time = models.TimeField('daily opening time', default=datetime.time(9, 00))
    closing_time = models.TimeField('daily closing time', default=datetime.time(17, 00))
    groomer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="store", null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.company_name

    def __str__(self):
        return self.company_name


class Locations(BaseModel):
    company = models.ForeignKey(Company, related_name='locations', on_delete=models.CASCADE)
    staff = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='locations', blank=True)
    location_name = models.CharField('location name', max_length=100)
    contact_number = models.CharField('contact number', max_length=50)
    contact_email = models.CharField('contact email', max_length=50)
    address = models.TextField('physical address')
    city = models.CharField('city', max_length=50)
    state = models.CharField('state', max_length=50)
    zip_code = models.CharField('zip code', max_length=50, null=True)


class ProductCategories(BaseModel):
    company = models.ForeignKey(Company, related_name='product_brands', on_delete=models.CASCADE)
    category_name = models.CharField('category name', max_length=50)


class Products(BaseModel):
    company = models.ForeignKey(Company, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategories, related_name='products', on_delete=models.CASCADE)
    barcode = models.CharField('barcode', max_length=50, null=True)
    name = models.CharField('product name', max_length=100)
    sku = models.CharField('sku', max_length=100, null=True)
    description = models.TextField('description')
    retail_price = MoneyField('retail price', max_digits=10, decimal_places=2, default_currency='USD')


class ProductVariants(BaseModel):
    product = models.ForeignKey(Products, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField('product name', max_length=100)
    barcode = models.CharField('barcode', max_length=50)
    sku = models.CharField('sku', max_length=100)
    quantity = models.IntegerField('quantity')
    retail_price = MoneyField('retail price', max_digits=10, decimal_places=2, default_currency='USD')

    def add_inventory_history(self, description, action, quantity):
        if action == 'sub':
            quantity = - quantity

        self.history.create(product_id=self.product_id, description=description, quantity=quantity)

    def to_json(self):
        return {
            "id": self.pk,
            "name": self.name,
            "barcode": self.barcode,
            "sku": self.sku,
            "quantity": self.quantity,
            "retail_price": self.retail_price.amount
        }


class ProductStockHistory(BaseModel):
    product = models.ForeignKey(Products, related_name='history', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariants, related_name='history', on_delete=models.CASCADE)
    description = models.CharField('description', max_length=50)
    quantity = models.IntegerField('quantity')


class ServiceGroups(BaseModel):
    company = models.ForeignKey(Company, related_name='service_groups', on_delete=models.CASCADE)
    appointment_color = models.CharField('appointment color', max_length=50)
    name = models.CharField('group name', max_length=100)
    description = models.TextField('description')


class Services(BaseModel):
    company = models.ForeignKey(Company, related_name='services', on_delete=models.CASCADE)
    group = models.ForeignKey(ServiceGroups, related_name='services', on_delete=models.CASCADE)
    staff = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='services', blank=True)
    name = models.CharField('name', max_length=100)
    description = models.TextField('description')
    duration = models.IntegerField('duration (in mins)', default=15)
    price = MoneyField('price', max_digits=10, decimal_places=2, default_currency='USD')


class DatesClosed(BaseModel):
    company = models.ForeignKey(Company, related_name='dates_closed', on_delete=models.CASCADE)
    closed_date = models.DateField('date closed', null=False)


class AutoNotifications(BaseModel):
    company = models.ForeignKey(Company, related_name='auto_notifications', on_delete=models.CASCADE)
    name = models.CharField('name', max_length=100)
    subject = models.CharField('email subject', max_length=100)
    message = models.TextField('message')
    sent_before = models.BooleanField('sent before appointment', default=True)
    minutes = models.IntegerField('minutes before/after appointment', default=15)


class Customers(BaseModel):
    company = models.ForeignKey(Company, related_name='clients', on_delete=models.CASCADE)
    first_name = models.CharField('first name', max_length=100)
    last_name = models.CharField('last name', max_length=100)
    customer_code = models.CharField('customer', max_length=50)
    email = models.CharField('email', max_length=100)
    phone_number = models.CharField('phone number', max_length=50)

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def generate_code(self, size=5):
        code = ''.join(random.choice(string.ascii_letters[26:] + string.digits) for i in range(size))
        if Customers.objects.filter(customer_code=code).exists():
            self.generate_code()
        self.customer_code = code


class CustomerPets(BaseModel):
    owner = models.ForeignKey(Customers, related_name='pets', on_delete=models.CASCADE)
    name = models.CharField('name', max_length=50)
    pet_type = models.CharField('type', max_length=50)

    def to_json(self):
        return {
            "id": self.pk,
            "name": self.name,
            "pet_type": self.pet_type
        }


class Bookings(BaseModel):
    company = models.ForeignKey(Company, related_name='bookings', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, related_name='bookings', on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    total_duration = models.IntegerField('total duration')
    total_price = MoneyField('total price', max_digits=10, decimal_places=2, default_currency='USD')
    status = models.CharField('status', default='booked', max_length=50)
    payment_status = models.CharField('payment status', default='pending', max_length=50)
    payment_reference = models.CharField('payment reference', null=True, max_length=100)


class BookingPets(BaseModel):
    booking = models.ForeignKey(Bookings, related_name='pets', on_delete=models.SET_NULL, null=True)
    pet = models.ForeignKey(CustomerPets, on_delete=models.SET_NULL, null=True)


class BookingServices(BaseModel):
    booking = models.ForeignKey(Bookings, related_name='services', on_delete=models.SET_NULL, null=True)
    pet = models.ForeignKey(BookingPets, related_name='services', on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True)


class BookingProducts(BaseModel):
    booking = models.ForeignKey(Bookings, related_name='products', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(ProductVariants, on_delete=models.SET_NULL, null=True)
