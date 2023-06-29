"""sophia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path , include , re_path
from accounts import urls as accurl
from accounts.views import home
from administration.views import testresult
from assessments import urls as assurl
from administration import urls as adminurl
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.views.defaults import page_not_found, server_error

handler404 = page_not_found
handler500 = server_error

admin.site.site_header = "Sophia Admin"
admin.site.site_title = "Sophia Portal"
admin.site.index_title = "Welcome to Sophia assessment Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('testcode/',testresult,name='testresult'),
    path('user/', include(accurl)),
    path('assessments/', include(assurl)),
    path('administration/', include(adminurl)),

    
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
