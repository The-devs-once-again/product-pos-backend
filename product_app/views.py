import json
from django.http import JsonResponse
from rest_framework import views
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer


# Create your views here.

class CreatProductView(APIView):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            product = serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


class ProductListView(APIView):
    def get(self, request):
        product_models = Product.objects.all()
        serializer = ProductSerializer(product_models, many=True)

        return JsonResponse({"products": serializer.data})


class ProductDetailView(APIView):
    def get(self, request, product_name):
        product_model = Product.objects.get(product_name=product_name)
        serializer = ProductSerializer(product_model)

        return JsonResponse({"product": serializer.data})
