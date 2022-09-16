from unicodedata import category
from rest_framework import serializers, reverse

from core.models import Category, Product

class CategoriesSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('id', 'title', 'description')
        model = Category


class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('title','description', 'price')
        model = Product   