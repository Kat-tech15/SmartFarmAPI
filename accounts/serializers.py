from rest_framework import serializers
from . models import CustomUser, ContactMessage
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    otp_via = serializers.ChoiceField(
        choices=[('email', 'Email'), ('sms', 'SMS')],
        default='email',
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'phone', 'email', 'password', 'otp_via']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        otp_via = validated_data.pop('otp_via', 'email')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone = validated_data['phone'],
            password=validated_data['password']
        )
        Token.objects.create(user=user)
        user.otp_via = otp_via
        return user
    
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class EmptySerializer(serializers.Serializer):
    pass

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message']
        