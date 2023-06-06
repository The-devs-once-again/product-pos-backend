import json
from dataclasses import dataclass
from typing import Optional, Type

from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.views import APIView


# API View Logic

@dataclass
class ViewLogic(APIView):
    serializer_class: Type[serializers.ModelSerializer]
    model: Type[models.Model]
    response_name: Optional[str] = None


@dataclass
class UpdateView(ViewLogic):
    def update(self, request, pk, partial=False):
        data = json.loads(request.body.decode('utf-8'))

        model_class = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer_class(model_class, data=data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def put(self, request, pk):
        return self.update(request, pk)

    def patch(self, request, pk):
        return self.update(request, pk, partial=True)

    def delete(self, request, pk):
        product_model = get_object_or_404(self.model, pk=pk)
        product_model.delete()

        return JsonResponse({"message": "Product deleted"})


@dataclass
class CreateView(ViewLogic):

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            model = serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


@dataclass
class ListView(ViewLogic):
    def get(self, request):
        model_list = self.model.objects.all()
        serializer = self.serializer_class(model_list, many=True)

        return JsonResponse({self.response_name: serializer.data})


@dataclass
class DetailView(ViewLogic):
    def get(self, request, query):
        model_detail = self.model.objects.get(**query)
        serializer = self.serializer_class(model_detail)

        return JsonResponse(serializer.data)