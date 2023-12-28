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


class BeerSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    type = BeerTypeSerializer(read_only=True)
    brand_name = serializers.CharField(write_only=True)
    type_name = serializers.CharField(write_only=True)

    class Meta:
        model = Beer
        fields = "__all__"

    def create(self, validated_data):
        brand_name = validated_data.pop("brand_name", None)
        if brand_name:
            brand = Brand.objects.filter(name__iexact=brand_name).first()
            if not brand:
                brand = Brand.objects.create(name=brand_name)
                logger.info(f"Created new brand {brand_name}")
        else:
            raise serializers.ValidationError({"brand_name": "This field is required."})

        type_name = validated_data.pop("type_name", None)
        if type_name:
            type = BeerType.objects.filter(name__iexact=type_name).first()
            if not type:
                type = BeerType.objects.create(name=type_name)
                logger.info(f"Created new beer type {type_name}")
        else:
            raise serializers.ValidationError({"type_name": "This field is required."})

        beer = Beer.objects.create(brand=brand, type=type, **validated_data)
        return beer


class BeerCheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerCheckin
        fields = "__all__"
