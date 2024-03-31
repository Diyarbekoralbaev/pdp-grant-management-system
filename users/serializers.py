from rest_framework import serializers
from .models import UserModel


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'phone', 'password', 'is_student', 'is_cook', 'is_grant', 'student_id', 'courses_year', 'group_number', 'date_joined', 'last_login', 'last_logged_device', 'last_logged_ip']
        read_only_fields = ['date_joined', 'last_login', 'last_logged_device', 'last_logged_ip', 'id']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['is_student']:
            if attrs['student_id'] is None:
                raise serializers.ValidationError('Student ID is required for student')
            if attrs['courses_year'] is None:
                raise serializers.ValidationError('Courses year is required for student')
            if attrs['group_number'] is None:
                raise serializers.ValidationError('Group number is required for student')
        if attrs['is_cook'] and attrs['is_grant']:
            raise serializers.ValidationError('User can be either cook or grant, not both')
        if not attrs['is_student'] and not attrs['is_cook'] and not attrs['is_grant']:
            raise serializers.ValidationError('User must be either student, cook or grant')
        if UserModel.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError('Username is already taken')
        if UserModel.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Email is already taken')
        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
        read_only_fields = ['id', 'username', 'email', 'phone', 'is_student', 'is_cook', 'is_grant', 'is_staff', 'is_superuser', 'is_active', 'last_time_eat', 'date_joined', 'last_login', 'last_logged_device', 'last_logged_ip']


class ChangePasswordSerializer(serializers.Serializer):
    model = UserModel

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] == attrs['old_password']:
            raise serializers.ValidationError('New password must be different from old password')
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError('New passwords do not match')
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    model = UserModel

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        if not UserModel.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('User with this email does not exist')
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    model = UserModel

    otp_code = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] == attrs['otp_code']:
            raise serializers.ValidationError('New password must be different from OTP code')
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError('New passwords do not match')
        return attrs


class DeleteUserSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)

    def validate(self, attrs):
        if not UserModel.objects.filter(id=attrs['id']).exists():
            raise serializers.ValidationError('User with this id does not exist')
        return attrs


class UserChangePasswordSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError('New passwords do not match')
        return attrs


class UserPutSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)