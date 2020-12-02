import django_filters
from django_filters import CharFilter

from .models import *

class productFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Product
        # fields = '__all__'
        # exclude = ['image']
        fields = ['name']
