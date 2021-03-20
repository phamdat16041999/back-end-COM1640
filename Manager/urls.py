from django.urls import path
from .import views 

urlpatterns = [
    path('', views.indexManager, name='home'),
    path('Contributionofterms', views.Contributionofterms),
    path('Percentageofcontributionscontributetoeachfaculty', views.Percentageofcontributionscontributetoeachfaculty),
    path('Numberofstudentssubmittingallsubjectsineachterm', views.Numberofstudentssubmittingallsubjectsineachterm),
    path('Exercisesthatthecoordinatorhasnotreadyet',views.Exercisesthatthecoordinatorhasnotreadyet),
    path('viewContribution', views.viewContribution),
    path('filter/', views.filter),
]