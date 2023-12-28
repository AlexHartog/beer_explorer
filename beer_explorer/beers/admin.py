from django.contrib import admin

from .models import Beer, BeerCheckin, BeerType, Brand, User

admin.site.register(User)
admin.site.register(Brand)
admin.site.register(BeerType)
admin.site.register(Beer)
admin.site.register(BeerCheckin)
