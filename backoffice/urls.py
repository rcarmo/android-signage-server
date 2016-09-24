"""backoffice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView
from signage import views
from os import environ

admin.site.site_header = environ.get('SITE_NAME', 'Signage Administration')

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='https://pixels.camp')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/assetlist/(?P<device_id>(.+))/(?P<mac_address>([0-9A-F]{2}[:-]){5}([0-9A-F]{2}))/(?P<ip_address>((2[0-5]|1[0-9]|[0-9])?[0-9]\.){3}((2[0-5]|1[0-9]|[0-9])?[0-9]))$', views.PlaylistView.as_view(), name="Get playlist"),
]