# Generated by Django 2.1.4 on 2019-03-09 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20190309_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderservices',
            name='duration',
            field=models.IntegerField(default=90, verbose_name='duration'),
            preserve_default=False,
        ),
    ]
