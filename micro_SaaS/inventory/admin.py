from django.contrib import admin
from .models import Business, Product, StockTransaction

# Register your models here.
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")
    list_filter = ("owner__username",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "business", "current_quantity"]
    list_filter = ["business","category"]
    search_fields = ["name"]

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ["product", "type", "quantity"]
    list_filter = ["type"]
    search_fields = ["product"]
