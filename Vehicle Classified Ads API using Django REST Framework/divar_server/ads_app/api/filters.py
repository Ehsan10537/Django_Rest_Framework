import django_filters
from ads_app.models import CarAd, MotorcycleAd


class CarAdFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = CarAd
        fields = []


class MotorcycleAdFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = MotorcycleAd
        fields = []