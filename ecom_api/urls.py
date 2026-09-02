from django.contrib import admin
from django.urls import path, include, re_path
from .ecom_app import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter




urlpatterns = [
    path("admin/", admin.site.urls),
    #path("products/", views.product_list, name="product-list"),
    #path("products/<int:pk>/", views.product_detail, name="product-detail"),
    #path("products/create/", views.ProductCreateView.as_view(), name="product-create"),
    path("products/", views.ProductListCreateView.as_view(), name="product-list-create"),
    path("products/<int:product_id>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("products/info/", views.ProductInfoView.as_view(), name= "product-info"),
    #path("orders/", views.OrderListView.as_view(), name="order-list"),
    #path("users/orders/", views.UserOrderListView.as_view(), name = "user-order"),
    path('silk', include('silk.urls', namespace='silk')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api-auth/", include("rest_framework.urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('users/', views.UserListView.as_view(), name = "user-list"),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken'))

]

router = DefaultRouter()
router.register("orders", views.OrderViewSet)
#router.register("orderitems", views.OrderItemViewSet)

urlpatterns += router.urls


