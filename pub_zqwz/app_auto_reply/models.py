from django.db import models

class pubWZWall(models.Model):
    skin_name = models.CharField(max_length=20)
    skin_url = models.CharField(max_length=500)
    hero_name = models.CharField(max_length=10, null=True)
    hero_name_bm = models.CharField(max_length=50, null=True)
    hero_id = models.IntegerField(null=True)
    skin_short_url = models.CharField(max_length=100)
    mob_skin_url = models.CharField(max_length=500, null=True)
    mob_skin_short_url = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "pub_wz_wall"

class pubWZVoice(models.Model):
    hero_name = models.CharField(max_length=100)
    voice_url = models.CharField(max_length=200)

    class Meta:
        db_table = "pub_wz_voice"

class pubWZNews(models.Model):
    doc_id = models.CharField(max_length=50)
    news_title = models.CharField(max_length=200)
    news_title_url = models.CharField(max_length=200)

    class Meta:
        db_table = "pub_wz_news"

class pubKeys(models.Model):
    key = models.CharField(max_length=200, unique=True)
    key_info = models.CharField(max_length=2000)

    class Meta:
        db_table = "pub_keys"

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

# 王者荣耀装备、铭文图标
class pubWZItem(models.Model):
    cx_name = models.CharField(max_length=20)
    cx_value = models.CharField(max_length=300)
    # 每次修改都会自动更新时间
    update_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "pub_wz_item"