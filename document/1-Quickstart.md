
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

