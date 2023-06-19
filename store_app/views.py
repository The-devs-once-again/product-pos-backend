from shared.base_views.generic_viewsets import GenericViewSet
from store_app.models import Order, Billing
from store_app.serializers import BillingSerializer, OrderSerializer

# Create your views here.
class OrderViewSet(GenericViewSet):
    """
    
    Order ModelViewSet
    
    """
    
    pk_field = 'order_id'

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class BillingViewSet(GenericViewSet):
    """
    
    Billing ModelViewSet
    
    """
    
    pk_field = 'ref_id'
    
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
