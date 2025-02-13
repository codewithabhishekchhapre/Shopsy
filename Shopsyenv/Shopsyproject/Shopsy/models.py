from django.db import models
from django.contrib.auth.models import User
import string
import random
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)  # Store hashed password
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    productname = models.CharField(max_length=100)
    productprice = models.IntegerField(default=0)
    description = models.CharField(max_length=100)
    discount = models.IntegerField(default=0)
    create_date = models.DateField(auto_now=True)
    create_by = models.CharField(max_length=100)


    def _str_(self):
        return self.productname
    
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=50.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)

    # Address Details
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    house_no = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        self.total_price = (self.price * self.quantity) + self.delivery_charge
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"    
    
    
class OTP(models.Model):
    user_id = models.IntegerField()  
    mobile_number = models.CharField(max_length=15)  
    otp_code = models.CharField(max_length=6)  
    created_at = models.DateTimeField(auto_now_add=True)  # No default

    def generate_otp(self):
        """Generate a random 6-digit OTP"""
        otp = ''.join(random.choices(string.digits, k=6)) 
        return otp

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.otp_code = self.generate_otp()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.otp_code}"