import django_filters
from .models import Donor

class DonorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    email = django_filters.CharFilter(lookup_expr='icontains', label='Email')
    phone = django_filters.CharFilter(lookup_expr='icontains', label='Phone')

    class Meta:
        model = Donor
        fields = ['name', 'email', 'phone', 'preferred_contact_method']