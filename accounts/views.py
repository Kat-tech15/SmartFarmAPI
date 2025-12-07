from rest_framework import generics, permissions,status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db import connection
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer, EmptySerializer,VerifyOTPSerializer, ResendOTPSerializer, ContactMessageSerializer
from .utils import send_otp_to_user, notify_admin_contact
from .models import  CustomUser, EmailOTP, ContactMessage
from django.utils import timezone

class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            otp_via = getattr(user, 'otp_via', 'email').lower()
            send_via_sms = otp_via == 'sms'

            send_otp_to_user(user, via_sms=send_via_sms)

            return Response({'message': f'User registered successfully. OTP send via {otp_via}.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']

       
        
        email_otp = EmailOTP.objects.filter(code=code, is_used=False).order_by('-created_at').first()
        if not email_otp:
            return Response({'message': 'OTP not found. Please request a new OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if email_otp.attempts >= 5:
            return Response({'message': 'Too many incorrect attempts. Request a new OTP'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        if email_otp.code != code:
            email_otp.attempts += 1
            email_otp.save(update_fields=['attempts'])
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        if email_otp.is_expired():
            return Response({'message': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        
        email_otp.is_used =True
        email_otp.save(update_fields=['is_used'])
        user = email_otp.user
        user.is_verified = True
        user.save(update_fields=['is_verified'])

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
            return Response({'message': 'If the email you provided exists, an OTP will be sent.'}, status=status.HTTP_200_OK)
        
        last_otp = EmailOTP.objects.filter(user=user, is_used=False).order_by('-expire_at').first()
        cooldown_seconds = 300
        if last_otp:
            elapsed = (timezone.now() - last_otp.created_at).total_seconds()
            if elapsed < cooldown_seconds:
                remaining = int(cooldown_seconds - elapsed)
                return Response({'message': f'Please wait {remaining} seconds before requesting a new OTP.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            EmailOTP.objects.filter(user=user, is_used=False).delete()
        
        otp_obj = EmailOTP.create_for_user(user)
        otp_via = getattr(user, 'otp_via', 'email').lower()
        send_via_sms = otp_via == 'sms'

        send_otp_to_user(user, code=otp_obj.code, via_sms=send_via_sms)

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
            
            
            refresh  = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh),
                             'access': str('refresh.access_token'),
                             'username': user.username,
            })
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    
class LogoutView(generics.GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if hasattr(request.user, "access_token"):
            request.user.access_token.delete()

        return Response({'message': 'User logged out successfully!'}, status=status.HTTP_200_OK)

@api_view
def health_check(request):
    try:
        connection.ensure_connection()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return JsonResponse({
        "status": "OK" if db_status == "connected" else "ERROR",
        "database": db_status,
        "version": "v1.0.0",
        "message": "Ecommerce API is running smoothly."
    })


class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]


    def perform_create(self, serializer):
        message_instance = serializer.save()

        notify_admin_contact(message_instance)
    
class ContactMessageAdminView(generics.ListAPIView):
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.IsAdminUser]

class ContactMessageDetailAdminView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.IsAdminUser]