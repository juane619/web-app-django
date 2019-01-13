from django.contrib import admin
from .models import Dish, RestaurantModel

# Register your models here.
admin.site.register([Dish, RestaurantModel])
