# 文档

文档相关的视图在 `docs.view` 中, 包括登录的账号密码也在其中, 你可以自行进行修改, 文档以 `API` 的 `py` 文件进行分类, 默认标题名称为 `py` 文件的文件名, 当然你也可以设置别名, 只需要在 `settings.py` 中添加如下配置: 

```python
INSTALLED_HANDLERS_NAME = {
    'api.article': '文章相关API',  
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