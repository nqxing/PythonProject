from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.Login.as_view()),
    url(r'^robot/$', views.KeyRobot.as_view()),
    url(r'^var/(\w+)/$', views.VarList.as_view()),
    url(r'^(\d+)/$', views.UpKey.as_view()),
    url(r'^exitLogin/$', views.exit_login),
    url(r'^$', views.Key.as_view()),
]