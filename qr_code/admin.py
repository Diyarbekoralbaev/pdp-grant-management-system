from django.contrib import admin
from .views import QRCodeView, QRCodeDetailView

admin.site.site_header = "QR Code Admin"
admin.site.site_title = "QR Code Admin Portal"
admin.site.index_title = "Welcome to QR Code Portal"
admin.site.register(QRCodeView)
admin.site.register(QRCodeDetailView)