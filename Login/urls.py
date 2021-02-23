from django.contrib import admin
from django.urls import path
from .import views 

urlpatterns = [
    path('', views.index),
    path('forgotPassword', views.forgotPassword),
    path('randomCode', views.randomCode),
    path('indexStudent', views.indexStudent),
    path('logout', views.logout),
]
