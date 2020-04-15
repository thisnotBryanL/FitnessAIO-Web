from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction
from django.utils import timezone

from calculator.calcFuncs import macroCalc, calcRemainCalories
from.models import Profile
from foodEntry.models import FoodItem

from django.views.generic import(
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)
from .forms import SignUpForm, EditCaloriesForm
from .models import Profile

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html', {})
    else:
        profile = request.user.profile
        macros = dict()
        macros = macroCalc(float(profile.weight),'average',float(profile.calories))

        #Query Set that retrieves the 5 most recent food items entered
        last_5Food = FoodItem.objects.filter(user=profile.user).order_by('-date_added')[:5]
                
        #Queries food items only for the current day
        queryset = FoodItem.objects.filter(
            date_added__date=timezone.now().date())

        #Calculator to calculate the remaining calories left after querying food consumed for the day
        calsFromFood = calcRemainCalories(queryset, profile.calories,macros['protein'], macros['fat'], macros['carbs'])
        print(calsFromFood)
        
        context = {
            "userProfile" : profile,
            "carbs" : macros['carbs'],
            "fats" : macros['fat'],
            "protein" : macros['protein'],
            "last5Food" : last_5Food,
            "caloriesRemain" : calsFromFood['calsRemain'],
            "proteinRemain" : calsFromFood['proteinRemain'],
            "fatRemain" : calsFromFood['fatRemain'],
            "carbsRemain" : calsFromFood['carbsRemain']
        }
        return render(request, 'home.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('registration:update-calories')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def logout_requestView(request):
    logout(request)
    return redirect('homeView')

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST, instance=request.user)
        profile_form = EditCaloriesForm(
            request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, (
                'Your profile was successfully updated!'))
            return redirect('homeView')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = SignUpForm(instance=request.user)
        profile_form = EditCaloriesForm(instance=request.user.profile)
    return render(request, 'registration/updateProfile.html', {
        'user_form': user_form,
        'profile_form' : profile_form
    })


@login_required
@transaction.atomic
def update_calories(request):
    if request.method == 'POST':
        profile_form = EditCaloriesForm(
            request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, (
                'Your profile was successfully updated!'))
            return redirect('homeView')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        profile_form = EditCaloriesForm(instance=request.user.profile)
    return render(request, 'registration/updateCalories.html', {
        'profile_form': profile_form
    })
