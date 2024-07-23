from django.contrib import admin
from .models import BikeModel, BikeRentalModel

admin.site.register(BikeModel)
admin.site.register(BikeRentalModel)