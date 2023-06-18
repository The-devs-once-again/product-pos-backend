"""This file is responsible for making the generic views"""

import json
from rest_framework import mixins, status
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from shared.configs.view_config import GenericViewConfigLoader
from shared.interfaces.view_interface import (
    CreateViewInterface,
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
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    
    def put(self, request: Request, pk=None, lookup_query=None) -> Response:
        return self.update(request, pk=pk, lookup_query=lookup_query)

    def patch(self, request: Request, pk=None, lookup_query=None) -> Response:
        return self.update(request, pk=pk, lookup_query=lookup_query, partial=True)


class CreateView(GenericViewConfigLoader, CreateViewInterface):
    """Generic view that does creation of objects in the database"""

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        serializer = self.view_config.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class ListView(GenericViewConfigLoader, ListViewInterface):
    """Generic view that lists all objects in the database"""

    def get(self, request: Request) -> Response:
        model_list = self.view_config.model.objects.all()
        serializer = self.view_config.serializer_class(model_list, many=True)

        return Response({self.view_config.response_name: serializer.data})


class DetailView(GenericViewConfigLoader, DetailViewInterface):
    """Generic view that gets a single object in the database"""

    def get(self, request: Request, query: dict) -> Response:
        model_detail = self.view_config.model.objects.get(**query)
        serializer = self.view_config.serializer_class(model_detail)

        return Response(serializer.data)


class DeleteView(GenericViewConfigLoader, mixins.DestroyModelMixin):
    """Generic view that either accepts a single delete or deletes all instances"""

    def delete(self, request: Request) -> Response:
        delete_all = request.query_params.get('delete_all', 'false').lower() == 'true'

        if delete_all:
            # All objects deletion
            self.view_config.model.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # Single object deletion
            pk = request.query_params.get('pk')
            
            if pk is not None:
                self.view_config.model.objects.filter(pk=pk).delete()

                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)