from random import randint  # 随机函数
from PIL import Image
from auto_reply.config.config import *
from auto_reply.config.fun_api import *
# 禁用安全请求警告 关闭SSL验证时用
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import traceback
import base64
import datetime
import threading
import time
import shutil
import os
import hashlib
import ctypes
import inspect
from threading import Thread
import xml.etree.ElementTree as et

from pyquery import PyQuery as pq
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from robot.models import pubVarList
import zipfile

# 2020.04.14新增包（解决获取饿了么sid需要滑动验证码）
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# linux系统安装该库失败，先注释掉 20201016
# import pyautogui as pg
import sqlite3