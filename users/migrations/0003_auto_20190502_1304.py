# Generated by Django 2.1.4 on 2019-05-02 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190502_0042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_google_signup',
        ),
        migrations.AddField(
            model_name='user',
            name='google_id',
            field=models.CharField(max_length=100, null=True, verbose_name='google id'),
        ),
    ]
