import uuid
from rest_framework import serializers
from .models import QRCodeModel


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCodeModel
        fields = '__all__'
    code = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    expired_at = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        if 'code' in attrs and not QRCodeModel.objects.filter(code=attrs['code']).exists():
            raise serializers.ValidationError('Invalid QR Code')
        if 'expired_at' in attrs:
            if self.instance and self.instance.is_expired():
                raise serializers.ValidationError('QR Code is expired')
            if self.instance and self.instance.expired_at != attrs['expired_at']:
                raise serializers.ValidationError('You cannot change expired_at')

        if 'code' in attrs:
            raise serializers.ValidationError('You cannot change code')

        if 'user' in attrs:
            if not attrs['user'].is_active:
                raise serializers.ValidationError('User is not active')

        if 'user' in attrs and self.instance:
            if attrs['user'] != self.instance.user:
                raise serializers.ValidationError('You cannot change user')

        return attrs


