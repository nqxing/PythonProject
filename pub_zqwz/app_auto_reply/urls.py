from django.conf.urls import url
from app_auto_reply.api import keys_admin, up_wz_wall, mon_news, up_wz_hero_info, add_wall, up_wz_item

urlpatterns = [
    url(r'^login/$', keys_admin.Login.as_view()),
    url(r'^var/(\w+)/$', keys_admin.VarList.as_view()),
    url(r'^(\d+)/$', keys_admin.UpKey.as_view()),
    url(r'^exitLogin/$', keys_admin.exit_login),
    url(r'^wz/$', keys_admin.KeyWZ.as_view()),
    url(r'^addwall/$', add_wall.AddWall.as_view()),
    url(r'^UPwz/$', up_wz_wall.UPWZWall.as_view()),
    url(r'^UPItem/$', up_wz_item.UPWZItem.as_view()),
    url(r'^MonNews/$', mon_news.MonNews.as_view()),
    url(r'^UPwzInfo/$', up_wz_hero_info.UPWZHeroInfo.as_view()),
    url(r'^$', keys_admin.Key.as_view()),
]