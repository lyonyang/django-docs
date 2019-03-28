# 认证

关于认证 , 你在 `django-rest-framework` 中可以看到 , 它是使用 `contrib.auth` 中的 `User` 来实现的 , 而在 `django` 中它是通过 `login_required` 来使用的

但是我们知道 , 他的用法是如果认证未通过 , 则重定向到登录页面 , 这不符合我们的使用 , API 就是为前后端分离准备的 , 我们不需要页面 , 我们需要的是当前的 `User` 数据

我希望我们编写 API 的方式更加简单 , 直观 , 所以这里可能需要你根据你的项目需求来编写你所需要的逻辑

## 定义你的login_required

这个装饰器的功能其实就相当你的登录 API , 通常我们会以 `token` 或者 `session` 又或者 `cookie` 的方式来使用 , 只不过为了方便使用 , 你应该再做一些其他的操作 , 以下分别以 `session` 和 `jwt` 为例: 

### Session

你可以在你的 `API` 目录下新建一个 `decorators.py` 来存放你的 `login_required` , 当然你也可以直接在 `docs.decorators.py` 中修改

```python

def login_required(handler):
    from functools import wraps
    @wraps(handler)
    def _wrapped_view(self, *args, **kwargs):
        if self.request.session.get('user'):
            # 这里建议你直接设置你的User对象
            # 我的项目中基本都会使用user, user_id, 所以我这里会设置两项
            # self.user = User.objects.filter(username=username).first()
            # self.user = self.user.id
            # 所以在你必须登录的API中, 你可以随意使用self.user, self.user_id
            self.user = self.request.session.get('user')
        else:
            return self.write({'return_code': 'Fail', 'return_msg': 'Unauthorized'})
        return handler(self, *args, **kwargs)
        
    return _wrapped_view

```

我们在我们的 `api.handler.article.py` 来使用我们的 `login_required` 

```python
class ArticleList(BaseHandler):
    @api_define('article_list', '/article/list', desc='文章列表')
    # 进行认证
    @login_required
    def get(self, request):
        articles = Article.objects.all().order_by('create_time')
        data = []
        for article in articles:
            data.append(article.data())
        return self.write({'return_code': CODE.SUCCESS, 'return_data': data})
```

为此 , 我在 `api.handler.user.py` 中已经写好了一个登录设置 `session` 的示例 , 你可以通过它进行测试

如果没有登录 , 则会返回 `{"return_code":"Fail", "return_msg":"Unauthorized"}`

### JWT

同上 , 只是逻辑有所改变

```python
def login_required(handler):
    from functools import wraps
    @wraps(handler)
    def _wrapped_view(self, *args, **kwargs):
        import jwt
        authorization = self.request.META.get('HTTP_AUTHORIZATION') or ' '
        _, token = authorization.split(' ')
        
        def get_payload():
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, options={'verify_exp': False})
                return payload
            except jwt.ExpiredSignatureError:
                # token 过期
                return 
            except jwt.InvalidTokenError:
                # token 无效
                return 
        
        if not get_payload():
            return self.write({'return_code': 'Fail', 'return_msg': 'Unauthorized'})
        
        # 这里建议你直接设置你的User对象
        # 我的项目中基本都会使用user, user_id, 所以我这里会设置两项
        # self.user = User.objects.filter(username=username).first()
        # self.user = self.user.id
        # 所以在你必须登录的API中, 你可以随意使用self.user, self.user_id
        self.user = get_payload()['data']['user']
        return handler(self, *args, **kwargs)
        
    return _wrapped_view
```

同样的 , 在 `api.handler.user.py` 中已经写好了一个登录获取 `token` 的示例 , 你可以通过它进行测试

**在这个 `login_required` 中 , 你所看到的 `self` 就是 `BaseHandler Object` , 所以你可以在这里使用 `BaseHandler` 以及它的基类 `View` 的一切方法与属性**

