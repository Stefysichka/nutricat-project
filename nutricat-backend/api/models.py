from django.db import models
from django.contrib.auth.models import User
class FoodProduct(models.Model):

    brand = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    food_type = models.CharField(max_length=20)
    calories_100g = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    protein_pct = models.DecimalField(max_digits=5, decimal_places=2)
    fat_pct = models.DecimalField(max_digits=5, decimal_places=2)
    fiber_pct = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):

        return f"{self.brand} - {self.product_name}"


class Cat(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cats')

    name = models.CharField(max_length=50)

    breed = models.CharField(max_length=50, blank=True, null=True)

    gender = models.CharField(max_length=10)
    birth_date = models.CharField(max_length=20) 
    weight_kg = models.DecimalField(max_digits=4, decimal_places=2)
    body_condition = models.CharField(max_length=20)
    activity_level = models.CharField(max_length=20)
    is_neutered = models.BooleanField(default=False)

    photo_url = models.TextField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    tips = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class CatRation(models.Model):

    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='rations')
    product = models.ForeignKey(FoodProduct, on_delete=models.CASCADE, related_name='rations')

    daily_portion_g = models.IntegerField()
    feeding_time = models.CharField(max_length=20)

    def __str__(self):

        return f"{self.cat.name} -> {self.product.product_name}"

class DietaryNorm(models.Model):

    factor_name = models.CharField(max_length=50)
    multiplier_value = models.DecimalField(max_digits=3, decimal_places=2)

