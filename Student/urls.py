from django.urls import path
from .import views 

urlpatterns = [
    path('/a', views.indexStudent),
    path('', views.ViewContributes),
]

