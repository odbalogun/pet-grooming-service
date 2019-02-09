from django.db import models
from djmoney.models.fields import MoneyField
from django.conf import settings


class BaseModel(models.Model):
    """
    Base model. Other models will inherit from this
    """
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)

    class Meta:
        abstract = True


class Company(BaseModel):
    company_name = models.CharField('company name', max_length=200, null=False)
    description = models.TextField('description', null=True)
    website = models.CharField('website', max_length=100, null=True)
    contact_number = models.CharField('contact number', max_length=50, null=True)
    time_zone = models.CharField('time zone', max_length=100, null=True)
    country = models.CharField('country', max_length=100, null=True)
    groomer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="store", null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.company_name

    def __str__(self):
        return self.company_name


class Locations(BaseModel):
    company = models.ForeignKey(Company, related_name='locations', on_delete=models.CASCADE)
    location_name = models.CharField('location name', max_length=100)
    contact_number = models.CharField('contact number', max_length=50)
    contact_email = models.CharField('contact email', max_length=50)
    address = models.TextField('physical address')
    city = models.CharField('city', max_length=50)
    state = models.CharField('state', max_length=50)
    zip_code = models.CharField('zip code', max_length=50, null=True)


class ProductCategories(BaseModel):
    company = models.ForeignKey(Company, related_name='product_brands', on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    category_name = models.CharField('category name', max_length=50)


class Products(BaseModel):
    company = models.ForeignKey(Company, related_name='products', on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(ProductCategories, related_name='products', on_delete=models.CASCADE)
    barcode = models.CharField('barcode', max_length=50)
    name = models.CharField('product name', max_length=100)
    sku = models.CharField('sku', max_length=100)
    description = models.TextField('description')
    retail_price = MoneyField('retail price', max_digits=10, decimal_places=2, default_currency='USD')
    discount_price = MoneyField('discount price', null=True, max_digits=10, decimal_places=2, default_currency='USD')


class ServiceGroups(BaseModel):
    company = models.ForeignKey(Company, related_name='service_groups', on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    appointment_color = models.CharField('appointment color', max_length=50)
    name = models.CharField('group name', max_length=100)
    description = models.TextField('description')


class Services(BaseModel):
    company = models.ForeignKey(Company, related_name='services', on_delete=models.CASCADE)
    group = models.ForeignKey(ServiceGroups, related_name='services', on_delete=models.CASCADE)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_services', null=True, on_delete=models.SET_NULL)
    staff = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='services')
    name = models.CharField('group name', max_length=100)
    description = models.TextField('description')
