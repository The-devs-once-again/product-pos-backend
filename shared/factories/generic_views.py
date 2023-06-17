"""This file is responsible for making the generic views"""

import json

from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.request import Request

from shared.configs.view_config import GenericViewConfigLoader
from shared.interfaces.view_interface import (
    CreateViewInterface,
    DeleteAllViewInterface,
    DetailViewInterface,
    ListViewInterface,
    UpdateViewInterface,
)


class UpdateView(GenericViewConfigLoader, UpdateViewInterface):
    """Generic view that does the update methods"""

    def _get_object(self, pk=None, lookup_query=None) -> models.Model:
        if lookup_query is not None:
            object = get_object_or_404(self.view_config.model, **lookup_query)

        else:
            object = get_object_or_404(self.view_config.model, pk=pk)

        return object

    def update(self, request: Request, pk=None, lookup_query=None, partial=False):
        data = request.data
        object_instance = self._get_object(pk=pk, lookup_query=lookup_query)
        context = {'request': request}
        serializer = self.view_config.serializer_class(object_instance, data=data,  # type: ignore
                    partial=partial, context=context)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors, status=400)

    def put(self, request: Request, pk=None, lookup_query=None):
        return self.update(request, pk, lookup_query=lookup_query)

    def patch(self, request: Request, pk=None, lookup_query=None):
        return self.update(request, pk, lookup_query=lookup_query, partial=True)

    def delete(self, request: Request, pk=None, lookup_query=None):
        model = self._get_object(pk, lookup_query=lookup_query)
        model.delete()

        return JsonResponse({"message": self.view_config.delete_message})


class CreateView(GenericViewConfigLoader, CreateViewInterface):
    """Generic view that does creation of objects in the database"""

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        serializer = self.view_config.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


class ListView(GenericViewConfigLoader, ListViewInterface):
    """Generic view that lists all objects in the database"""

    def get(self, request: Request) -> JsonResponse:
        model_list = self.view_config.model.objects.all()
        serializer = self.view_config.serializer_class(model_list, many=True)

        return JsonResponse({self.view_config.response_name: serializer.data})


class DetailView(GenericViewConfigLoader, DetailViewInterface):
    """Generic view that gets a single object in the database"""

    def get(self, request: Request, query: dict) -> JsonResponse:
        model_detail = self.view_config.model.objects.get(**query)
        serializer = self.view_config.serializer_class(model_detail)

        return JsonResponse(serializer.data)


class DeleteAllView(GenericViewConfigLoader, DeleteAllViewInterface):
    """Generic view that deletes all objects in the database"""

    def delete(self, request: Request) -> JsonResponse:
        self.view_config.model.objects.all().delete()

        return JsonResponse({"message": self.view_config.delete_message})
