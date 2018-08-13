from calendar import timegm
from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

import jwt

from .exceptions import GraphQLJWTError
from .settings import jwt_settings


def jwt_payload(user, context=None):
    username = user.get_username()
    
    if hasattr(username, 'pk'):
        username = username.pk

    payload = {
        'id': user.id,
        user.USERNAME_FIELD: username,
        'exp': datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA,
    }

    if jwt_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(datetime.utcnow().utctimetuple())

    if jwt_settings.JWT_AUDIENCE is not None:
        payload['aud'] = jwt_settings.JWT_AUDIENCE

    if jwt_settings.JWT_ISSUER is not None:
        payload['iss'] = jwt_settings.JWT_ISSUER

    return payload


def jwt_encode(payload, context=None):
    return jwt.encode(
        payload,
        jwt_settings.JWT_SECRET_KEY,
        jwt_settings.JWT_ALGORITHM,
    ).decode('utf-8')


def jwt_decode(token, context=None):
    return jwt.decode(
        token,
        jwt_settings.JWT_SECRET_KEY,
        jwt_settings.JWT_VERIFY,
        options={
            'verify_exp': jwt_settings.JWT_VERIFY_EXPIRATION,
        },
        leeway=jwt_settings.JWT_LEEWAY,
        audience=jwt_settings.JWT_AUDIENCE,
        issuer=jwt_settings.JWT_ISSUER,
        algorithms=[jwt_settings.JWT_ALGORITHM])


def get_authorization_header(request):
    auth = request.META.get('HTTP_AUTHORIZATION', '').split()
    prefix = jwt_settings.JWT_AUTH_HEADER_PREFIX

    if len(auth) != 2 or auth[0].lower() != prefix.lower():
        return None
    return auth[1]


def get_payload(token, context=None):
    try:
        payload = jwt_settings.JWT_DECODE_HANDLER(token, context)
    except jwt.ExpiredSignature:
        raise GraphQLJWTError(_('登录已过期'))
    except jwt.DecodeError:
        raise GraphQLJWTError(_('签名解码失败'))
    except jwt.InvalidTokenError:
        raise GraphQLJWTError(_('无效的token'))
    return payload


def get_user_by_natural_key(user_id):
    user = get_user_model()
    try:
        return user.objects.get_by_natural_key(user_id)
    except user.DoesNotExist:
        msg = _('用户不存在')
        raise GraphQLJWTError(msg)


def get_user_by_payload(payload):
    username = payload.get(get_user_model().USERNAME_FIELD)

    if not username:
        raise GraphQLJWTError(_('无效的签名'))

    user = get_user_by_natural_key(username)

    if user is not None and not user.is_active:
        raise GraphQLJWTError(_('用户已停用'))
    return user
