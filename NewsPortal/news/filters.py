import django_filters
from django import forms
from .models import *

class NewsFilter(django_filters.FilterSet):
    timestamp__gte = django_filters.DateFilter(
        field_name='timestamp',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Post
        fields = ['name', 'author', 'category', 'timestamp__gte']