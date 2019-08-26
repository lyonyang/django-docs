# Django Docs

![django-version](https://img.shields.io/badge/django%20version-1.x-blue.svg)
![python-version](https://img.shields.io/badge/python-3.4%2C%203.5%2C%203.6-blue.svg)
![django-docs](https://img.shields.io/badge/django--docs-2.1.0-blue)


## 安装

```shell
$ pip install django-apidocs
```

## 快速开始

在 `settings.py` , `INSTALLED_APPS` 添加 `django_docs`

```python
INSTALLED_APPS = [
    '...',
    'django_docs'
]
```

在项目根 `urls.py` 中, 添加文档路由

```python
url(r'^django_docs/', include('django_docs.urls')),
```

启动项目, 访问 `ip:port/django_docs/login/` , 输入任意用户名密码登录

## 编写API

新建目录与文件 `api/article.py` 


使用原始的 `View` 与 `JsonResponse`

```python
from django_docs import docs_define
from django.views import View
from django.http import JsonResponse

class ArticleList(View):
    @docs_define('/article/list', desc='文章列表')
    def get(self, request):
        data = [
            {
                'title': 'django-docs',
                'author': 'lyon',
                'content': 'This is a Django application. Help you build Web API quickly.'
            },
            {
                'title': 'django-docs-desc',
                'author': 'lyon',
                'content': 'Efficient, Simple and Flexible.'
            }

        ]
        return JsonResponse(data, safe=False)
```

使用 `BaseHandler`

```python
from django_docs import docs_define, BaseHandler

class ArticleList(BaseHandler):
    @docs_define('/article/list', desc='文章列表')
    def get(self, request):
        data = [
            {
                'title': 'django-docs',
                'author': 'lyon',
                'content': 'This is a Django application. Help you build Web API quickly.'
            },
            {
                'title': 'django-docs-desc',
                'author': 'lyon',
                'content': 'Efficient, Simple and Flexible.'
            }

        ]
        return self.write(data)
```

注册 `article.py` 

```python
# settings.py

INSTALLED_HANDLERS = [
    'api.article', 
]
```

刷新文档

