from django.urls import path
from . import views 

urlpatterns = [
    path('list/', views.LivestockList.as_view()),
    path('<int:pk>/', views.LivestockDetail.as_view()),
]