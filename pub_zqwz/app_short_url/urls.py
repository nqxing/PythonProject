from django.conf.urls import url
from app_short_url.views import addShortUrl, restoreUrl, rurl

urlpatterns = [
    url(r'^addShortUrl/$', addShortUrl),
    url(r'^restoreUrl/$', restoreUrl),
    url(r'^([A-Za-z0-9]+)/', rurl),
]