# Generated by Django 2.1.4 on 2019-02-23 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20190223_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='cancellation_limit',
            field=models.IntegerField(default=3, verbose_name='max_hours_to_cancellation'),
        ),
        migrations.AddField(
            model_name='company',
            name='hours_bookable_in_advance',
            field=models.IntegerField(default=3, verbose_name='min hours bookable in advance'),
        ),
        migrations.AddField(
            model_name='company',
            name='max_day_bookable_in_advance',
            field=models.IntegerField(default=10, verbose_name='max days bookable in advance'),
        ),
    ]