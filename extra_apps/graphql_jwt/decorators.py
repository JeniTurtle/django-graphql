from functools import wraps
import logging

from django.contrib.auth import authenticate, get_user_model
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from promise import Promise, is_thenable

from . import exceptions
from .shortcuts import get_token

__all__ = [
    'user_passes_test',
    'login_required',
    'staff_member_required',
    'permission_required',
    'token_auth',
]


def context(f):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                info = args[f.__code__.co_varnames.index('info')]
            except Exception:
                try:
                    info = args[f.__code__.co_varnames.index('self')]
                except Exception:
                    raise Exception("请传入正确的参数")
                
            if hasattr(info, 'context'):
                cont = info.context
            elif hasattr(info, 'request'):
                cont = info.request
            else:
                raise Exception("请传入正确的参数")
            return func(cont, *args, **kwargs)
        return wrapper
    return decorator


def user_passes_test(test_func):
    def decorator(f):
        @wraps(f)
        @context(f)
        def wrapper(context, *args, **kwargs):
            if test_func(context.user):
                return f(*args, **kwargs)
            raise exceptions.PermissionDenied
        return wrapper
    return decorator


login_required = user_passes_test(lambda u: u.is_authenticated)
staff_member_required = user_passes_test(lambda u: u.is_active and u.is_staff)


def throw_error(error_message):
    """
    当程序报错时，指定给前端返回的错误信息，以及打印原始错误记录。
    注：需要放在其他装饰器前面
    :param error_message:
    :return:
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger = logging.getLogger(func.__name__)
                logger.error(e)
                raise Exception(error_message)
        return wrapper
    return decorator


def permission_required(perm):
    def check_perms(user):
        if isinstance(perm, six.string_types):
            perms = (perm,)
        else:
            perms = perm

        if user.has_perms(perms):
            return True
        return False
    return user_passes_test(check_perms)


def token_auth(f):
    @wraps(f)
    def wrapper(cls, root, info, password, **kwargs):
        def on_resolve(values):
            user, payload = values
            payload.token = get_token(user, info.context)
            return payload

        username = kwargs.get(get_user_model().USERNAME_FIELD)

        user = authenticate(
            request=info.context,
            username=username,
            password=password)

        if user is None:
            raise exceptions.GraphQLJWTError(
                # _('Please, enter valid credentials'))
                _('请输入正确的账号密码！'))

        if hasattr(info.context, 'user'):
            info.context.user = user

        result = f(cls, root, info, **kwargs)
        values = (user, result)

        # Improved mutation with thenable check
        if is_thenable(result):
            return Promise.resolve(values).then(on_resolve)
        return on_resolve(values)
    return wrapper
