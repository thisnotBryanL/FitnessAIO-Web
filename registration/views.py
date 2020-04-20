from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

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


# Same way to do Json Requests for charts using REST Framework API View  (BEST WAY)
# class ChartData(APIView):
#     """
#     View to list all users in the system.

#     * Requires token authentication.
#     * Only admin users are able to access this view.
#     """
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]

#     def get(self, request, format=None):
#         profile = request.user.profile
#         macros = dict()
#         macros = macroCalc(float(profile.weight), 'average',
#                        float(profile.calories))
#         data = {
#             "carbs": macros['carbs'],
#             "fats": macros['fat'],
#             "protein": macros['protein']
#         }
#         return Response(data)

# Returns JSON data to be used for charts
def get_data(request):

    labels = ['Protein', 'Carbohydrates', 'Fat']
    if not request.user.is_authenticated:
        currFoodItems = FoodItem.objects.filter().order_by('-date_added')[:3]
        proMacro = 180
        fatMacro = 66
        carbMacro = 220
        userCals = 2200

        testUserCalsFromFood = calcRemainCalories(
            currFoodItems, userCals, proMacro, fatMacro, carbMacro)

        foodNames = []
        foodCalories = []
        calsConvert = 0
        for items in currFoodItems:
            foodNames.append(items.name)
            calsConvert = float(items.calories)
            foodCalories.append(calsConvert)
        print(foodNames)
        print(foodCalories)
        
        default_items = [testUserCalsFromFood['proteinRemain'],
                         testUserCalsFromFood['carbsRemain'], testUserCalsFromFood['fatRemain']]
        totMacros = [proMacro,
                     carbMacro, fatMacro]

        data = {
            "labels": labels,
            "default": default_items,
            "total_macros": totMacros,
            "labels2": foodNames,
            "totalCals": foodCalories
        }
        
    else: 
        profile = request.user.profile
        macros = dict()
        macros = macroCalc(float(profile.weight), 'average',
                        float(profile.calories))

        #Queries food items only for the current day
        queryset = FoodItem.objects.filter(
            date_added__date=timezone.localdate(), user=request.user)

        foodNames = []
        foodCalories = []
        calsConvert = 0
        for items in queryset:
            foodNames.append(items.name)
            calsConvert = float(items.calories)
            foodCalories.append(calsConvert)

        #Calculator to calculate the remaining calories left after querying food consumed for the day
        calsFromFood = calcRemainCalories(
            queryset, float(profile.calories), macros['protein'], macros['fat'], macros['carbs'])

        default_items = [calsFromFood['proteinRemain'],calsFromFood['carbsRemain'],calsFromFood['fatRemain']]
        totMacros = [macros['protein'],
                        macros['carbs'], macros['fat']]
        
        data = {
            "labels" : labels,
            "default": default_items,
            "total_macros": totMacros,
            "labels2": foodNames,
            "totalCals" : foodCalories
        }
    return JsonResponse(data)

def home(request):
    userCals = 0
    userCalsRemain = 0
    if not request.user.is_authenticated:

        currFoodItems = FoodItem.objects.filter().order_by('-date_added')[:3]
        proMacro = 180
        fatMacro = 66
        carbMacro = 220
        userCals = 2200

        testUserCalsFromFood = calcRemainCalories(
            currFoodItems, userCals, proMacro, fatMacro, carbMacro)



        return render(request, 'home.html', {
            'testUserProRemain' : testUserCalsFromFood['proteinRemain'],
            'testUserFatRemain' : testUserCalsFromFood['fatRemain'],
            'testUserCarbRemain' : testUserCalsFromFood['carbsRemain'],
            'userCalsRemain': testUserCalsFromFood['calsRemain'],
            'testUserProtein': proMacro,
            'testUserFat' : fatMacro,
            'testUserCarb' : carbMacro,
            'userCals' : userCals,
            'testUserFoodList': currFoodItems
        })
    else:
        profile = request.user.profile
        macros = dict()
        macros = macroCalc(float(profile.weight),'average',float(profile.calories))
        userCals = float(profile.calories)

        #Query Set that retrieves the 5 most recent food items entered
        last_5Food = FoodItem.objects.filter(user=profile.user).order_by('-date_added')[:5]
                
        #Queries food items only for the current day
        queryset = FoodItem.objects.filter(
            date_added__date=timezone.localdate(), user = request.user)

        #Calculator to calculate the remaining calories left after querying food consumed for the day
        calsFromFood = calcRemainCalories(queryset, float(profile.calories),macros['protein'], macros['fat'], macros['carbs'])
        context = {
            "userProfile" : profile,
            "userCals" : userCals,
            "carbs" : macros['carbs'],
            "fats" : macros['fat'],
            "protein" : macros['protein'],
            "last5Food" : last_5Food,
            "userCalsRemain": calsFromFood['calsRemain'],
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
            return redirect('homeView')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        profile_form = EditCaloriesForm(instance=request.user.profile)
    return render(request, 'registration/updateCalories.html', {
        'profile_form': profile_form
    })
