from django.contrib import admin
from ads_app.models import CarAd, MotorcycleAd, Review, CarAdImage, MotorcycleAdImage

admin.site.register(CarAd)
admin.site.register(MotorcycleAd)
admin.site.register(Review)
admin.site.register(CarAdImage)
admin.site.register(MotorcycleAdImage)
