from django.contrib import admin
from django.contrib.auth.models import User

from .models import ProductModel, Product, UserModel

# Register your models here.

admin.site.register(Product)
admin.site.register(UserModel)