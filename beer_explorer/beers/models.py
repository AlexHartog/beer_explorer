from django.db import models
from django.db.models.functions import Lower


class User(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="brand_unique_lower_case_name",
            )
        ]

    def __str__(self):
        return self.name


class BeerType(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="type_unique_lower_case_name",
            )
        ]

    def __str__(self):
        return self.name


class Beer(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    type = models.ForeignKey(BeerType, on_delete=models.CASCADE)
    percentage = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class BeerCheckin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    date = models.DateField()
    picture = models.ImageField(upload_to="checkin_pictures", blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)