from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserModel, OTPModel
from .serializers import SignupSerializer, LoginSerializer, ChangePasswordSerializer, ResetPasswordSerializer, \
    SetNewPasswordSerializer, DeleteUserSerializer, UserChangePasswordSerializer, UserSerializer, UserPutSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from drf_yasg.utils import swagger_auto_schema
from .utils import generate_otp, send_otp

class SignupView(APIView):
    @swagger_auto_schema(
        request_body=SignupSerializer,
        tags=['auth']
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(password=make_password(serializer.validated_data['password']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        tags=['auth']
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = UserModel.objects.filter(username=username).first()
            print(user, password, user.password, check_password(password, user.password))
            if user and check_password(password, user.password) and user.is_active:
                # AccessToken.objects.filter(user=user).delete()
                # RefreshToken.objects.filter(user=user).delete()
                access_token = AccessToken.for_user(user)
                refresh_token = RefreshToken.for_user(user)
                user_id = user.uuid
                return Response(
                    {'access_token': str(access_token), 'refresh_token': str(refresh_token), 'user_id': user_id},
                    status=status.HTTP_200_OK)
            raise AuthenticationFailed('Invalid username or password')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['auth'],
        security=[{'Bearer': []}],
    )
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            raise AuthenticationFailed('No refresh token provided')
        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            return Response({'access_token': str(access_token)})
        except Exception as e:
            raise AuthenticationFailed('Invalid refresh token')


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['auth'],
        security=[{'Bearer': []}],
    )
    def get(self, request):
        user = request.user
        return Response({'message': f'Hello {user.username}'})


class MeView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]

    @swagger_auto_schema(
        tags=['auth'],
        security=[{'Bearer': ['read', 'write    ']}],
        operation_id='me',
    )
    def get(self, request):
        user = request.user
        serializer = SignupSerializer(user)
        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        tags=['auth'],
        security=[{'Bearer': []}],
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            if check_password(old_password, user.password):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'})
            raise AuthenticationFailed('Old password is incorrect')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['auth'],
        security=[{'Bearer': []}],
    )
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'})
        except Exception as e:
            return Response({'message': 'Logout failed'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['auth'],
        security=[{'Bearer': []}],
    )
    def post(self, request):
        try:
            user = request.user
            user.auth_token_set.all().delete()
            return Response({'message': 'Logout all successful'})
        except Exception as e:
            return Response({'message': 'Logout all failed'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        tags=['auth'],
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = UserModel.objects.filter(email=email).first()
            if user:
                otp_code = generate_otp()
                send_otp(otp=otp_code, email=email)
                return Response({'message': 'OTP sent successfully'})
            raise AuthenticationFailed('User with this email does not exist')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(APIView):
    @swagger_auto_schema(
        request_body=SetNewPasswordSerializer,
        tags=['auth'],
    )
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp_code']
            new_password = serializer.validated_data['new_password']
            email = serializer.validated_data['email']
            user = UserModel.objects.filter(email=email).first()
            if user:
                otp = OTPModel.objects.filter(user=user, otp=otp_code).first()
                if otp and not otp.is_valid(otp_code):
                    user.set_password(new_password)
                    user.save()
                    return Response({'message': 'Password changed successfully'})
                raise AuthenticationFailed('Invalid OTP code')
            raise AuthenticationFailed('User with this email does not exist')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        request_body=DeleteUserSerializer,
        tags=['admin_panel_auth'],
        security=[{'Bearer': []}],
    )
    def post(self, request):
        serializer = DeleteUserSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.is_superuser:
                user_for_delete = UserModel.objects.filter(id=serializer.validated_data['uuid']).first()
                if user_for_delete:
                    user_for_delete.delete()
                    return Response({'message': 'User deleted successfully'})
                raise AuthenticationFailed('User with this uuid does not exist')
            raise AuthenticationFailed('You are not authorized to perform this action')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        tags=['admin_panel_auth'],
        security=[{'Bearer': []}],
    )
    def get(self, request):
        user = request.user
        if user.is_superuser:
            users = UserModel.objects.all()
            serializer = SignupSerializer(users, many=True)
            return Response(serializer.data)
        raise AuthenticationFailed('You are not authorized to perform this action')

    @swagger_auto_schema(
        tags=['admin_panel_auth'],
        security=[{'Bearer': []}],
        request_body=SignupSerializer,
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.is_superuser:
                user_for_change = serializer.save(password=make_password(serializer.validated_data['password']))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            raise AuthenticationFailed('You are not authorized to perform this action')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['admin_panel_auth'],
        security=[{'Bearer': []}],
        request_body=UserPutSerializer,
    )
    def put(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.is_superuser:
                user_for_change = UserModel.objects.filter(id=serializer.validated_data['uuid']).first()
                if user_for_change:
                    user_for_change.username = serializer.validated_data['username', user_for_change.username]
                    user_for_change.email = serializer.validated_data['email', user_for_change.email]
                    user_for_change.phone = serializer.validated_data['phone', user_for_change.phone]
                    user_for_change.is_student = serializer.validated_data['is_student', user_for_change.is_student]
                    user_for_change.is_cook = serializer.validated_data['is_cook', user_for_change.is_cook]
                    user_for_change.is_grant = serializer.validated_data['is_grant', user_for_change.is_grant]
                    user_for_change.student_id = serializer.validated_data['student_id', user_for_change.student_id]
                    user_for_change.courses_year = serializer.validated_data[
                        'courses_year', user_for_change.courses_year]
                    user_for_change.group_number = serializer.validated_data[
                        'group_number', user_for_change.group_number]
                    user_for_change.is_active = serializer.validated_data['is_active', user_for_change.is_active]
                    user_for_change.is_superuser = serializer.validated_data[
                        'is_superuser', user_for_change.is_superuser]
                    user_for_change.save()
                    return Response(serializer.data)
                raise AuthenticationFailed('User with this uuid does not exist')
            raise AuthenticationFailed('You are not authorized to perform this action')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['admin_panel_auth'],
        security=[{'Bearer': []}],
        request_body=DeleteUserSerializer,
    )
    def delete(self, request):
        serializer = DeleteUserSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.is_superuser:
                user_for_delete = UserModel.objects.filter(id=serializer.validated_data['uuid']).first()
                if user_for_delete:
                    user_for_delete.delete()
                    return Response({'message': 'User deleted successfully'})
                raise AuthenticationFailed('User with this uuid does not exist')
            raise AuthenticationFailed('You are not authorized to perform this action')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        request_body=UserChangePasswordSerializer,
        tags=['admin_panel_auth'],
        security=[{'Bearer': []}],
    )
    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.is_superuser:
                user_for_change = UserModel.objects.filter(id=serializer.validated_data['uuid']).first()
                if user_for_change:
                    new_password = serializer.validated_data['new_password']
                    user_for_change.set_password(new_password)
                    user_for_change.save()
                    return Response({'message': 'Password changed successfully'})
                raise AuthenticationFailed('User with this uuid does not exist')
            raise AuthenticationFailed('You are not authorized to perform this action')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
