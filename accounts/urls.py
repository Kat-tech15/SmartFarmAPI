from django.urls import path 
<<<<<<< HEAD
from .views import RegisterView, LoginView, LogoutView
#from rest_framework_swagger.views import get_swagger_view
#schema_view = get_swagger_view(title= 'SmartFarm API')


urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    #path('swagger_docs/', schema_view),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
=======
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend-otp'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('contact/', views.ContactMessageCreateView.as_view(), name='contact'),
    path('admin/contact/', views.ContactMessageAdminView.as_view(), name='admin-contact'),
    path('admin/contact/<int:pk>/', views.ContactMessageDetailAdminView.as_view(), name='admin-contact-detail'),
>>>>>>> 4294538fb763fe93126bc76c703e502ff3037e80
]