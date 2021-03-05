from django.urls import path
from .import views 

urlpatterns = [
    path('', views.indexStudent),
    path('ViewContributes', views.ViewContributes),
    path('ViewDeadline', views.ViewDeadline),
    path('ViewDeadline/<int:id>', views.ViewDeadlineYear),
    path('indexStudent', views.indexStudent),
    path('indexUser', views.indexStudent), 
    
]

