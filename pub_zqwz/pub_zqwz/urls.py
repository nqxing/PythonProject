"""pub_zqwz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from app_auto_reply.views import auto_reply

#以下3个包生产环境开启
from django.conf.urls import url
# 导入server服务
from django.views.static import serve
from pub_zqwz.settings import STATIC_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autoReply/', auto_reply),
    path('key/', include('app_auto_reply.urls')),
    path('s/', include('app_short_url.urls')),
    # 以下生产环境开启
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT})
]
