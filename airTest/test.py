# -*- encoding=utf8 -*-

__author__ = "Administrator"

from airtest.core.api import *

auto_setup(__file__)

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

poco(name="QQ").click()
poco(text="联系人").click()
poco(name="com.tencent.mobileqq:id/ivTitleBtnRightImage").click()
poco(text="QQ号/手机号/群/公众号").click()
poco(name="com.tencent.mobileqq:id/et_search_keyword").set_text("541116212")
poco(text="找人:").click()
poco(text="发消息").click()
poco(name="com.tencent.mobileqq:id/input").set_text("这是测试！")
poco(text="发送").click()
