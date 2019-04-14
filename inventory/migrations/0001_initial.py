# Generated by Django 2.1.4 on 2019-04-14 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('delete_status', models.BooleanField(default=False, verbose_name='deleted')),
                ('category_name', models.CharField(max_length=50, verbose_name='category name')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_brands', to='companies.Company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('delete_status', models.BooleanField(default=False, verbose_name='deleted')),
                ('barcode', models.CharField(max_length=50, null=True, verbose_name='barcode')),
                ('name', models.CharField(max_length=100, verbose_name='product name')),
                ('sku', models.CharField(max_length=100, null=True, verbose_name='sku')),
                ('description', models.TextField(verbose_name='description')),
                ('image', models.ImageField(default='products/images/default-pro.jpg', null=True, upload_to='products/images/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='inventory.ProductCategories')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='companies.Company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductStockHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('delete_status', models.BooleanField(default=False, verbose_name='deleted')),
                ('description', models.CharField(max_length=50, verbose_name='description')),
                ('quantity', models.IntegerField(verbose_name='quantity')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='inventory.Products')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductVariants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('delete_status', models.BooleanField(default=False, verbose_name='deleted')),
                ('name', models.CharField(max_length=100, verbose_name='product name')),
                ('barcode', models.CharField(max_length=50, verbose_name='barcode')),
                ('sku', models.CharField(max_length=100, verbose_name='sku')),
                ('quantity', models.IntegerField(verbose_name='quantity')),
                ('retail_price', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='retail price')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='inventory.Products')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='productstockhistory',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='inventory.ProductVariants'),
        ),
    ]
