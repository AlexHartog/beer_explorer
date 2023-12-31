from rest_framework import viewsets

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
