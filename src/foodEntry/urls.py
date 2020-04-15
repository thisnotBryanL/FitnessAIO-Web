from django.conf.urls import url
from django.urls import include, path

from foodEntry.views import createfooditem_View, updatefooditem_View, deletefooditem_View
urlpatterns = [
    path('create/', createfooditem_View, name="create-food"),
    path('update/<int:id>/', updatefooditem_View, name="update-food" ),
    path('delete/<int:id>/', deletefooditem_View, name="delete-food" ),
]
