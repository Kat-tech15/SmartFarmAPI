from django.urls import path
from . import views 

urlpatterns = [
    path('list/', views.CropDetail.as_view()),
    path('<int:pk>/', views.CropDetail.as_view()),
]