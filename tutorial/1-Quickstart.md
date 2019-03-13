# 快速开始

我们将使用 `django-api-docs` 编写一个简单的API, 以查看文库文章为例

## 创建项目

创建项目与应用

```shell
# 创建项目目录
➜  ~ django-admin.py startapp quickstart
➜  ~ cd quickstart
# 创建应用
➜  ~ python3 manage.py startapp articles
```

注册APP

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'articles',
]
```

在 `articles.models` 中添加Model

```python
class Article(models.Model):
    """
    文库
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
```

同步数据库

```python
➜  ~ python manage.py makemigrations
➜  ~ python manage.py migrate
```

## 添加Docs应用

将项目中 `docs` 目录放入 `quickstart` 项目根目录中 , 并注册APP

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'docs', # 推荐放在用户应用的最上层
    'articles',
]
```

添加路由

```python
from django.conf.urls import url, include
from django.contrib import admin
from docs import router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include('docs.urls')),
]

urlpatterns += router.urls
```

现在就可以启动项目了

```python
➜  ~ python3 manage.py runserver 0.0.0.0:8000
```

随后访问 `http://127.0.0.1:8000/docs/login` , 因为我们需要先登录才能看到文档 

![login]([https://github.com/lyonyang/django-api-docs/blob/master/asset/login.png])

默认用户名和密码均为 `admin` 

![default_docs]([https://github.com/lyonyang/django-api-docs/blob/master/asset/default_docs.png])

## 编写API

创建一个 `api` 目录来编写我们的 API

```shell
# 在根目录创建api目录
➜  ~ mkdir api
```

接下来我们在 `api` 目录中创建 `article.py` , 编写一个查看文库中所有文件的 API , 在这之前我们先在 Model `Article` 中添加一个方法供我们使用 :

```python
# articles.models
class Article(models.Model):
    """
    文库
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
        
	# 获取对象属性
    def data(self):
        return {
            'article_id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }
```

接下来, 看我们的第一个API :

```python
from docs import Param, BaseHandler, api_define
from apps.articles.models import Article

class ArticleList(BaseHandler):
    @api_define('article_list', '/article/list', desc='文章列表')
    def get(self, request):
        articles = Article.objects.all().order_by('create_time')
        data = []
        for article in articles:
            data.append(article.data())
        return self.write({'return_code': 'success', 'return_data': data})
```

API虽然写好了, 但是我们还需要制定加载这个`api.article.py` , 在 `settings` 中添加以下配置 : 

```python
INSTALLED_HANDLERS = [
    'api.article',
]
```

重新启动一下我们的项目, 再访问 `http://127.0.0.1:8000/docs` 

![first_api]([https://github.com/lyonyang/django-api-docs/blob/master/asset/first_api.png])

我们的第一个接口就这样写好了 , 接下来我们来使用这个文档看看 , 我们来发送 `GET` 请求

![request]([https://github.com/lyonyang/django-api-docs/blob/master/asset/request.png])

更多说明请看其他文档

 

 