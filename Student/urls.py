from django.urls import path
from .import views 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.indexStudent),
    path('ViewContributes', views.ViewContributes),
    path('ViewDeadline', views.ViewDeadline),
    path('ViewDeadline/<int:id>', views.ViewDeadlineYear),
    path('viewUpload/<int:id>', views.viewUpload),
    path('uploadContribute/<int:id>', views.uploadContribute),
    path('indexStudent', views.indexStudent),
    path('indexUser', views.indexStudent), 
    # path('upload', views.upload_book, name='upload_book'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)