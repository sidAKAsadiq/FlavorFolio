"""
URL configuration for Recipe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from RecipeApp.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add-recipe/',add_recipe,name = 'add-recipe'),
    path('view-all/',view_all,name = 'view-all'),
    path('delete-recipe/',delete_recipe,name = 'delete-recipe'),
    path('delete-select/',delete_select,name = 'delete-select'),
    path('delete-id/<id>/',delete_id,name = "delete-id"), 
    path('update/',update,name = "update"), 
    path('update-id/<id>/',update_id,name = "update-id"), 
    path('search',search,name = "search"),   
    path('login/' , login_page , name = "login_page"),
    path('logout/' , logout_page , name = "logout_page"),
    path('register/' , register , name = "register"),
    path('' , homepage , name = "home")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()