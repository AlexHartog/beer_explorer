from django.db.models import Q
from rest_framework import serializers
import logging

from .models import Beer, BeerCheckin, BeerType, Brand, User

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name"]


class BeerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerType
        fields = ["name"]


class BrandField(serializers.CharField):
    def to_representation(self, value):
        return BrandSerializer(value).data

    def to_internal_value(self, data):
        brand = Brand.objects.filter(name__iexact=data).first()
        if not brand:
            brand = Brand.objects.create(name=data)
            logger.info(f"Created new brand {data}")
        return brand


class TypeField(serializers.CharField):
    def to_representation(self, value):
        return BeerTypeSerializer(value).data

    def to_internal_value(self, type_name):
        beer_type = BeerType.objects.filter(name__iexact=type_name).first()
        if not beer_type:
            beer_type = BeerType.objects.create(name=type_name)
            logger.info(f"Created new beer type {beer_type}")
        return beer_type


class BeerSerializer(serializers.ModelSerializer):
    brand = BrandField()
    type = TypeField()

    class Meta:
        model = Beer
        fields = "__all__"


class BeerCheckinSerializer(serializers.ModelSerializer):
    beer = BeerSerializer()
    user = UserSerializer()

    class Meta:
        model = BeerCheckin
        fields = "__all__"


class BeerCheckinCreateSerializer(serializers.ModelSerializer):
    beer_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BeerCheckin
        fields = ["user_id", "date", "beer_id", "rating"]
