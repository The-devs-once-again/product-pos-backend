import json
from abc import ABC, abstractmethod

from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .view_config import GenericViewConfigLoader


class _ABCGenericView(ABC, GenericViewConfigLoader):
    """An abstract class that just inherits from the GenericViewConfigLoader"""


class UpdateViewInterface(ABC):
    def update(self, request, pk=None, look_query=None, partial=False):
        """Gets the object to be updated"""

    @abstractmethod
    def put(self, request, pk=None, look_query=None):
        """Updates the object fully"""

    @abstractmethod
    def patch(self, request, pk=None, look_query=None):
        """Updates an object partially"""

    @abstractmethod
    def delete(self, request, pk=None, look_query=None):
        """Deletes a single object"""


class CreateViewInterface(ABC):
    @abstractmethod
    def post(self, request):
        """Creates an object"""


class ListViewInterface(ABC):
    @abstractmethod
    def get(self, request):
        """Lists all the objects"""


class DetailViewInterface(ABC):
    @abstractmethod
    def get(self, request, query):
        """Gets a single object"""


class DeleteAllViewInterface(ABC):
    @abstractmethod
    def delete(self, request):
        """Deletes all objects"""


class UpdateView(_ABCGenericView, UpdateViewInterface):
    def _get_model_class(self, pk=None, lookup_query=None) -> models.Model:
        if lookup_query is not None:
            model_class = get_object_or_404(self.view_config.model, **lookup_query)

        else:
            model_class = get_object_or_404(self.view_config.model, pk=pk)

        return model_class

    def update(self, request, pk=None, lookup_query=None, partial=False):
        data = json.loads(request.body.decode('utf-8'))

        serializer = self.view_config.serializer_class(self._get_model_class(pk=pk, lookup_query=lookup_query),
                                                       data=data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def put(self, request, pk=None, lookup_query=None):
        return self.update(request, pk, lookup_query=lookup_query)

    def patch(self, request, pk=None, lookup_query=None):
        return self.update(request, pk, lookup_query=lookup_query, partial=True)

    def delete(self, request, pk=None, lookup_query=None):
        product_model = self._get_model_class(pk, lookup_query=lookup_query)
        product_model.delete()

        return JsonResponse({"message": self.view_config.delete_message})


class CreateView(_ABCGenericView, CreateViewInterface):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        serializer = self.view_config.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


class ListView(_ABCGenericView, ListViewInterface):
    def get(self, request):
        model_list = self.view_config.model.objects.all()
        serializer = self.view_config.serializer_class(model_list, many=True)

        return JsonResponse({self.view_config.response_name: serializer.data})


class DetailView(_ABCGenericView, DetailViewInterface):
    def get(self, request, query):
        model_detail = self.view_config.model.objects.get(**query)
        serializer = self.view_config.serializer_class(model_detail)

        return JsonResponse(serializer.data)


class DeleteAllView(_ABCGenericView, DeleteAllViewInterface):
    def delete(self, request):
        self.view_config.model.objects.all().delete()

        return JsonResponse({"message": self.view_config.delete_message})
