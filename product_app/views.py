from rest_framework.views import APIView
from api_logic.view_logic import UpdateView, ListView, DetailView, CreateView
from .models import Product
from .serializers import ProductSerializer

# Create your views here.


class UpdateProductView(APIView):
    update_product_view = UpdateView(
        serializer_class=ProductSerializer,
        model=Product,
        delete_message="Product deleted"
    )

    def update(self, request, pk, partial=False):
        self.update_product_view.update(request=request, pk=pk, partial=partial)

    def put(self, request, pk):
        return self.put(request, pk)

    def patch(self, request, pk):
        return self.update_product_view.patch(request=request, pk=pk)

    def delete(self, request, pk):
        return self.update_product_view.delete(request=request, pk=pk)


class CreatProductView(APIView):
    create_product_view = CreateView(
        serializer_class=ProductSerializer,
        model=Product
    )

    def post(self, request):
        return self.create_product_view.post(request=request)


class ProductListView(APIView):
    product_list_view = ListView(
        model=Product,
        serializer_class=ProductSerializer,
        response_name="products"
    )

    def get(self, request):
        return self.product_list_view.get(request=request)


class ProductDetailView(APIView):
    product_detail_view = DetailView(
        serializer_class=ProductSerializer,
        model=Product,
    )

    def get(self, request, product_name):
        query_params = {"product_name": product_name}

        return self.product_detail_view.get(request=request, query=query_params)

