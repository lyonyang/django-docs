# django-api-docs

## 简介

django-api-docs 是一个用于构建Web API的工具:palm_tree:

Django 版本: 1.x

## 安装

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

将 `docs` 添加进 `INSTALLED_APPS` 这不是必要的, 当你使用 `python manage.py collectstatic` 整合静态文件, 且更换 `docs.templates` 中HTML文件的位置时, 你可以把它当做一个包

将 `docs` 注册进 `INSTALLED_APPS` 主要是为了 `Django` 能够找到我们的静态文件 , 当然还有一点就是, 这样更符合我们的习惯

## 快速开始

我们将使用 `django-api-docs` 编写一个简单的API, 以查看文库文章为例

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

同步数据库

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

接下来我们在 `api` 目录中创建 `article.py` , 你也可以像本项目`(django-api-docs)`一样, 在 `api` 目录中再创建一个 `handler` 目录来存放 `API` 文件, 在编写API之前我们先在 Model `Article` 中添加一个方法供我们使用 :

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
from artilces.models import Article

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
    'api.article',  # 本项目 api.handler.article
]
```

重新启动一下我们的项目, 再访问 `http://127.0.0.1:8000/docs` 

![first_api](https://raw.githubusercontent.com/lyonyang/django-api-docs/master/asset/first_api.png)

我们的第一个接口就这样写好了 , 接下来我们来使用这个文档看看 , 我们来发送 `GET` 请求

![request](https://raw.githubusercontent.com/lyonyang/django-api-docs/master/asset/request.png)


### 文档

文档相关的视图在 `docs.view` 中, 包括登录的账号密码也在其中, 你可以自行进行修改, 文档以 `API` 的 `py` 文件进行分类, 默认标题名称为 `py` 文件的文件名, 当然你也可以设置别名, 只需要在 `settings.py` 中添加如下配置: 

```python
INSTALLED_HANDLERS_NAME = {
    'api.article': '文章相关API',  # 本项目 api.handler.article
}
```

这样, 在文档中标题就会为 `文章相关API` 啦

所有默认配置如下: 

```python
# 注册的api
INSTALLED_HANDLERS = []

# 注册的api标题别名
INSTALLED_HANDLERS_NAME = {}

# 是否隐藏文档
HIDE_API_DOCS = False

# 自动添加options请求方法
AUTO_ADD_OPTIONS_METHOD = True

# 全局headers参数
DEFAULT_HEADERS = []

# 全局params参数
DEFAULT_PARAMS = []
```

### 关于API写法的问题


`BaseHandler` 是 `django.views` 中 `View` 的子类, 你需要继承它来编写你的 `api` .

装饰器 `@api_define` 负责注册路由, 以及将该 `API` 添加到 `API` 文档中, 其原型为 `api_define(name, url, params=None, headers=None, desc='', display=True)` , 参数说明如下:

-  `name` , 为 `django.conf.urls` 中 `url(regex, view, kwargs=None, name=None)` 函数的第四个参数 `name` , 可用于反向生成 URL  
-  `url`  , 即该接口的路由地址
- `params` 与 `headers` 为文档中请求所需要的参数
- `desc` , 为该接口的具体描述
- `display` , 是否在文档中显示该 `API`

在大体上, 它的写法与 Django 的 CBV 一致, 你也可以通过 Django 中注册路由的方式来生成路由, 不过这样, `API` 文档就失效了, 并且这种在 `urls.py` 中注册路由的方式也是比较麻烦的, 所以你应该使用 `@api_define` 来注册你的路由以及生成你的 `API` 文档

**编写方式建议**

因为通常我们写接口基本都是以单个为单位的, 所以对于一个 Class , 我们只会使用一个 `method`, 比如现在我们需要两个接口:

- 查看文章的接口  /article/detail
- 添加文章的接口  /article/add

**方式一:**

```python
import datetime
from docs import Param, BaseHandler, api_define
class ArticleDetail(BaseHandler):
    @api_define('article_detail', '/article/detail', [
        Param('article_id', True, 'int', '1', '文章ID'),
    ], desc='查看文章详情')
    def get(self, request):
        data = {
            'title': 'django-api-docs快速构建Web API',
            'content': '写接口效率要高, 姿势要帅, 没错~',
            'author': 'Lyon',
            'create_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return self.write({'return_code': 0, 'return_data': data})


class ArticleAdd(BaseHandler):
    @api_define('article_add', '/article/add', [
        Param('title', True, 'str', 'API Docs', '标题'),
        Param('content', True, 'str', '一个构建Web API的工具', '内容'),
        Param('author', True, 'str', 'Lyon', '作者'),
    ], desc='添加文章')
    def post(self, request):
        title = self.data.get('title')
        content = self.data.get('content')
        author = self.data.get('author')
        if not all((title, content, author)):
            return self.write({'return_code': 10000, 'return_msg': 'Invalid parameter.'})
        # TODO 创建一条文章数据
        return self.write({'return_code': 0, 'return_data': {}})
```

**方式二:**

```python
import datetime
from docs import Param, BaseHandler, api_define
class ArticleHandler(BaseHandler):
    @api_define('article_detail', '/article/detail', [
        Param('article_id', True, 'int', '1', '文章ID'),
    ], desc='查看文章详情')
    def get(self, request):
        data = {
            'title': 'django-api-docs快速构建Web API',
            'content': '写接口效率要高, 姿势要帅, 没错~',
            'author': 'Lyon',
            'create_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return self.write({'return_code': 0, 'return_data': data})

    @api_define('article_add', '/article/add', [
        Param('title', True, 'str', 'API Docs', '标题'),
        Param('content', True, 'str', '一个构建Web API的工具', '内容'),
        Param('author', True, 'str', 'Lyon', '作者'),
    ], desc='添加文章')
    def post(self, request):
        title = self.data.get('title')
        content = self.data.get('content')
        author = self.data.get('author')
        if not all((title, content, author)):
            return self.write({'return_code': 10000, 'return_msg': 'Invalid parameter.'})
        # TODO 创建一条文章数据
        return self.write({'return_code': 0, 'return_data': {}})
```

对于以上两种方式, 我通常会使用第一种方式编写API, 当然你也可以使用第二种方式, 但是一个 Class 只有一个 get, 一个 post ...

**注意: 在一个 Class 中, 如果出现了两次相同的 `method` , 后面的方法将会对前面的覆盖 , 因为路由注册的是调用的 `as_view()` , 而不是以函数为单位注册的**

```python
from docs import BaseHandler
class ArticleHandler(BaseHandler):

    def get(self, request):
        return self.write({'msg': '我是他的前身'})
    
    def get(self, request):
        return self.write({'msg': '我才是真正的get'})
```

**内部实现**

`BaseHandler` 继承于 `View` , 它主要新增了 `data` 属性和 `write()` 方法:

- data , `Django` 中你这么使用 `request.METHOD.get()` , 现在你这么使用 `self.data.get()`
- write(), 返回一个 `Response` 对象, 所以在你返回响应对象时, 你只需要直接 `return self.write(return_data)` 就行, 其中 `return_data` 为一串JSON数据
 
 如果你响应的数据为 XML 或其他, 你可以利用 `Django` 内置的 `HttpResponse` 等响应对象来实现你想达到的目的 , `self.write()` 默认响应的 `content_type` 为 `application/json`
 

## 后续

后续将会添加更加完整的DEMO , 以及使用该工具编写的项目流程, 本工具源码中有一些详细的注释, 更多信息你可以直接阅读代码哟, 如果你觉得用起来不错, 可以给本项目一个:tada: `Star` 哦.

当然如果你有什么问题或者建议也欢迎 `Issue`, 也可以直接联系我 QQ: 547903993  Email: lyon.yang@qq.com

详细使用文档会在近期更新完毕

