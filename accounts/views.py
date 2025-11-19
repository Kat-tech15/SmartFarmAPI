from rest_framework import generics, permissions,status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer, EmptySerializer,VerifyOTPSerializer, ResendOTPSerializer
from .utils import send_otp_to_user
from .models import  CustomUser, EmailOTP
from django.utils import timezone
from datetime import timedelta
import random

class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_otp_to_user(user)
            #token, _ = Token.objects.get_or_create(user=user)
            return Response({'message': 'User registered successfully. OTP send to your email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        try:
            user = CustomUser.objects.get(email=email)
            email_otp = EmailOTP.objects.get(user=user, code=code)
        except (CustomUser.DoesNotExist, EmailOTP.DoesNotExist):
            return Response({'message': 'Invalid OTP or email.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if email_otp.is_expired():
            return Response({'message': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_verified = True
        user.save()

        return Response({'message': 'OTP verified successfully!'}, status=status.HTTP_200_OK)

class ResendOTPView(generics.GenericAPIView):
    serializer_class = ResendOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        last_otp = EmailOTP.objects.filter(user=user, is_used=False).order_by('-expire_at').first()
        if last_otp:
            if timezone.now() < last_otp.expire_at - timedelta(minutes=5) + timedelta(minutes=5):
                wait_time = (last_otp.expire_at - timezone.now()).seconds
                return Response({'message': f"please wait {wait_time//60} minutes and {wait_time%60}  seconds before requesting a new OTP."},
                                status=status.HTTP_429_TOO_MANY_REQUESTS
                                )
            last_otp.delete()
        
        code = str(random.randint(100000, 999999))
        expire_at = timezone.now() + timedelta(minutes=5)
        otp_instance = EmailOTP.objects.create(code=code, expire_at=expire_at)

        send_otp_to_user(user, otp_instance.code)

        return Response({'message': 'OTP resent successfully.'}, status=status.HTTP_200_OK)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer= self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        
        if user:
            if not user.is_verified:
                return Response({'message': 'Email not verified. Please verify your email to login.'}, status=status.HTTP_403_FORBIDDEN)
            
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key,
                             'username': user.username,
                             'email': user.email
            })
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    
class LogoutView(generics.GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if hasattr(request.user, "auth_token"):
            request.user.auth_token.delete()

        return Response({'message': 'User logged out successfully!'}, status=status.HTTP_200_OK)

