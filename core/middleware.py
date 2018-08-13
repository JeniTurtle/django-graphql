from django.http import JsonResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from re import compile


EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info.lstrip('/')
        if any(m.match(path) for m in EXEMPT_URLS):
            if not request.user.is_authenticated:
                return JsonResponse({
                    'errors': [{'message': '登陆后才允许访问'}],
                }, status=401)
