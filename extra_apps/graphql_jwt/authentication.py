from .utils import get_payload, get_authorization_header, get_user_by_payload


class Authentication(object):
    
    def __init__(self, request=None):
        if not request:
            raise Exception('缺少request参数')
        self.context = request

    def authenticate(self):
        jwt_value = get_authorization_header(self.context)
        
        if jwt_value is None:
            return None

        jwt_dict = get_payload(jwt_value, self.context)

        return get_user_by_payload(jwt_dict)
