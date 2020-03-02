from django.conf.urls import url
from django.urls import include, path

from foodEntry.views import FoodItemCreateView
urlpatterns = [
    path('create/', FoodItemCreateView.as_view(), name="create-food"),

]
