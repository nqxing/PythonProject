from django.db import models

class pubCardUsers(models.Model):
    bind_name = models.CharField(max_length=50, null=True)
    wx_open_id = models.CharField(max_length=200, null=True)
    wx_puid = models.CharField(max_length=50, null=True)
    wx_note = models.CharField(max_length=10, null=True)
    wx_name = models.CharField(max_length=30, null=True)
    qq = models.CharField(max_length=30, null=True)
    state = models.BooleanField(default=False)
    time_list = models.CharField(max_length=50, null=True)
    time_num = models.IntegerField(null=True)
    is_first = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "pub_card_users"

class pubCardHistory(models.Model):
    his_id = models.CharField(max_length=20)
    his_info = models.CharField(max_length=5000)
    class Meta:
        db_table = "pub_card_text_history"

class pubCardText(models.Model):
    text_id = models.IntegerField()
    text_info = models.CharField(max_length=50, null=True)
    text_story = models.CharField(max_length=500, null=True)
    week = models.IntegerField(null=True)
    holiday = models.CharField(max_length=50, null=True)
    is_holiday = models.BooleanField(default=False)
    class Meta:
        db_table = "pub_card_text"

class pubEleSignUsers(models.Model):
    bind_name = models.CharField(max_length=50, null=True)
    wx_open_id = models.CharField(max_length=200, null=True)
    wx_puid = models.CharField(max_length=50, null=True)
    wx_note = models.CharField(max_length=20, null=True)
    wx_name = models.CharField(max_length=30, null=True)
    qq = models.CharField(max_length=30, null=True)
    mobile = models.CharField(max_length=11, null=True)
    sid = models.CharField(max_length=150, null=True)
    user_id = models.CharField(max_length=50, null=True)
    state = models.BooleanField(default=False)
    is_bind = models.BooleanField(default=False)
    is_sign = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "pub_ele_sign_users"

class pubEleSignVdtoken(models.Model):
    wx_open_id = models.CharField(max_length=200)
    mobile = models.CharField(max_length=11)
    vdtoken = models.CharField(max_length=500)
    class Meta:
        db_table = "pub_ele_sign_vdtoken"

class pubEleSignCode(models.Model):
    wx_open_id = models.CharField(max_length=200)
    sms_code = models.CharField(max_length=6, default="0")
    is_send = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "pub_ele_sign_hd_code"

