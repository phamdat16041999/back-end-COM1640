from django.urls import path
from .import views 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.indexStudent),
    path('ViewContributes', views.ViewContributes, name='ViewContributes'),
    path('ViewDeadline', views.ViewDeadline),
    path('ViewDeadline/<int:id>', views.ViewDeadlineYear),
    path('ViewDeadline/viewUploaded/<int:id>', views.viewUploaded),
    path('ViewDeadline/viewUpdate/<int:id>', views.viewUpdate),
    path('ViewDeadline/uploadContribute/<int:id>',views.uploadContribute),
    path('ViewDeadline/updateContribute/<int:id>',views.updateContribute),
    path('ViewDeadline/viewUpload/<int:id>', views.viewUpload),
    path('ViewDeadline/sendMessenger/<int:id>/<str:messenger>', views.sendMessenger),
    path('ViewDeadline/getMessenger/<int:id>', views.getMessenger),
    path('uploadContribute/<int:id>', views.uploadContribute),
    path('indexStudent', views.indexStudent),
    path('indexUser', views.indexStudent),
    path('filter/', views.filter),  
    path('my_profileStudent', views.my_profileStudent),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)