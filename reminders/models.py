from django.db import models
from core.models import BaseModel
from companies.models import Company


class Reminders(BaseModel):
    company = models.ForeignKey(Company, related_name='auto_notifications', on_delete=models.CASCADE)
    name = models.CharField('name', max_length=100)
    subject = models.CharField('email subject', max_length=100)
    message = models.TextField('message')
    sent_before = models.BooleanField('sent before appointment', default=True)
    minutes = models.IntegerField('minutes before/after appointment', default=15)

