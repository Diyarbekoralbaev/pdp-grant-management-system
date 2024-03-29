from django.urls import path
from .views import QRCodeView, QRCodeDetailView

urlpatterns = [
    path('', QRCodeView.as_view()),
    path('<code>/', QRCodeDetailView.as_view())
]
