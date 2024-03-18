from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Customer(User):
    name = models.CharField(max_length=255)
    is_custom_admin = models.BooleanField(default=False)


    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50, default='cake')
    image = models.ImageField(upload_to='images/')

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        
    def get_absolute_url(self):
        return reverse("product", kwargs={"pk": self.pk})
    
    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={"product_id": self.pk})

    def __str__(self):
        return f"{self.name} - {self.type}  - {self.image}- Ksh{self.price}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def subtotal(self):
        return self.product.price 

    def __str__(self):
        return f"{self.product.name} (User: {self.user.name})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    shipping_address = models.CharField(max_length=255, default=0000)
    phone_number = models.CharField(max_length=20, default='')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                       default=0.0)
    created_at = models.DateTimeField(default=timezone.now)
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='pending')

    def __str__(self):
        return f"Order {self.pk} by {self.user.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
