from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FoodItem
from .forms import FoodEntryForm

# Create your views here.

class FoodItemCreateView(LoginRequiredMixin, CreateView):
    template_name = "foodEntry/createFood.html"
    form_class = FoodEntryForm
    queryset = FoodItem.objects.all()
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return redirect('home')
