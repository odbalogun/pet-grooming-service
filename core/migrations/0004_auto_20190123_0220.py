# Generated by Django 2.1.4 on 2019-01-23 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190123_0217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='locations',
            old_name='name',
            new_name='location_name',
        ),
    ]
