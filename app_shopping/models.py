from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class ProductModel(models.Model):
    category = models.CharField(max_length = 50, null = False, blank = False)
    name = models.CharField(max_length = 100, null = False, blank = False)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, null = False, blank = False)
    image = models.ImageField(upload_to='media/product_images', null = False, blank = False)
    description = models.TextField(max_length = 500, null = False, blank = False)

class Product(models.Model):
    category = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    discount = models.DecimalField(max_digits = 10, decimal_places = 2, null = False, blank = False)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, null = False, blank = False)
    img = models.ImageField(upload_to='media/product_images', null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)

class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.IntegerField()

    last_login = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return self.name