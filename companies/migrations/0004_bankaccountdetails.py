# Generated by Django 2.1.4 on 2019-04-19 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_remove_company_groomer'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccountDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=50, verbose_name='account')),
                ('account_name', models.CharField(max_length=50, verbose_name='account_name')),
                ('account_type', models.CharField(max_length=50, verbose_name='account_type')),
                ('bank_name', models.CharField(max_length=100, verbose_name='bank_name')),
                ('country', models.CharField(max_length=50, verbose_name='country')),
                ('last_four_digits', models.CharField(max_length=10, verbose_name='last_four_digits')),
                ('routing_number', models.CharField(max_length=50, verbose_name='routing_number')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_account_details', to='companies.Company')),
            ],
        ),
    ]
