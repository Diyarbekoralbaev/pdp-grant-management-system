from django.urls import path
from .views import QRCodeView, QRCodeDetailView, FoodIntakeRecordView

urlpatterns = [
    path('', QRCodeView.as_view()),
    path('<code>/', QRCodeDetailView.as_view()),
    path('food-intake/<user_id>/', FoodIntakeRecordView.as_view())
]
