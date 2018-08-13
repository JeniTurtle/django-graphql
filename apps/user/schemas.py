from graphene import relay, Field, AbstractType, String, Int, Boolean
from graphene_django import DjangoObjectType, filter
from graphql_jwt import relay as jwt_relay, shortcuts, decorators
# django_filters 版本 < 2.0.0
from django_filters import FilterSet, OrderingFilter, CharFilter

from core.utils import decode_id
from .models import Users as UserModel
from .errors import Errors


class LoginUserInput:
    username = String(required=True)
    password = String(required=True)


class UpdateUserInfoInput:
    real_name = String(required=True)
    mobile = String(required=True)
    email = String(required=True)
    gender = Int(default_value=0)


class RegisterUserInput(UpdateUserInfoInput, LoginUserInput):
    pass


class UserNode(DjangoObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ('password', 'first_name', 'last_name')
        interfaces = (relay.Node,)
    
    @classmethod
    @decorators.throw_error(Errors.SELECT_USER_INFO_FAILED)
    @decorators.permission_required('user.view_users')
    def get_node(cls, info, user_id):
        if user_id:
            return super().get_node(info, user_id)
        else:
            return None


class UserFilter(FilterSet):
    username = CharFilter(field_name=UserModel.USERNAME_FIELD, lookup_expr='icontains')
    real_name = CharFilter(field_name='real_name', lookup_expr='icontains')
    mobile = CharFilter(field_name='mobile', lookup_expr='icontains')
    email = CharFilter(field_name='email', lookup_expr='icontains')
    
    class Meta:
        model = UserModel
        fields = ['username', 'real_name', 'mobile', 'email']

    @property
    @decorators.throw_error(Errors.SELECT_USER_LIST_FAILED)
    @decorators.permission_required('user.view_users')
    def qs(self):
        return super().qs
    
    order_by = OrderingFilter(fields=('create_time', 'username'))


class RegisterUser(relay.ClientIDMutation):
    class Input(RegisterUserInput):
        pass

    payload = Field(UserNode)
    token = String()
    
    @classmethod
    @decorators.permission_required('user.add_users')
    def mutate_and_get_payload(cls, root, info, **input):
        email = input.pop('email')
        username = input.pop(UserModel.USERNAME_FIELD, email)
        password = input.pop('password') if 'password' in input else UserModel.objects.make_random_password()
        
        user = UserModel.objects.create_user(username, email, password, **input)
        token = shortcuts.get_token(user, info.context)
        return RegisterUser(payload=user, token=token)


class UpdateSelfInfo(relay.ClientIDMutation):
    class Input(UpdateUserInfoInput):
        real_name = String()
        mobile = String()
        email = String()
    
    payload = Field(UserNode)
    
    @classmethod
    @decorators.throw_error(Errors.UPDATE_USER_INFO_FAILED)
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user
        
        for key, value in input.items():
            setattr(user, key, value)
        
        user.save()
        
        updated_user = UserModel.objects.get(pk=user.pk)
        
        return UpdateSelfInfo(payload=updated_user)


class UpdateUserInfo(relay.ClientIDMutation):
    class Input(UpdateUserInfoInput):
        id = String(required=True)
        real_name = String()
        mobile = String()
        email = String()
        is_staff = Boolean()
        is_active = Boolean()
    
    payload = Field(UserNode)
    
    @classmethod
    @decorators.throw_error(Errors.UPDATE_USER_INFO_FAILED)
    @decorators.permission_required('user.change_users')
    def mutate_and_get_payload(cls, root, info, **input):
        user_id = decode_id(input.pop('id'))
        updated_user = UserModel.objects.get(pk=user_id)
        
        for key, value in input.items():
            setattr(updated_user, key, value)
        
        updated_user.save()
        return UpdateUserInfo(payload=updated_user)
    
    
class ResetUserPassword(relay.ClientIDMutation):
    class Input:
        password = String(required=True)
        id = String(required=True)

    payload = Field(UserNode)

    @classmethod
    @decorators.throw_error(Errors.RESET_USER_PASSWORD_FAILED)
    @decorators.permission_required('user.graphql_reset_password')
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            uid = decode_id(input.get('id'))
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise Exception('无效的用户id')
        
        user.set_password(input.pop('password'))
        user.save()

        return ResetUserPassword(payload=user)


class ResetSelfPassword(relay.ClientIDMutation):
    class Input:
        password = String(required=True)
        current_password = String(required=True)
    
    payload = Field(UserNode)
    
    @classmethod
    @decorators.throw_error(Errors.RESET_USER_PASSWORD_FAILED)
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user
        current_password = input.pop('current_password')
    
        if user.check_password(current_password):
            user.set_password(input.pop('password'))
        else:
            raise Exception("当前密码不正确")
    
        user.save()
        
        return ResetSelfPassword(payload=user)


class Login(jwt_relay.JSONWebTokenMutation):
    payload = Field(UserNode)

    @classmethod
    def resolve(cls, root, info):
        return cls(payload=info.context.user)
    

class QueryResolver(object):
    @decorators.throw_error(Errors.SELECT_USER_INFO_FAILED)
    def resolve_self_info(self, info, **kwargs):
        return UserNode.get_node(info, info.context.user.id)


# 无需效验登录权限
class Mutation(AbstractType):
    user_login = Login.Field()
    

# 无需效验登录权限
class Query(AbstractType):
    user_verify_token = jwt_relay.Verify.Field()


# 需要效验登录权限
class AuthedMutation(AbstractType):
    user_register_user = RegisterUser.Field()
    user_update_self_info = UpdateSelfInfo.Field()
    user_update_user_info = UpdateUserInfo.Field()
    user_reset_user_password = ResetUserPassword.Field()
    user_reset_self_password = ResetSelfPassword.Field()
    

# 需要效验登录权限
class AuthedQuery(AbstractType, QueryResolver):
    user_refresh_token = jwt_relay.Refresh.Field()
    user_list = filter.DjangoFilterConnectionField(UserNode, filterset_class=UserFilter)
    user_user_info = relay.Node.Field(UserNode)
    user_self_info = Field(UserNode)
