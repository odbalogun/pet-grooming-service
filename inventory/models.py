from django.db import models
from core.models import BaseModel
from companies.models import Company


class ProductCategories(BaseModel):
    company = models.ForeignKey(Company, related_name='product_brands', on_delete=models.CASCADE)
    category_name = models.CharField('category name', max_length=50)

    def __unicode__(self):
        return self.category_name

    def __str__(self):
        return self.category_name


class Products(BaseModel):
    company = models.ForeignKey(Company, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategories, related_name='products', on_delete=models.CASCADE)
    barcode = models.CharField('barcode', max_length=50, null=True)
    name = models.CharField('product name', max_length=100)
    sku = models.CharField('sku', max_length=100, null=True)
    description = models.TextField('description')
    image = models.ImageField(max_length=None, null=True, default='products/images/default-pro.jpg',
                              upload_to='products/images/')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class ProductVariants(BaseModel):
    product = models.ForeignKey(Products, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField('product name', max_length=100)
    barcode = models.CharField('barcode', max_length=50)
    sku = models.CharField('sku', max_length=100)
    quantity = models.IntegerField('quantity')
    retail_price = models.DecimalField('retail price', max_digits=10, decimal_places=2, null=True)

    def add_inventory_history(self, description, action, quantity):
        if action == 'sub':
            quantity = - quantity

        self.history.create(product_id=self.product_id, description=description, quantity=quantity)

    def to_json(self):
        return {
            "id": self.pk,
            "name": self.name,
            "barcode": self.barcode,
            "sku": self.sku,
            "quantity": self.quantity,
            "retail_price": self.retail_price
        }


class ProductStockHistory(BaseModel):
    product = models.ForeignKey(Products, related_name='history', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariants, related_name='history', on_delete=models.CASCADE)
    description = models.CharField('description', max_length=50)
    quantity = models.IntegerField('quantity')
