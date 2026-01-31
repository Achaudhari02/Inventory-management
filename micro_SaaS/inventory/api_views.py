from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Business, Product, StockTransaction
from .serializers import (
    UserSerializer,
    BusinessSerializer,
    ProductSerializer,
    StockTransactionSerializer
)


class RegisterView(generics.CreateAPIView):
    """User registration endpoint."""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class BusinessViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for businesses.
    Users can only access their own businesses.
    """
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Business.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for products within a business.
    Nested under /businesses/{business_id}/products/
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_business(self):
        business_id = self.kwargs.get('business_id')
        return get_object_or_404(Business, id=business_id, owner=self.request.user)

    def get_queryset(self):
        business = self.get_business()
        queryset = Product.objects.filter(business=business)

        # Support filtering
        search = self.request.query_params.get('search')
        category = self.request.query_params.get('category')

        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                sku__icontains=search
            ) | queryset.filter(
                supplier_name__icontains=search
            )

        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def perform_create(self, serializer):
        business = self.get_business()
        serializer.save(business=business)


class StockTransactionViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for stock transactions within a business.
    Nested under /businesses/{business_id}/transactions/

    Creating a transaction automatically updates product quantity:
    - type='In': increases product.current_quantity
    - type='Out': decreases product.current_quantity (validates sufficient stock)
    """
    serializer_class = StockTransactionSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']  # No PUT/DELETE for transactions

    def get_business(self):
        business_id = self.kwargs.get('business_id')
        return get_object_or_404(Business, id=business_id, owner=self.request.user)

    def get_queryset(self):
        business = self.get_business()
        queryset = StockTransaction.objects.filter(business=business).select_related('product')

        # Support filtering by type
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(type=transaction_type)

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        business = self.get_business()
        transaction = serializer.save(business=business)

        # Update product quantity
        product = transaction.product
        if transaction.type == 'In':
            product.current_quantity += transaction.quantity
        else:  # Out
            product.current_quantity -= transaction.quantity
        product.save()
