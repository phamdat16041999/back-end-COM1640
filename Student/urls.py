from django.urls import path
from .import views 

urlpatterns = [
    path('home', views.indexStudent),
    path('', views.ViewContributes),
    path('ViewDeadline', views.ViewDeadline),
    path('indexStudent', views.indexStudent),
    path('indexUser', views.indexStudent), 

]

