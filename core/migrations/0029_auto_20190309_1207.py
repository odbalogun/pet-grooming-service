# Generated by Django 2.1.4 on 2019-03-09 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20190309_0110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderservices',
            old_name='staff_id',
            new_name='staff',
        ),
    ]
