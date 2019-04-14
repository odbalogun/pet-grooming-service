from django.db import models
from django.conf import settings
from core.models import BaseModel


class Messages(BaseModel):
    subject = models.CharField('subject', max_length=200)
    message = models.TextField('message')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_emails',
                               on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_emails', on_delete=models.SET_NULL,
                                 null=True)
