from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from calculator.calcFuncs import macroCalc, calcRemainCalories
from foodEntry.models import FoodItem
from .filters import FoodItemFilter



# Create your views here.


@login_required
def profilePage_view(request):
    userProfile = request.user.profile

    # Query of all the food items associated with current user with dates in descending order
    foodlist = FoodItem.objects.filter(user=request.user).order_by('-date_added')



    numberOfEntries = len(foodlist)

    # Queryset of food items is run through the filter to get all food item parameters
    foodFilter = FoodItemFilter(request.GET, queryset=foodlist)

    # queryset is now filtered down with the search parmaeters
    foodlist = foodFilter.qs

    paginator = Paginator(foodlist, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'profile.html',{
        'userProfile' : userProfile,
        'foodlist' : foodlist,
        'foodFilter' : foodFilter,
        'number_of_food': numberOfEntries,
        'page_obj' : page_obj,
    })
