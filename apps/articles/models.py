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
    delete_status = models.IntegerField(default=1, choices=DELETE_CHOICES, verbose_name='删除状态')

    class Meta:
        db_table = 'article'

    def data(self):
        return {
            'article_id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }

    @classmethod
    def create_data(cls, title, content, author):
        obj = cls(title=title, content=content, author=author)
        try:
            obj.save()
        except Exception as e:
            # TODO log
            return
        return obj

    @classmethod
    def edit_data(cls, obj, title, content, author):
        obj.title = title
        obj.content = content
        obj.author = author
        try:
            obj.save()
        except Exception as e:
            # TODO log
            return
        return obj

    @classmethod
    def delete_data(cls, obj):
        try:
            obj.delete()
        except Exception as e:
            # TODO log
            return
        return True
