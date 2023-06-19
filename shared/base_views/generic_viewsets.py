"""This file is responsible for making generic or custom viewsets"""

from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response


class GenericViewSet(viewsets.ModelViewSet):
    """
    
    Custom ModelViewSet class that make the pk as string
    instead of the autofield id
    
    """
    
    pk_field = None

    def _get_lookup_field(self, pk) -> dict:
        return {self.pk_field: pk}

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        
        Equivalent of GET request wherein pk is a string. 
        This request is under the DETAIL route.
        
        """

        lookup_field = self._get_lookup_field(kwargs.get('pk'))
        
        try:
            instance = self.get_queryset().get(**lookup_field)
            serializer = self.get_serializer(instance)
            
            return Response(serializer.data)
        
        except self.queryset.model.DoesNotExist: # type: ignore
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        """
        
        Equivalent of patch PATCH request wherein pk is a string.
        This request is under DETAIL ROUTE

        """
        
        lookup_field = self._get_lookup_field(kwargs.get('pk'))
        
        try:
            instance = self.get_queryset().get(**lookup_field)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(serializer.data)
        
        except self.queryset.model.DoesNotExist: # type: ignore
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """
        
        Equivalent of DELETE request wherein pk is a string
        This request is under the DETAIL route.

        """

        lookup_field = self._get_lookup_field(kwargs.get('pk'))

        try:
            instance = self.get_queryset().get(**lookup_field)
            instance.delete()

            return Response({"message": "object removed"}, status=status.HTTP_200_OK)
        except self.queryset.model.DoesNotExist: # type: ignore
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def destroy_all(self, request: Request, *args, **kwargs) -> Response:
        """
        
        Equivalent of DELETE but for all objects of the model.
        This request is under the LIST route.
        
        """

        self.queryset.model.objects.all().delete() # type: ignore

        return Response({"message": "objects removed"}, status=status.HTTP_200_OK)