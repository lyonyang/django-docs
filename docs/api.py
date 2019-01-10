"""
该文件中不能导入使用全局导入 app 中的 model, 因为 app docs 是第一被加载的且必须为第一加载项 :
    1. model 与 App存在绑定关系, 必须 Install App 才能使用
    2. 为了使 api 能够自动进行注册路由, 在根目录的文件夹下的 urls.py 中进行自动加载
        - urls.py
            from docs import router
            urlpatterns += router.urls
        - urls.py 为Django自动加载项
        - 通过settings中的 INSTALLED_HANDLERS 设置需要加载的 api
"""

from functools import wraps
from rest_framework.views import APIView
from rest_framework.response import Response
from docs import router, Param
from docs.utils.jwt import JwtHandler


def api_define(name, url, params=[], desc='', headers=[]):
    if not headers:
        headers = [
            Param('authorization', False, 'str'),
            Param('channel', True, 'int', '1', '渠道'),
            Param('organ', True, 'int', '000001', '机构'),
        ]

    def foo(view):
        method = view.__name__
        router.register(view=view, name=name, url=url, params=params, method=method, desc=desc, headers=headers)

        @wraps(view)
        def inner(*args, **kwargs):
            return view(*args, **kwargs)

        return inner

    return foo


def login_required(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        user_id = JwtHandler.get_user_id(self.token, self.channel, self.organ)
        if not user_id:
            return Response({'code': -1, 'msg': '用户信息已失效, 请重新登录!'})
        if self.channel == '3':
            pass
        from apps.classroom.models.user import User
        self.user = User.objects.filter(id=user_id).first()
        self.user_id = self.user.id
        return method(self, *args, **kwargs)

    return wrapper


class BaseHandler(APIView):

    user = None
    user_id = None

    @property
    def ip(self):
        return self.get_request_ip()

    def get_request_ip(self):
        request = self.request
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        return ip

    def get_arg(self, name=None):
        if hasattr(self.request, self.request.method):
            args = getattr(self.request, self.request.method)
            if name is not None:
                args = args.get(name)
                if not args:
                    args = self.request.data.get(name)
                return args
        return None

    def files(self, name=None):
        if name is None:
            return self.request.FILES
        return self.request.FILES.get(name)

    def write(self, data=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
        return Response(data=data, status=status, template_name=template_name, headers=headers, exception=exception,
                        content_type=content_type)

    def set_user(self, user_id=None):
        authorization = self.request.META.get('HTTP_AUTHORIZATION') or ' '
        _, token = authorization.split(' ')
        user_id = user_id or JwtHandler.get_user_id(token, self.channel, self.organ)
        if user_id:
            from apps.classroom.models.user import User
            user = User.objects.filter(id=user_id).first()
            self.user_id = user_id
            self.user = user
            return True
        return False

    @property
    def token(self):
        authorization = self.request.META.get('HTTP_AUTHORIZATION') or ' '
        _, token = authorization.split(' ')
        return token

    @property
    def channel(self):
        return self.request.META.get('HTTP_CHANNEL')

    @property
    def organ(self):
        return self.request.META.get('HTTP_ORGAN')
