from django.utils.translation import ugettext_lazy as _


class GraphQLJWTError(Exception):
    default_message = None

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super(GraphQLJWTError, self).__init__(message)


class PermissionDenied(GraphQLJWTError):
    default_message = _('没有权限')
    

class NotAuthorization(GraphQLJWTError):
    default_message = _('没有登录')
    

class AuthenticationFailed(GraphQLJWTError):
    default_message = _('无效的认证请求头')
