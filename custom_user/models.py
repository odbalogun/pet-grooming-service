from django.utils.timezone import localtime, timedelta
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from core.models import Company
from util import random_string, send_mail

from .managers import UserManager
import datetime
import hashlib


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=100)
    last_name = models.CharField('last name', max_length=100)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    is_groomer = models.BooleanField('is groomer', default=False)
    is_staff = models.BooleanField('is staff', default=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='staff', null=True)
    delete_status = models.BooleanField('deleted', default=False)
    activation_key = models.CharField(max_length=400, null=True)
    key_expires = models.DateTimeField(null=True)
    password_reset_key = models.CharField(max_length=400, null=True)
    password_key_expires = models.DateTimeField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject=subject, message=message, to=self.email)

    def generate_activation_key(self):
        self.activation_key = hashlib.sha512("{}{}".format(self.email, random_string(10)).encode("utf8")).hexdigest()
        self.key_expires = localtime() + timedelta(days=1)

    def generate_password_request_key(self):
        self.password_reset_key = hashlib.sha512("{}{}".format(self.email, random_string(10)).encode("utf8"))\
            .hexdigest()
        self.password_key_expires = localtime() + timedelta(days=1)
