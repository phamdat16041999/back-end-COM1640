from django.urls import path
from .import views 

urlpatterns = [
    path('', views.indexCoordinator),
    path('viewContribute', views.viewContribute),
]