from django.urls import path, include
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('', views.LuckView.as_view(), name="luck"),
    path('flag/', views.flag_view, name="flag"),
    path('<str:user_id>/', views.ShareView.as_view(), name="share"),
    path('error/', views.error_view, name="error"),
]
