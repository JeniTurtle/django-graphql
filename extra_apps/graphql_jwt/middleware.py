from django.http import JsonResponse
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin

from .exceptions import GraphQLJWTError
from .utils import get_authorization_header
from .authentication import Authentication


class JSONWebTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if get_authorization_header(request) is not None:
            if not hasattr(request, 'user') or request.user.is_anonymous:
                # 我这里没用配置backends的方式，直接通过中间件设置user内容
                authenticate = Authentication(request)
                
                try:
                    user = authenticate.authenticate()
                except GraphQLJWTError as err:
                    return JsonResponse({
                        'errors': [{'message': str(err)}],
                    }, status=401)

                if user is not None:
                    request.user = request._cached_user = user

    def process_response(self, request, response):
        patch_vary_headers(response, ('Authorization',))
        return response
