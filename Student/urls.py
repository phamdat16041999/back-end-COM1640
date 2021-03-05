from django.urls import path
from .import views 

urlpatterns = [
    path('', views.indexStudent),
    path('ViewContributes', views.ViewContributes),
    path('ViewDeadline', views.ViewDeadline),
    path('ViewDeadline/<int:id>', views.ViewDeadlineYear),
    path('ViewDeadline/Upload/<int:id>', views.UploadFile),
    path('indexStudent', views.indexStudent),
    path('indexUser', views.indexStudent), 
    path('book_list/<int:id>', views.book_list, name='book_list'),
    # path('upload', views.upload_book, name='upload_book'),

]

