from rest_framework import viewsets
from django.http import JsonResponse

from .stats import UserStats

from .models import Beer, BeerCheckin, BeerType, Brand, User
from .serializers import (
    BeerCheckinSerializer,
    BeerCheckinCreateSerializer,
    BeerSerializer,
    BeerTypeSerializer,
    BrandSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BeerTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BeerType.objects.all()
    serializer_class = BeerTypeSerializer


class BeerViewSet(viewsets.ModelViewSet):
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer


class BeerCheckinViewSet(viewsets.ModelViewSet):
    queryset = BeerCheckin.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BeerCheckinCreateSerializer
        else:
            return BeerCheckinSerializer


def get_points(request):
    user_stats = UserStats()
    data = user_stats.get_stats()
    return JsonResponse(data, safe=False)
