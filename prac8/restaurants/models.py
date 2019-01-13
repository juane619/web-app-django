from django.db import models

from pymongo import MongoClient

from django.core.validators import MinValueValidator


# Mongo
mongoClient = MongoClient('mongodb://localhost:27017/')
db = mongoClient['test']

rest_collec = db['restaurants']
district_collec = db['neighborhoods']

# Dish model


class Dish(models.Model):
    TYPES_COUSINE = (
        ('am', 'American'),
        ('br', 'British'),
        ('ca', 'Caribbean'),
        ('ch', 'Chinese'),
        ('es', 'Spanish')
    )
    name = models.CharField(max_length=50, blank=False, null=False)
    type_cousine = models.CharField(
        max_length=2, choices=TYPES_COUSINE, blank=False, null=False)
    allergens = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8, validators=[
                                MinValueValidator(0, "Precio negativo no permitido")])

    def __str__(self):
        return '{} {}'.format(self.name, self.price)


# Restaurant model
class RestaurantModel(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    location = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return 'name: {}, location: {}'.format(self.name, self.location)
