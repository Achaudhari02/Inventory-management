from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

class Business(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="business"
    )

    class Meta: 
        constraints = [
            models.UniqueConstraint(
                fields= ["name"],
                name= "Unique name per business"
            )
        ]

    def __str__(self):
        return f"name: {self.name} created at: {self.created_at}"

alphaNumericValidator = RegexValidator(
    r'^[a-zA-Z0-9]+$',
    message="Only letters and numbers allowed"
)

class Product(models.Model):
    business = models.ForeignKey(
        Business, 
        on_delete=models.CASCADE,
        related_name="product"
    )
    name = models.CharField(max_length=100)
    sku = models.CharField(
        max_length=100,
        validators=[alphaNumericValidator]
    )
    category = models.CharField(max_length=100)
    current_quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=100)
    supplier_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"name: {self.name} current quantity: {self.current_quantity} category: {self.category}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields= ["business", "sku"],
                name = "unique_sku_per_business"
            )
        ]

class StockTransaction(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="transaction"
    )
    
    class InOutChoices(models.TextChoices):
        IN = "In"
        OUT = "Out"
    
    type = models.CharField(
        max_length=100,
        choices=InOutChoices.choices
        )
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"product: {self.product} type: {self.type} quantity: {self.quantity}"



