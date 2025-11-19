from django.urls import path 
from .views import RegisterView, LoginView, LogoutView, VerifyOTPView, ResendOTPView, ContactMessageCreateView, ContactMessageAdminView, ContactMessageDetailAdminView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact/', ContactMessageCreateView.as_view(), name='contact'),
    path('admin/contact/', ContactMessageAdminView.as_view(), name='admin-contact'),
    path('admin/contact/<int:pk>/', ContactMessageDetailAdminView.as_view(), name='admin-contact-detail'),
]