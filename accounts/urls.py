from django.urls import path 
from .views import RegisterView, LoginView, LogoutView
#from rest_framework_swagger.views import get_swagger_view
#schema_view = get_swagger_view(title= 'SmartFarm API')


urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    #path('swagger_docs/', schema_view),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]