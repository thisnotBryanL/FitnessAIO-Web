from django.conf.urls import url
from django.urls import include, path

from foodEntry.views import createfooditem_View
urlpatterns = [
    path('create/', createfooditem_View, name="create-food"),
]
