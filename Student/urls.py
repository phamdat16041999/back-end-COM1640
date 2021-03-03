from django.urls import path
from .import views 

urlpatterns = [
    path('home', views.indexStudent),
    path('ViewContributes', views.ViewContributes),
    path('ViewDeadline', views.ViewDeadline),
    path('', views.indexStudent),
    path('indexUser', views.indexStudent), 

]

