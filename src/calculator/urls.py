from django.conf.urls import url
from django.urls import include, path

from .views import macroCalcView

app_name = 'calculator'
urlpatterns = [
    path('macros/', macroCalcView, name="macro-calc"),
]
