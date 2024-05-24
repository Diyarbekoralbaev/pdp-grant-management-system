from django.contrib import admin
from .models import QRCodeModel, FoodIntakeRecord

admin.site.register(QRCodeModel)
admin.site.register(FoodIntakeRecord)