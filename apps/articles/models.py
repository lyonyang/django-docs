from django.db import models


# Create your models here.

class Article(models.Model):
    """
    文章
    """
    DELETE_CHOICES = (
        (1, '正常'),
        (0, '删除')
    )

    title = models.CharField(max_length=64, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.CharField(max_length=64, verbose_name='作者')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    delete_status = models.IntegerField(choices=DELETE_CHOICES, verbose_name='删除状态')

    class Meta:
        db_table = 'article'
