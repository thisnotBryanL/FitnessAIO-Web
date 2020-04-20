from django import forms
from .models import FoodItem

class FoodEntryForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = [
            "name",
            "calories",
            "protein",
            "fat",
            "carbohydrates",
            "time"
        ]