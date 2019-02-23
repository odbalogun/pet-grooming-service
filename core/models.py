from django.db import models
from djmoney.models.fields import MoneyField
from django.conf import settings


class BaseModel(models.Model):
    """
    Base model. Other models will inherit from this
    """
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)
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
    cancellation_limit = models.IntegerField('max_hours_to_cancellation', default=3)
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


class DatesClosed(BaseModel):
    company = models.ForeignKey(Company, related_name='dates_closed', on_delete=models.CASCADE)
    closed_date = models.DateField('date closed', null=False)

