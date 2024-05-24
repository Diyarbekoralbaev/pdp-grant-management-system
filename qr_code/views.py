from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import QRCodeModel, FoodIntakeRecord
from .serializers import QRCodeSerializer, FoodIntakeRecordSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from datetime import timedelta


class QRCodeView(APIView):
    # permission_classes = [IsAuthenticated,]
    # authentication_classes = [JWTAuthentication,]

    @swagger_auto_schema(request_body=QRCodeSerializer)
    def post(self, request):
        serializer = QRCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        qr_codes = QRCodeModel.objects.all()
        serializer = QRCodeSerializer(qr_codes, many=True)
        return Response(serializer.data)


class QRCodeDetailView(APIView):
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    def get(self, request, code):
        qr_code = QRCodeModel.objects.filter(code=code).first()
        user = QRCodeModel.objects.filter(code=code).first().user
        last_record = FoodIntakeRecord.objects.filter(user=user).last()
        if last_record and last_record.taken_at + timedelta(hours=3) > timezone.now(): # you can change the time here to test
            raise AuthenticationFailed('You can only take food every 2 hours', status.HTTP_403_FORBIDDEN)
        else:
            record = FoodIntakeRecord.objects.create(user=user)
            record.save()
        if not qr_code:
            raise AuthenticationFailed('Invalid QR Code', status.HTTP_404_NOT_FOUND)
        serializer = QRCodeSerializer(qr_code)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, code):
        qr_code = QRCodeModel.objects.filter(code=code).first()
        if not qr_code:
            raise AuthenticationFailed('Invalid QR Code')
        serializer = QRCodeSerializer(qr_code, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, code):
        qr_code = QRCodeModel.objects.filter(code=code).first()
        if not qr_code:
            raise AuthenticationFailed('Invalid QR Code')
        qr_code.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, code):
        qr_code = QRCodeModel.objects.filter(code=code).first()
        if not qr_code:
            raise AuthenticationFailed('Invalid QR Code')
        serializer = QRCodeSerializer(qr_code, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FoodIntakeRecordView(APIView):
    def get(self, request, user_id):
        records = FoodIntakeRecord.objects.filter(user=user_id)
        serializer = FoodIntakeRecordSerializer(records, many=True)
        return Response(serializer.data)