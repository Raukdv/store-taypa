from rest_framework import response, status, views
from core.models import Company, Product, Category
from ..serializers.categories import CategoriesSerializer, ProductsSerializer

class CategoriesView(views.APIView):
    serializer_class = CategoriesSerializer

    def get(self, request, *args, **kwargs):
        company = Company.objects.get(slug=kwargs['slug'])
        data = company.category_set.all()
        response_data = CategoriesSerializer(instance=data, many=True)

        return response.Response(response_data.data)

class ProductsView(views.APIView):
    serializer_class = ProductsSerializer

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(id=kwargs['id'])
        data = category.products.values()
        serializer = ProductsSerializer(instance=data, many=True)
        return response.Response(serializer.data)