from django.urls import path
from .import views 

urlpatterns = [
    path('', views.indexGuess),
    path('filter/', views.filter),
]