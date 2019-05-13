from django.db import models
from django.conf import settings
import datetime
from core.models import BaseModel
import random
import string


class Company(BaseModel):
    company_name = models.CharField('company name', max_length=200, null=False)
    company_code = models.CharField('code', max_length=20)
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

    def __unicode__(self):
        return self.company_name

    def __str__(self):
        return self.company_name

    @property
    def groomer(self):
        return self.staff.filter(is_groomer=True).first()

    def generate_code(self, size=10):
        code = ''.join(random.choice(string.ascii_letters[26:] + string.digits) for i in range(size))
        if Company.objects.filter(company_code=code).exists():
            self.generate_code()
        self.company_code = code


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


class DatesClosed(models.Model):
    company = models.ForeignKey(Company, related_name='dates_closed', on_delete=models.CASCADE)
    closed_date = models.DateField('date closed', null=False)

    def to_json(self):
        return {
            "id": self.pk,
            "name": self.closed_date
        }


class DaysOff(models.Model):
    company = models.ForeignKey(Company, related_name='days_off', on_delete=models.CASCADE)
    day = models.CharField('day', null=False, max_length=20)

    def to_json(self):
        return {
            "id": self.pk,
            "day": self.day
        }


class BankAccountDetails(models.Model):
    company = models.ForeignKey(Company, related_name='bank_account_details', on_delete=models.CASCADE)
    account = models.CharField('account', max_length=50)
    account_name = models.CharField('account_name', max_length=50)
    account_type = models.CharField('account_type', max_length=50)
    bank_name = models.CharField('bank_name', max_length=100)
    country = models.CharField('country', max_length=50)
    last_four_digits = models.CharField('last_four_digits', max_length=10)
    routing_number = models.CharField('routing_number', max_length=50)