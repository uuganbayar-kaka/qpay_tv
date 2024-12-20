from django.urls import path

from base import views

urlpatterns = [
    path('ping', views.ping),
    path('get_invioce/', views.GetInvioceView.as_view()),
]
