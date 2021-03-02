from django.urls import path
from .import views 

urlpatterns = [
    path('home', views.indexStudent),
    path('ViewContributes', views.ViewContributes),
    path('', views.ViewDeadline),
    path('indexStudent', views.indexStudent),
    path('indexUser', views.indexStudent),  #lỗi............

]

