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
    calories = models.CharField(max_length=7)
    protein = models.CharField(max_length=5)
    fat = models.CharField(max_length=5)
    carbohydrates = models.CharField(max_length=5)
    time = models.CharField(max_length = 200, choices = TIME_EATEN, null = True)

    def __str__(self):
        return self.name
