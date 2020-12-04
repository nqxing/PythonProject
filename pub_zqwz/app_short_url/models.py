from django.db import models

# Create your models here.
# 短url表
class ShortUrl(models.Model):
    id = models.AutoField(primary_key=True)
    # 短url
    short_url = models.CharField(max_length=255)
    # 原始url
    ori_url = models.TextField()
    # 短url有效期
    period = models.DateTimeField()

    def __str__(self):
        return self.short_url

    class Meta:
        db_table = "pub_short_url"