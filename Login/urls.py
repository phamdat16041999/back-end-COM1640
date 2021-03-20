from django.contrib import admin
from django.urls import path, include
from .import views 

urlpatterns = [
    path('', views.index),
    path('forgotPassword', views.forgotPassword),
    path('randomCode', views.randomCode),
    path('indexUser', views.indexUser),
    path('logout', views.logout),
    path('authenticationInterface/<int:id>/', views.authenticationInterface),
    path('authentication/<int:id>/', views.authentication),
    path('changePasswordInterface/<int:id>/<str:code>/', views.changePasswordInterface),
    path('changePassword/<int:id>/', views.changePassword),
    path('Student', include('Student.urls')),
    path('Coordinator/', include('Coordinator.urls')),
    path('Manager/', include('Manager.urls')),
    path('Guess/', include('Guess.urls')),

]
