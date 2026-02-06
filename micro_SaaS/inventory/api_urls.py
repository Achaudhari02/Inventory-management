from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .api_views import (
    RegisterView,
    BusinessViewSet,
    ProductViewSet,
    StockTransactionViewSet,
)

router = DefaultRouter()
router.register(r'businesses', BusinessViewSet, basename='business')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='api-register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('', include(router.urls)),

    path(
        'businesses/<int:business_id>/products/',
        ProductViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='business-products-list'
    ),
    path(
        'businesses/<int:business_id>/products/<int:pk>/',
        ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
        name='business-products-detail'
    ),
    path(
        'businesses/<int:business_id>/transactions/',
        StockTransactionViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='business-transactions-list'
    ),
    path(
        'businesses/<int:business_id>/transactions/<int:pk>/',
        StockTransactionViewSet.as_view({'get': 'retrieve'}),
        name='business-transactions-detail'
    ),
]
