from django.urls import path
from .import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.indexCoordinator),
    path('viewContribute/<int:id>', views.viewContribute),
    path('indexUser', views.indexCoordinator),
    path('sendMessenger/<int:id>/<str:messenger>', views.sendMessenger),
    path('getMessenger/<int:id>', views.getMessenger),
    path('public/<int:status>/<int:id>', views.public),
    path('filter/', views.filter),
    path('my_profileCoordinator', views.my_profileCoordinator),
]