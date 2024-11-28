from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ('IN', 'In'),
        ('OUT', 'Out'),
    )

    product = models.ForeignKey(Product, related_name='movements', on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.movement_type} - {self.product.name} - {self.quantity} units"
