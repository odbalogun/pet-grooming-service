from django.db import models
from core.models import BaseModel
from companies.models import Company
import random
import string


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


class PetCategories(BaseModel):
    company = models.ForeignKey(Company, related_name='pet_categories', on_delete=models.CASCADE)
    name = models.CharField('name', max_length=50)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "id": self.pk,
            "name": self.name
        }


class CustomerPets(BaseModel):
    owner = models.ForeignKey(Customers, related_name='pets', on_delete=models.CASCADE)
    name = models.CharField('name', max_length=50)
    category = models.ForeignKey(PetCategories, related_name='pets', null=True, on_delete=models.SET_NULL)

    def to_json(self):
        return {
            "id": self.pk,
            "name": self.name,
            "category": self.category.to_json()
        }

