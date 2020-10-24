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

class pubLOLWall(models.Model):
    skin_name = models.CharField(max_length=50)
    skin_url = models.CharField(max_length=500)
    hero_name = models.CharField(max_length=10, null=True)
    hero_id = models.IntegerField(null=True)
    skin_short_url = models.CharField(max_length=100, null=True)
    skin_size = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "pub_lol_wall"

class pubLOLNews(models.Model):
    doc_id = models.CharField(max_length=150)
    news_title = models.CharField(max_length=200)
    news_title_url = models.CharField(max_length=200)

    class Meta:
        db_table = "pub_lol_news"

class pubKeys(models.Model):
    key = models.CharField(max_length=200, unique=True)
    key_info = models.CharField(max_length=2000)

    class Meta:
        db_table = "pub_keys"

class pubIdentID(models.Model):
    api_key = models.CharField(max_length=200)

    class Meta:
        db_table = "pub_ident_id"