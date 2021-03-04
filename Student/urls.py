from django.urls import path
from .import views 

urlpatterns = [
    path('', views.indexStudent),
    path('ViewContributes', views.ViewContributes),
    path('ViewDeadline', views.ViewDeadline),
    path('indexStudent', views.indexStudent),
    path('indexUser', views.indexStudent), 

]

