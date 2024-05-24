from django.contrib import admin
from .models import QRCodeModel, FoodIntakeRecord


class QRCodeModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'updated_at', 'expired_at', 'is_expired')
    list_filter = ('user', 'created_at', 'updated_at', 'expired_at')
    search_fields = ('user', 'code', 'created_at', 'updated_at', 'expired_at')
    readonly_fields = ('created_at', 'updated_at', 'expired_at', 'is_expired')


class FoodIntakeRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'taken_at')
    list_filter = ('user', 'taken_at')
    search_fields = ('user', 'taken_at')
    readonly_fields = ('taken_at',)


admin.site.register(QRCodeModel, QRCodeModelAdmin)
admin.site.register(FoodIntakeRecord, FoodIntakeRecordAdmin)