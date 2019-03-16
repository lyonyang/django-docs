# Settings

## 介绍

关于 `django-api-docs` 中的所有配置 , 在 `docs.settings.py` 你可以看到详细的列表

下面我会进行一一说明

## INSTALLED_HANDLERS

`INSTALLED_HANDLERS` 为一个 `list` 或者 `tuple` , 它的元素为一个以 `.` 连接的 `py` 文件绝对路径 , 即要注册的 `handler` , 你可以将 `handler` 理解为 `Django` 中的 `views.py` 

示例

```python
INSTALLED_HANDLERS = [
    'api.handler.article',
]
```

默认为空列表 `INSTALLED_HANDLERS = []` 

## INSTALLED_HANDLERS_NAME

`INSTALLED_HANDLERS_NAME` 是一个 `dict` , 其中元素以 `INSTALLED_HANDLERS` 中元素为 `key` , `value` 为需要在文档上显示的别名

默认注册的 `handler` 在文档中其名称为 `handler` 文件名 , 你可以在 `INSTALLED_HANDLERS_NAME` 中来添加别名

示例

```python
INSTALLED_HANDLERS_NAME = {
    'api.handler.article': '文章相关API'
}
```

默认为空 `INSTALLED_HANDLERS_NAME = {}`

## HIDE_API_DOCS

`HIDE_API_DOCS` 默认为 `False` 

即默认不隐藏文档 , 为了数据安全在正式环境中你应该将其设置为 `True` , 或者你也可以通过添加 `DOCS_ALLOWED_HOSTS` 来指定可访问主机

## AUTO_ADD_OPTIONS_METHOD

`AUTO_ADD_OPTIONS_METHOD` 默认为 `True` 

通常我们用不到 `OPTIONS` 请求 , 不过浏览器会进行预检 , 就会发送 `OPTIONS` 请求 , 该配置为是否自动在文档中添加 `OPTIONS` 按钮 , 以供我们测试使用 , 如果你不需要可以将其设置成 `False` 

## DEFAULT_HEADERS

全局的 `headers` 参数 , 即请求默认需要的 `headers` , 这将会在你的每个 API 中添加你所设置的 `headers` , 即在文档中显示的 `headers` 

它是一个 `list` , 其元素为一个 `tuple` 或者 `Param` 对象

```python
DEFAULT_HEADERS = [
    ('authorization', False, 'str', '', 'Token'),
]
# 或者
DEFAULT_HEADERS = [
    Param('authorization', False, 'str', '', 'Token'),
]
```

## DEFAULT_PARAMS

与 `DEFAULT_HEADERS` 一样 , 为全局的 `params` 参数 , 设置后文档上所有的 API 中都会添加

```python
DEFAULT_PARAMS = [
    ('platform', False, 'str', '', '平台'),
]
# 或者
DEFAULT_PARAMS = [
    Param('platform', False, 'str', '', '平台'),
]
```

## DOCS_USERNAME and DOCS_PASSWORD

`DOCS_USERNAME` 和 `DOCS_PASSWORD` 分别为文档管理员账号的用户名和密码

默认 `DOCS_USERNAME = DOCS_PASSWORD = 'admin'` 

## DOCS_ALLOWED_HOSTS

设置允许访问的主机地址 , 默认 `DOCS_ALLOWED_HOSTS = ["*"]` , 即允许所有主机访问

