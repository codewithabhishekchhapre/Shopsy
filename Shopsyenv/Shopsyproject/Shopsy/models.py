from django.db import models

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