class pubEleHBRecord(models.Model):
    bianhao = models.IntegerField()
    name = models.CharField(max_length=50, null=True)
    amount = models.CharField(max_length=10, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    esource = models.CharField(max_length=10, null=True)
    class Meta:
        db_table = "pub_ele_hb_record"

class pubEleGroupSn(models.Model):
    bianhao = models.CharField(max_length=11, null=True)
    group_sn = models.CharField(max_length=100, null=True)
    yet = models.IntegerField(default=0)
    yet_max = models.IntegerField(default=0)
    url = models.CharField(max_length=200, null=True)
    state = models.BooleanField(default=False) #是否已红包退出监控，False为没有
    from_name = models.CharField(max_length=20, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    up_time = models.DateTimeField(auto_now=True, null=True)
    retrys = models.IntegerField(null=True)
    is_send = models.BooleanField(default=False, null=True) #是否已发送给红包来源人，False为没有
    class Meta:
        db_table = "pub_ele_group_sn"

class pubEleID(models.Model):
    mobile = models.CharField(max_length=20)
    open_id = models.CharField(max_length=200)
    sign = models.CharField(max_length=200)
    sid = models.CharField(max_length=200)
    mob_url = models.CharField(max_length=200, null=True)
    qq = models.CharField(max_length=20, null=True)
    qq_pwd = models.CharField(max_length=30, null=True)
    is_five = models.BooleanField(default=False, null=True) #是否已领取五次
    user_id = models.CharField(max_length=50, null=True)
    is_cb = models.BooleanField(default=False, null=True) #账号是否可以拆包
    id_info = models.CharField(max_length=50, null=True)  # 账号状态信息
    time_stamp = models.BigIntegerField(null=True)  # 账号毫秒时间戳 排序用
    class Meta:
        db_table = "pub_ele_id"

class pubEleSignInfo(models.Model):
    wx_open_id = models.CharField(max_length=200)
    sign_info = models.CharField(max_length=500)
    sign_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "pub_ele_sign_info"

class pubEleTXUrls(models.Model):
    url = models.CharField(max_length=500)
    name = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "pub_ele_tx_urls"

class pubSMSList(models.Model):
    mobile = models.CharField(max_length=50)
    mobile_url = models.CharField(max_length=500)
    note = models.CharField(max_length=100, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "pub_sms_list"

class pubBindUsers(models.Model):
    bind_name = models.CharField(max_length=50, null=True)
    wx_open_id = models.CharField(max_length=200, null=True)
    is_bind = models.BooleanField(default=False)
    wx_note = models.CharField(max_length=20, null=True)
    qq = models.CharField(max_length=20, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "pub_bind_users"

class pubVIPUsers(models.Model):
    wx_puid = models.CharField(max_length=50)
    wx_note = models.CharField(max_length=10)
    wx_name = models.CharField(max_length=30)
    num = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "pub_vip_users"

class pubVarList(models.Model):
    var_name = models.CharField(max_length=20, unique=True)
    var_info = models.CharField(max_length=2000)
    note = models.CharField(max_length=100, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "pub_var_list"

class pubWZHeroName(models.Model):
    hero_id = models.IntegerField()
    hero_name = models.CharField(max_length=20)
    hero_name_bm = models.CharField(max_length=20, null=True)
    # 每次修改都会自动更新时间
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "pub_wz_hero_name"

# 王者荣耀全英雄胜率表
class pubWZwinRate(models.Model):
    cx_name = models.CharField(max_length=200)
    cx_value = models.CharField(max_length=5000)
    hero_name = models.CharField(max_length=20)
    hero_id = models.IntegerField()
    update_time_str = models.CharField(max_length=20)
    # 每次修改都会自动更新时间
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "pub_wz_win_rate"

# 王者荣耀全英雄技能介绍表
class pubWZSkill(models.Model):
    cx_name = models.CharField(max_length=200)
    cx_value = models.CharField(max_length=5000)
    hero_name = models.CharField(max_length=20)
    hero_id = models.IntegerField()
    # 每次修改都会自动更新时间
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "pub_wz_skill"

# 王者荣耀全英雄核心出装表
class pubWZEquip(models.Model):
    cx_name = models.CharField(max_length=200)
    cx_value = models.CharField(max_length=5000)
    cx_value1 = models.CharField(max_length=5000)
    hero_name = models.CharField(max_length=20)
    hero_id = models.IntegerField()
    # 每次修改都会自动更新时间
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "pub_wz_equip"

# 王者荣耀全英雄铭文搭配表
class pubWZRune(models.Model):
    cx_name = models.CharField(max_length=200)
    cx_value = models.CharField(max_length=5000)
    hero_name = models.CharField(max_length=20)
    hero_id = models.IntegerField()
    # 每次修改都会自动更新时间
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "pub_wz_rune"

# 王者荣耀全英雄克制关系表
class pubWZKZ(models.Model):
    cx_name = models.CharField(max_length=200)
    cx_value = models.CharField(max_length=5000)
    hero_name = models.CharField(max_length=20)
    hero_id = models.IntegerField()
    # 每次修改都会自动更新时间
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "pub_wz_kz"

# 王者荣耀全英雄组合关系表
class pubWZZH(models.Model):
    cx_name = models.CharField(max_length=200)
    cx_value = models.CharField(max_length=5000)
    hero_name = models.CharField(max_length=20)
    hero_id = models.IntegerField()
    # 每次修改都会自动更新时间
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "pub_wz_zh"

# 王者荣耀全英雄人物介绍表
class pubWZIntroduce(models.Model):
    cx_name = models.CharField(max_length=200)
    cx_value = models.CharField(max_length=5000)
    hero_name = models.CharField(max_length=20)
    hero_id = models.IntegerField()
    # 每次修改都会自动更新时间
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "pub_wz_introduce"

# 王者荣耀全英雄技巧使用表
class pubWZSkills(models.Model):
    cx_name = models.CharField(max_length=200)
    cx_value = models.CharField(max_length=5000)
    hero_name = models.CharField(max_length=20)
    hero_id = models.IntegerField()
    # 每次修改都会自动更新时间
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "pub_wz_skills"