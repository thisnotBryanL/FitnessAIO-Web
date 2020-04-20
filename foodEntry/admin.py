from django.contrib import admin

# Register your models here.
from .models import FoodItem

admin.site.register(FoodItem)