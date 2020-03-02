from django.db import models
from registration.models import User
# Create your models here.
class FoodItem(models.Model):
    TIME_EATEN = [
        ('Breakfast','Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack','Snack')
    ]
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add=True)
    calories = models.DecimalField(max_digits=10000, decimal_places=1)
    protein = models.DecimalField(max_digits=10000, decimal_places=1)
    fat = models.DecimalField(max_digits=10000, decimal_places=1)
    carbohydrates = models.DecimalField(max_digits=10000, decimal_places=1)
    time = models.CharField(max_length = 200, choices = TIME_EATEN, null = True)

    def __str__(self):
        return self.name
