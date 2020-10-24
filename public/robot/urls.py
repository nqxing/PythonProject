from django.conf.urls import url
from robot.views import up_wz_wall, wall, up_lol_wall, wall_zip
from robot.views import mon_news
from robot.views import auto_hongbao, up_wz_hero_info

urlpatterns = [
    url(r'^UPwz/$', up_wz_wall.UPWZWall.as_view()),
    url(r'^UPlol/$', up_lol_wall.UPLOLWall.as_view()),
    url(r'^ZIPwall/$', wall_zip.ZIPWall.as_view()),
    url(r'^MonNews/$', mon_news.MonNews.as_view()),
    url(r'^AThongbao/$', auto_hongbao.AThongbao.as_view()),
    url(r'^UPwzInfo/$', up_wz_hero_info.UPWZHeroInfo.as_view()),
    url(r'^$', wall.Wall.as_view()),
]