# Generated by Django 2.1.4 on 2019-04-14 00:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
        ('companies', '0002_auto_20190414_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='staff',
            field=models.ManyToManyField(blank=True, related_name='services', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='servicegroups',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_groups', to='companies.Company'),
        ),
    ]
