# Generated by Django 2.1.4 on 2019-04-14 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('delete_status', models.BooleanField(default=False, verbose_name='deleted')),
                ('quantity', models.IntegerField(default=1, verbose_name='quantity')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='price')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('delete_status', models.BooleanField(default=False, verbose_name='deleted')),
                ('start_time', models.DateTimeField(verbose_name='start time')),
                ('end_time', models.DateTimeField(null=True, verbose_name='end time')),
                ('total_duration', models.IntegerField(null=True, verbose_name='total duration')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='total price')),
                ('status', models.CharField(default='booked', max_length=50, verbose_name='status')),
                ('note', models.TextField(null=True, verbose_name='booking note')),
                ('payment_status', models.CharField(default='pending', max_length=50, verbose_name='payment status')),
                ('payment_reference', models.CharField(max_length=100, null=True, verbose_name='payment reference')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('delete_status', models.BooleanField(default=False, verbose_name='deleted')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='price')),
                ('start_time', models.DateTimeField(verbose_name='start time')),
                ('duration', models.IntegerField(verbose_name='duration')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='sales.Orders')),
                ('pet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='customers.CustomerPets')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]