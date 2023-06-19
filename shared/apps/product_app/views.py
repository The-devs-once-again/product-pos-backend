from shared.apps.product_app.models import Product
from shared.apps.product_app.serializers import ProductSerializer

from shared.base_views.generic_viewsets import GenericViewSet


# Create your views here.
class ProductViewSet(GenericViewSet):
    """
    
    Product ModelViewSet 

    """

    pk_field = 'product_name'

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
