# Router

## 使用

关于路由, 事实上, 它并不需要单独处理, 因为它已经成为了 API 的一个属性

也就是你在编写 API 时的 `@api_define` 中的第二个参数 `url` 

当然在编写之前, 你需要在你的项目根目录的 `urls.py` 中添加如下代码

```python
from django.conf.urls import url, include
from django.contrib import admin
from docs import router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include('docs.urls')),  # 此处为添加项, docs文档的路由, 包括登录注册和文档页面
]

urlpatterns += router.urls  # 将文档自动注册的路由添加到你项目的路由中
```

## 内部实现

关于 `Router` 的实现其实很简单, 其源代码如下 : 

```python
class Router(object):
    def __init__(self):
        self._registry = {}
        self.endpoints = []

    def register(self, **kwargs):
        view = kwargs['view']
        if self._registry.get(view.__module__) is None:
            self._registry[view.__module__] = [kwargs, ]
        else:
            self._registry[view.__module__].append(kwargs)

    def get_urls(self):
        """
        Return a list of URL patterns, given the registered apis.
        """
        from django.conf.urls import url

        settings_check()

        if not isinstance(settings.INSTALLED_HANDLERS, (list, tuple)):
            raise TypeError(_(
                'settings INSTALLED_HANDLERS should be list not %s' % type(settings.INSTALLED_HANDLERS)))

        for api in settings.INSTALLED_HANDLERS:
            import_string(api + '.__name__')
        urlpatterns = []
        for module, param in self._registry.items():
            m = import_string(module)
            for p in param:
                func, name, regex, params, headers, desc, display = p['view'], p['name'], p['url'], p[
                    'params'], p['headers'], p['desc'], p['display']
                view_name, method = func.__qualname__.split('.')
                # class
                view = getattr(m, view_name)
                if method not in view.http_method_names:
                    # method 不合法
                    raise type('HttpMethodError', (Exception,), {})(_('%s is not an HTTP method.' % method))

                method = force_str(method).upper()
                if regex.startswith('/'):
                    regex = regex.replace('/', '', 1)
                pattern = url(r'^%s$' % regex, csrf_exempt(view.as_view()), name=name)
                urlpatterns.append(pattern)
                if display:
                    for endpoint in self.endpoints:
                        if endpoint.path == simplify_regex(pattern.regex.pattern):
                            endpoint.methods.append(method)
                            # 如果已经存在则进行覆盖
                            endpoint.params[method], endpoint.headers[method] = params, headers
                            break
                    else:
                        endpoint = ApiEndpoint(pattern=pattern, method=method, headers=headers, params=params,
                                               name_parent=module, desc=desc)
                        if settings.AUTO_ADD_OPTIONS_METHOD:
                            if method != "OPTIONS":
                                endpoint.methods.append("OPTIONS")
                                endpoint.params["OPTIONS"], endpoint.headers[
                                    "OPTIONS"] = params_check(settings.DEFAULT_PARAMS), params_check(
                                    settings.DEFAULT_HEADERS)
                        self.endpoints.append(endpoint)
        return urlpatterns

    @property
    def urls(self):
        if not hasattr(self, '_urls'):
            self._urls = self.get_urls()
        return self._urls
```

当使用 `@api_define` 时, 会将注册路由需要的参数添加到 `self._registry` 中, 将所有的 `endpoint` 添加到 `self.endpoints` 中

这样 , 在使用 `urlpatterns += router.urls` 时, 就会将你注册的 `handler` 的路由一次性全部注册

关于 `api_define` 更多的信息你可以从 `decorators` 中获取