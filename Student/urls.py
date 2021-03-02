from django.urls import path
from .import views 

urlpatterns = [
    path('home', views.indexStudent),
    path('contribute', views.ViewContributes),
    path('', views.ViewDeadline),

]

