from django.urls import path
from .views import TopUpOrderCreateAPIView, DashboardView

urlpatterns = [
    path('topup/', TopUpOrderCreateAPIView.as_view()),
    path('dashboard/', DashboardView.as_view())
]
