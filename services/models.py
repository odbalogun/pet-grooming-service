from django.db import models
from core.models import BaseModel
from companies.models import Company
from django.conf import settings


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
    price = models.DecimalField('price', max_digits=10, decimal_places=2)

    @property
    def staff_details(self):
        data = []

        for x in self.staff.all():
            data.append(x.to_json())
        return data

