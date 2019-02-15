# Generated by Django 2.1.4 on 2019-02-15 11:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_services_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='services',
            name='name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='services',
            name='staff',
            field=models.ManyToManyField(blank=True, related_name='services', to=settings.AUTH_USER_MODEL),
        ),
    ]
