"""This file is responsible for making custom routers"""

from rest_framework import routers
from rest_framework.routers import Route

class CRUDRouter(routers.SimpleRouter):
    """
    
    Custom router that defines the fundamental CRUD functions.
    
    """

    routes = [
        # Create route 
        Route(
            url=r'^{prefix}/create{trailing_slash}$',
            mapping={
                'post': 'create',
                'delete': 'destroy_all',
            },
            name='{basename}-create',
            detail=False,
            initkwargs={'suffix': 'Create'}
        ),
        # List route.
        Route(
            url=r'^{prefix}/list{trailing_slash}$',
            mapping={
                'get': 'list',
                'delete': 'destroy_all' 
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/detail/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
    ]