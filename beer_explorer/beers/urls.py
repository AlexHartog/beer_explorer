from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import get_points

from .views import (
    BeerCheckinViewSet,
    BeerTypeViewSet,
    BeerViewSet,
    BrandViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"brands", BrandViewSet)
router.register(r"beertypes", BeerTypeViewSet)
router.register(r"beers", BeerViewSet)
router.register(r"beercheckins", BeerCheckinViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("points", get_points, name="points"),
]
