import traceback
import requests
import time
import re
import json
import hashlib
import xml.etree.ElementTree as et
from random import randint  # 随机函数
from pyquery import PyQuery as pq
import threading
from threading import Thread
import datetime
from selenium import webdriver
import ctypes
import inspect
from apscheduler.schedulers.blocking import BlockingScheduler
from pub_zqwz.logger import *

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080'
}

XML_TEXT = '<xml>' \
           '<ToUserName><![CDATA[{}]]></ToUserName>' \
           '<FromUserName><![CDATA[{}]]></FromUserName>' \
           '<CreateTime>{}</CreateTime>' \
           '<MsgType><![CDATA[text]]></MsgType>' \
           '<Content><![CDATA[{}]]></Content>' \
           '</xml>'

XML_IMGAGE = '<xml>' \
           '<ToUserName><![CDATA[{}]]></ToUserName>' \
           '<FromUserName><![CDATA[{}]]></FromUserName>' \
           '<CreateTime>{}</CreateTime>' \
           '<MsgType><![CDATA[image]]></MsgType>' \
           '<Image><MediaId><![CDATA[{}]]></MediaId></Image>' \
           '</xml>'

XML_NEWS = '''
          <xml>
          <ToUserName><![CDATA[{}]]></ToUserName>
          <FromUserName><![CDATA[{}]]></FromUserName>
          <CreateTime>{}</CreateTime>
          <MsgType><![CDATA[news]]></MsgType>
          <ArticleCount>1</ArticleCount>
          <Articles>
            <item>
              <Title><![CDATA[{}]]></Title>
              <Description><![CDATA[{}]]></Description>
              <PicUrl><![CDATA[{}]]></PicUrl>
              <Url><![CDATA[{}]]></Url>
            </item>
          </Articles>
        </xml>
        '''

HERO_BM_DICT = {
    "154": "木兰",
    "167": "猴子|猴哥",
    "168": "牛头|牛魔王",
    "130": "宫本",
    "116": "阿柯|阿珂",
    "113": "鱼",
    "126": "夏侯",
    "112": "鲁班|卤蛋",
    "132": "马可",
    "157": "火舞",
    "162": "娜可|露露",
    "163": "橘右君",
    "177": "狼狗",
    "184": "奶妈",
    "186": "太乙",
    "190": "诸葛",
    "111": "大小姐",
    "187": "东皇",
    "182": "干将",
    "193": "凯|恺",
    "196": "百里|守约",
    "195": "玄策",
    "502": "老虎",
    "513": "上官|婉儿",
    '511': '八戒',
    "312": "炸弹猫",
    '505': '谣|摇',
    '506': '走地鸡',
    '522': '耀|燿',
    '531': '静|境|竟',
    '527': '蒙括'
}

TIP_DICT = {
    'bz': '*小提示：发送“{}壁纸”可获取{}全皮肤壁纸，更多数据请直接发送英雄名查看哦',
    'jn': '*小提示：发送“{}技能”可快速了解{}技能介绍，更多数据请直接发送英雄名查看哦',
    'sl': '*小提示：发送“{}胜率”可查看{}最新胜率榜，更多数据请直接发送英雄名查看哦',
    'cz': '*小提示：发送“{}出装”可查看{}出装推荐，更多数据请直接发送英雄名查看哦',
    'mw': '*小提示：发送“{}铭文”可查看{}最新铭文搭配，更多数据请直接发送英雄名查看哦',
    'kz': '*小提示：发送“{}克制”可查看{}英雄克制关系，更多数据请直接发送英雄名查看哦',
    'js': '*小提示：发送“{}介绍”可查看{}的故事介绍，更多数据请直接发送英雄名查看哦',
    'zh': '*小提示：发送“{}组合”可查看{}双/三排组合推荐，更多数据请直接发送英雄名查看哦',
    'jq': '*小提示：发送“{}攻略”可查看{}打法攻略，更多数据请直接发送英雄名查看哦',
    'yy': '*小提示：发送“{}语音”可获取{}皮肤语音包，更多数据请直接发送英雄名查看哦',
}