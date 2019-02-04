from django.db import models
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

