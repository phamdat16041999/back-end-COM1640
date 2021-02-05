from django.contrib import admin
from django.urls import path
from .import views 

urlpatterns = [
    path('', views.index),
    path('forgotPassword', views.forgotPassword),
    path('randomCode', views.randomCode),
]
