"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls')),
    path('success/', views.success, name='success'),
    path('privacy/', views.privacy, name='privacy'),
    path('case0/', views.case0, name='case0'),
    path('case1/', views.case1, name='case1'),
    path('case2/', views.case2, name='case2'),
]


admin.site.site_header = "Админка сайта"
admin.site.site_title = "Панель управления"
admin.site.index_title = "Добро пожаловать в админку"
