# django-api-docs

## 简介

django-api-docs 是一个用于构建Web API的工具:palm_tree:

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

## 使用方法

你可以直接fork本项目代码, 通过 `python manage.py runserver` 命令来进行测试使用.

### API

这是一个 `API` 的示例:

```python
from docs import Param, BaseHandler, api_define
from apps.articles.models import Article
from api.status import CODE, MSG
# 获取文章列表
class ArticleList(BaseHandler):
    @api_define('article_list', '/article/list', desc='文章列表')
    def get(self, request):
        articles = Article.objects.all().order_by('create_time')
        data = []
        for article in articles:
            data.append(article.data())
        return self.write({'return_code': CODE.SUCCESS, 'return_data': data})
```

`BaseHandler` 是 `django.views` 中 `View` 的子类, 你需要继承它来编写你的 `api` .

装饰器 `@api_define` 负责注册路由, 以及将该 `API` 添加到 `API` 文档中, 其原型为 `api_define(name, url, params=None, headers=None, desc='', display=True)` , 参数说明如下:

-  `name` , 为 `django.conf.urls` 中 `url(regex, view, kwargs=None, name=None)` 函数的第四个参数 `name` , 可用于反向生成 URL  
-  `url`  , 即该接口的路由地址
- `params` 与 `headers` 为文档中请求所需要的参数
- `desc` , 为该接口的具体描述
- `display` , 是否在文档中显示该 `API`

在大体上, 它的写法与 Django 的 CBV 一致, 你也可以通过 Django 中注册路由的方式来生成路由, 不过这样, `API` 文档就失效了, 并且这种在 `urls.py` 中注册路由的方式也是比较麻烦的, 所以你应该使用 `@api_define` 来注册你的路由以及生成你的 `API` 文档

### 路由注册

很简单, 你只需要在 `urls.py` 中添加如下两行: 

```python
from docs import router
urlpatterns += router.urls
```

这样你的路由就注册成功了, 当然文档的 URL 是额外的, 所以, `urls.py` 中的所有代码应该是这样的: 

```python
from django.conf.urls import url, include
from django.contrib import admin
from docs import router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include('docs.urls')), # 文档url
]

urlpatterns += router.urls
```

当然, 这还没有完, 还有一个重要的步骤, 那就是注册 API, 即在 `settings.py` 中添加你需要注册的那些 API:

```python
INSTALLED_HANDLERS = [
    'api.handler.article',
]
```

这样, 它就会在加载时, 自动去注册 `article.py` 中的所有 `API` , 也就是说, 以后你只需要在 `INSTALLED_HANDLERS` 中来逐步添加以 `.` 连接的绝对路径的 `py` 文件, 你的 `API` 就可以无限的进行下去了

### 文档

文档相关的视图在 `docs.view` 中, 包括登录的账号密码也在其中, 你可以自行进行修改, 文档以 `API` 的 `py` 文件进行分类, 默认标题名称为 `py` 文件的文件名, 当然你也可以设置别名, 只需要在 `settings.py` 中添加如下配置: 

```python
INSTALLED_HANDLERS_NAME = {
    'api.handler.article': '文章相关API',
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

## 后续

后续将会添加更加完整的DEMO , 以及使用该工具编写的项目流程, 本工具源码中有一些详细的注释, 更多信息你可以直接阅读代码哟, 如果你觉得用起来不错, 可以给本项目一个:tada: `Star` 哦.

当然如果你有什么问题或者建议也欢迎 `Issue`, 也可以直接联系我 QQ: 547903993  Email: lyon.yang@qq.com

详细使用文档会在近期更新完毕

