import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import views
from rest_framework import status
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer

# Create your views here.


class UpdateProductView(APIView):
    serializer_class = ProductSerializer

    def update(self, request, pk, partial=False):
        data = json.load(request.body.decode('utf-8'))

        product_model = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product_model, data=data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        product_model = get_object_or_404(Product, pk=pk)
        product_model.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


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
