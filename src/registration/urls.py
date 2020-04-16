from django.conf.urls import url
from django.urls import include, path

from registration.views import (home, signup, update_profile, logout_requestView, update_calories)

app_name = 'registration'
urlpatterns = [
    path('', signup, name= "signup"),
    path('update-profile/', update_profile, name="update-profile"),
    path('update-calories/', update_calories, name="update-calories"),
    path('logout/', logout_requestView, name ="logout" ),
]
 
