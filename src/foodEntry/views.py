from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import FoodItem
from .forms import FoodEntryForm

# Create your views here.


@login_required
@transaction.atomic
def createfooditem_View(request):
    if request.method == 'POST':
        food_form = FoodEntryForm(request.POST)
        if food_form.is_valid():
            profile = food_form.save(commit = False)
            profile.user = request.user
            profile.save()
            print(food_form.cleaned_data.get('date_added'))
            return redirect('homeView')
        else:
            print("ERROR IN SAVING FOOD ITEM")
    else:
        food_form = FoodEntryForm()
    return render(request, 'foodEntry/createFood.html', {'form': food_form})