# classy django for detailed in drf 

from rest_framework.decorators import api_view, parser_classes, action
from .models import Product, Order, OrderItem, User
from .serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer, OrderItemSerializer, OrderCreateSerializer, UserSerializer
from rest_framework.response import Response
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from .filters import ProductFilter, InStockFilter, OrderFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework import viewsets
from django.utils.decorators import method_decorator 
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from .tasks import send_order_confirmation_email


"""@api_view(["GET"])
def product_list(request):
    #products = Product.objects.all()
    products = Product.objects.filter(stock__gt = 0)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def product_detail(request,pk):
    product = Product.objects.get(pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)"""

"""@api_view(["POST"])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def product_create(request):
    serializer = ProductSerializer(data= request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status= 201)
    return Response(serializer.errors, status = 400)"""

"""class ProductCreateView(generics.CreateAPIView):
    model = Product
    serializer_class = ProductSerializer"""

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ("name", "price")
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "price"]
    throttle_scope = "products"
 
    """pagination_class = CursorPagination
    pagination_class.ordering = "id"  """


    pagination_class = None


    """pagination_class.default_limit = 5
    pagination_class.max_limit = 10
    pagination_class.offset_query_param = "subset" """


    """ pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.page_query_param = "page-num"
    pagination_class.page_size_query_param = "size-num"
    pagination_class.max_page_size = 12
    pagination_class.last_page_strings = "final"       """


    # @method_decorator(cache_page(60 * 15, key_prefix="product_list"))
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    

    # def get_queryset(self):
    #     import time
    #     time.sleep(2)
    #     return super().get_queryset()


    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


"""@api_view(["GET"])
def order_list(request):
    #orders = Order.objects.all()
    orders = Order.objects.prefetch_related("items", "items__product").all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data) """

"""class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer"""

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"

    def get_permissions(self):
        self.permission_classes == [AllowAny]
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    

"""  class OrderListView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer


class UserOrderListView(generics.ListAPIView):
    #queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return(Order.objects.filter(user= self.request.user).prefetch_related("items__product"))  """




"""@api_view(["GET"])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({"products":products, "count": len(products),
                                         "max_price": products.aggregate(max_price = Max("price"))["max_price"]})
    return Response(serializer.data)"""



class ProductInfoView(APIView):
    def get(self, request, format = None):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({"products":products, "count": len(products),
                                         "max_price": products.aggregate(max_price = Max("price"))["max_price"]})
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer 
    permission_classes = [IsAuthenticated]
    pagination_class = None
    #pagination_class.page_query_param = "page_size"

    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]
    throttle_scope = "orders"
    
    @method_decorator(cache_page(60 * 15, key_prefix = "order_list"))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs 
    
    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return OrderCreateSerializer
        return super().get_serializer_class()
    
    
    def perform_create(self, serializer):
        order = serializer.save(user = self.request.user)
        send_order_confirmation_email.delay(order.order_id, self.request.user.email)


    """@action(methods=["GET"], url_path = "user-orders", detail = False)
     def user_order(self, request):
        orders = self.get_queryset().filter(user= request.user)
        serializer = self.get_serializer(orders, many = True)
        return Response(serializer.data)   """ 



"""class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all() """

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
