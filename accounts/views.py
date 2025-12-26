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

class LoginView(generics.GenericAPIView):
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
                             'access': str(refresh.access_token),
                             'username': user.username,
            })
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_tooken.delete()
        except:
            pass 
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
