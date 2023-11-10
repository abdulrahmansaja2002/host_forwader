"""
URL configuration for host_forwader project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from django.contrib import admin
from django.conf import settings
from django.urls import path
from .views import index, add_target_host, host_forwader, set_target_host, check_conection, scan_all_lan_host,set_forward_headers, set_forward_root_path, set_full_forward


urlpatterns = [
    # path('admin/', admin.site.urls),
    # add static url for static files
    # path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
    path('settings/', index, name="index"),
    path('settings/set_target_host/', set_target_host, name='set_target_host'),
    path('settings/check_conection/', check_conection, name='check_conection'),
    path('settings/add_target_host/', add_target_host, name="add_target_host"),
    path('settings/scan_all_lan_host/', scan_all_lan_host, name="scan_all_lan_host"),
    path('settings/set_forward_headers/', set_forward_headers, name="set_forward_headers"),
    path('settings/set_forward_root_path/', set_forward_root_path, name="set_forward_root_path"),
    path('settings/set_full_forward/', set_full_forward, name="set_full_forward"),
    path('', host_forwader, {'path': ''}),
    path('<path:path>', host_forwader),
    # path('home/', index, name="index"),

]
