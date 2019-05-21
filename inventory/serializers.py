from .models import ProductCategories, Products, ProductVariants
from companies.models import Company
from rest_framework import serializers


class ProductCategorySerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())

    class Meta:
        model = ProductCategories
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Products.objects.filter().all())
    product_name = serializers.StringRelatedField(many=False, read_only=True, source='product')

    class Meta:
        model = ProductVariants
        fields = ('id', 'name', 'quantity', 'retail_price', 'product', 'product_name')


class ProductSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                 queryset=Company.objects.all())
    category = serializers.PrimaryKeyRelatedField(many=False, read_only=False, required=True,
                                                  queryset=ProductCategories.objects.all())
    category_name = serializers.StringRelatedField(many=False, read_only=True, source='category')
    # variants = serializers.SerializerMethodField()
    variants = ProductVariantSerializer(many=True, required=True)
    image = serializers.ImageField(max_length=None, use_url=True, required=False)

    # @staticmethod
    # def get_variants(product):
    #     qs = ProductVariants.objects.filter(delete_status=False, product=product).all()
    #     serializer = ProductVariantSerializer(instance=qs, many=True)
    #     return serializer.data

    class Meta:
        model = Products
        fields = '__all__'
        depth = 2

