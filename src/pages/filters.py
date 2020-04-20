import django_filters

from django_filters import DateFilter, CharFilter
from foodEntry.models import FoodItem

class FoodItemFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    start_date = DateFilter(field_name = 'date_added', lookup_expr = 'gte')
    end_date = DateFilter(field_name='date_added', lookup_expr='lte')
    class Meta:
        model = FoodItem
        fields = ['time']
