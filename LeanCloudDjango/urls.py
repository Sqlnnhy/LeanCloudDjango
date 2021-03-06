"""LeanCloudDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from LCD import views as lcd_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^list', lcd_view.show),
    url(r'^home', lcd_view.home),
    url(r'^index', lcd_view.index),
    url(r'^rpc/ping.action', lcd_view.ping),
    url(r'^rpc/releaseTicket.action', lcd_view.releaseTicket),
    url(r'^rpc/obtainTicket.action', lcd_view.obtainTicket),
#     url(r'^', lcd_view.index1),
    # url(r'^grappelli/', include('grappelli.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
