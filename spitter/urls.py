"""spitter URL Configuration

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
from main import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^discover/$', views.discover, name='discover'),
    url(r'^feed/(?P<handle_name>[\w\-]+)/spitt$', views.feed_ajax_spitt, name='feed_ajax_spitt'),
    url(r'^feed/(?P<handle_name>[\w\-]+)/bio$', views.feed_ajax_bio, name='feed_ajax_bio'),
    url(r'^feed/(?P<handle_name>[\w\-]+)/img$', views.feed_ajax_img, name='feed_ajax_img'),
    url(r'^feed/(?P<handle_name>[\w\-]+)/follow$', views.feed_ajax_follow, name='feed_ajax_follow'),
    url(r'^feed/(?P<handle_name>[\w\-]+)/$', views.feed, name='feed'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^images/(?P<file_name>[^\\]*\.(\w+))$', views.getimage, name='getimage'),
    url(r'^admin/', admin.site.urls)
]
