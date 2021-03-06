# Generated by Django 2.1.3 on 2018-12-03 13:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='allergens',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='dish',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0, 'Precio negativo no permitido')]),
        ),
    ]
