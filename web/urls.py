from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('case0/', views.case_view, name='case0'),
]
