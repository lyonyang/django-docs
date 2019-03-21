# django-api-docs

![django-version](https://img.shields.io/badge/django%20version-1.x-blue.svg)
![python-version](https://img.shields.io/badge/python-3.4%2C%203.5%2C%203.6-blue.svg)
![django-api-docs](https://img.shields.io/badge/django--api--docs-0.1.0-blue.svg)

## 简介

django-api-docs 是一个用于构建Web API的工具:palm_tree:

在 Django 中, 最有名气的 RESTful 工具应该就是 `django-rest-framework` 了, 我曾经也用过一段时间 , 但是渐渐的 , 我发现它让我的工作变得越来越复杂 , 整个项目看起来是那么的乱 , API 不应该太过于遵循 REST 规范 , `Serializer` 局限性太大了 , `Authentication` 必须得有那么一个 User 让我真是纳闷 , 构建 Web API 更是让人感到鸡肋 …… 

基于种种的原因 , 我实在是不想再用它了 , 当然它的技术层次还是很棒的 , 可能由于作者是国外的 , 也许国外编写 API 的方式和国内太不一样

在写这个工具之前 , 我其实已经完成了一半 , 用在了我公司的项目中 , 不过那时并没有完全抛弃 `django-rest-framwork` , 而是两者掺半 , 到现在完全剔除并更进一步的优化 , 成为了这个 `django-api-docs` 

**示例**


&lt;video id="video" controls="" controls autoplay="autoplay" poster="https://raw.githubusercontent.com/lyonyang/django-api-docs/master/asset/demo.png"&gt;
      &lt;source id="mp4" src="https://raw.githubusercontent.com/lyonyang/django-api-docs/master/asset/demo.mov" type="video/mp4"&gt;
&lt;/video&gt;


## 快速开始

### 安装

`django-api-docs` 是一个 `Django` 的应用, 所以你可以将 `docs` 目录复制进你的项目中, 随后: 

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'docs',  # or docs.apps.DocsConfig
    ...  # your apps
]
```

将 `docs` 添加进 `INSTALLED_APPS` 这不是必要的, 当你使用 `python manage.py collectstatic` 整合静态文件, 且更换 `docs.templates` 中HTML文件的位置时, 你可以把它当做一个包 , 因为这个时候他已经没有了 Django 的样子

将 `docs` 注册进 `INSTALLED_APPS` 主要是为了 `Django` 能够找到我们的静态文件 , 当然还有一点就是, 这样更符合我们的习惯

我们将使用 `django-api-docs` 编写一个简单的API, 以查看文库文章为例 , 其源代码在该项目的 `quickstart` 中

### 创建项目

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

同步数据库 , 因为Docs的登录暂时使用到的 `Django` 内置的 `session` 表 , 后续将会添加 `JWT`

```python
➜  ~ python manage.py makemigrations
➜  ~ python manage.py migrate
```

### 添加Docs应用

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

![login](https://raw.githubusercontent.com/lyonyang/django-api-docs/master/asset/login.png)

默认用户名和密码均为 `admin` 

![default_docs](https://raw.githubusercontent.com/lyonyang/django-api-docs/master/asset/default_docs.png)

### 编写API

创建一个 `api` 目录来编写我们的 API

```shell
# 在根目录创建api目录
➜  ~ mkdir api
```

接下来我们在 `api` 目录中创建 `article.py` , 在编写API之前我们先在 Model `Article` 中添加一个 `serialize()` 方法供我们获取对象数据用 :

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
        
    def serialize(self):
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
from artilces.models import Article

class ArticleList(BaseHandler):
    @api_define('article_list', '/article/list', headers=[('authorization', False, 'str', '', 'Token'), ], desc='文章列表')
    def get(self, request):
        articles = Article.objects.all().order_by('create_time')
        data = []
        for article in articles:
            data.append(article.serialize())
        return self.write({'return_code': 'success', 'return_data': data})
```

API虽然写好了, 但是我们还需要指定加载这个`api.article.py` , 在 `settings` 中添加以下配置 : 

```python
INSTALLED_HANDLERS = [
    'api.article',  
]
```

重新启动一下我们的项目, 再访问 `http://127.0.0.1:8000/docs` 

![first_api](https://raw.githubusercontent.com/lyonyang/django-api-docs/master/asset/first_api.png)

我们的第一个接口就这样写好了 , 但是现在文库里没有任何数据 , 我们再下一个添加文章的接口

```python
class ArticleAdd(BaseHandler):
    @api_define('article_add', '/article/add', [
        ('title', True, 'str', 'API Docs', '标题'),
        ('content', True, 'str', '一个构建Web API的工具', '内容'),
        ('author', True, 'str', 'Lyon', '作者'),
    ], [
        ('authorization', False, 'str', '', 'Token'),
    ],desc='添加文章')
    def post(self, request):
        title = self.data.get('title')
        content = self.data.get('content')
        author = self.data.get('author')
        if not all((title, content, author)):
            return self.write({'return_code': 'error', 'return_msg': 'Invalid parameter.'})
        article = Article.objects.create(title=title, content=content, author=author)
        if not article:
            return self.write({'return_code': 'fail', 'return_msg': 'fail'})
        return self.write({'return_code': 'success', 'return_data': {'article_id': article.id}})
```

重新启动我们的项目

![second_api](https://raw.githubusercontent.com/lyonyang/django-api-docs/master/asset/second_api.png)

接下来我们来使用这个文档看看 , 添加一条文章数据 : 

![article_add](https://raw.githubusercontent.com/lyonyang/django-api-docs/master/asset/article_add.png)

我们再获取文章列表

![request](https://raw.githubusercontent.com/lyonyang/django-api-docs/master/asset/request.png)

两个 API 编写完毕 , 是不是很简单呢 ~

## 支持与建议

如果你认为本工具不错 , 可以给本项目一个:tada: `Star` 哟.

本工具代码量很少 , 使用时你也可以直接看 `docs` 中的源代码来获取你想要的一些信息

当然如果你有什么问题或者建议也欢迎 `Issue`, 也可以直接联系我 

QQ: 547903993    Email: lyon.yang@qq.com



