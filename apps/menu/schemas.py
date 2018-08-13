from graphene import relay, AbstractType, List, Int, String, Field
from graphene_django import DjangoObjectType, filter
# django_filters 版本 < 2.0.0
from django_filters import FilterSet, OrderingFilter, CharFilter, ChoiceFilter

from graphql_jwt import decorators
from .models import Menus as MenuModel
from core.utils import is_number, decode_id
from .errors import Errors


class MenuInput:
    menu_name = String()
    menu_type = Int()
    menu_parent = String()
    menu_url = String()
    menu_icon = String()
    menu_order = Int()


class MenuNode(DjangoObjectType):
    class Meta:
        model = MenuModel
        exclude_fields = ('create_time', 'update_time')
        interfaces = (relay.Node,)
    
    @classmethod
    @decorators.throw_error(Errors.SELECT_MENU_INFO_FAILED)
    @decorators.permission_required('menu.view_menus')
    def get_node(cls, info, menu_id):
        if menu_id:
            return super().get_node(info, menu_id)
        else:
            return None


class MenuFilter(FilterSet):
    menu_name = CharFilter(field_name='menu_name', lookup_expr='icontains')
    menu_type = ChoiceFilter(field_name='menu_type', choices=MenuModel.MENU_TYPE_CHOICES)
    menu_parent = CharFilter(field_name='menu_parent', lookup_expr='exact')

    class Meta:
        model = MenuModel
        fields = ['menu_name', 'menu_type', 'menu_parent']
    
    @property
    @decorators.throw_error(Errors.SELECT_MENU_LIST_FAILED)
    @decorators.permission_required('menu.view_menus')
    def qs(self):
        menu_parent = self.data.get('menu_parent', None)
        if menu_parent and not is_number(menu_parent):
            self.data['menu_parent'] = decode_id(menu_parent)
        return super().qs
    
    order_by = OrderingFilter(fields=('menu_name', 'menu_order'))


class CreateMenu(relay.ClientIDMutation):
    class Input(MenuInput):
        menu_name = String(required=True)
        menu_type = Int(required=True)
        menu_url = String(required=True)
    
    menu = Field(MenuNode)
    
    @classmethod
    @decorators.throw_error(Errors.CREATE_MENU_FAILED)
    @decorators.permission_required('menu.add_menus')
    def mutate_and_get_payload(cls, root, info, **input):
        if 'menu_parent' in input:
            input['menu_parent'] = MenuModel.objects.get(pk=decode_id(input['menu_parent']))
            
        menu = MenuModel.objects.create(**input)
        return CreateMenu(menu=menu)
    

class DeleteMenu(relay.ClientIDMutation):
    class Input:
        id = String(required=True)

    menu = Field(MenuNode)

    @classmethod
    @decorators.throw_error(Errors.DELETE_MENU_FAILED)
    @decorators.permission_required('menu.delete_menus')
    def mutate_and_get_payload(cls, root, info, **input):
        menu = MenuModel.objects.get(pk=decode_id(input.get('id')))
        menu.delete()
        return DeleteMenu(menu=menu)


class UpdateMenuInfo(relay.ClientIDMutation):
    class Input(MenuInput):
        id = String(required=True)
        pass

    menu = Field(MenuNode)

    @classmethod
    @decorators.throw_error(Errors.UPDATE_MENU_FAILED)
    @decorators.permission_required('menu.change_menus')
    def mutate_and_get_payload(cls, root, info, **input):
        menu_id = decode_id(input.pop('id'))
        menu = MenuModel.objects.get(pk=menu_id)
    
        for key, value in input.items():
            if key == 'menu_parent':
                value = None if value == "" else MenuModel.objects.get(pk=decode_id(value))
            setattr(menu, key, value)

        menu.save()
        return UpdateMenuInfo(menu=menu)


class QueryResolver(object):
    @decorators.throw_error(Errors.SELECT_SELF_MENU_FAILED)
    def resolve_menu_self_menus(self, info, **kwargs):
        user = info.context.user
        return user.get_group_menus(**kwargs)


class AuthedQuery(AbstractType, QueryResolver):
    menu_list = filter.DjangoFilterConnectionField(MenuNode, filterset_class=MenuFilter)
    menu_info = relay.Node.Field(MenuNode)
    menu_self_menus = List(MenuNode, menu_type=Int(), order_by=String(default_value='-create_time'))
    
    
class AuthedMutation(AbstractType):
    menu_update_menu_info = UpdateMenuInfo.Field()
    menu_create_menu = CreateMenu.Field()
    menu_delete_menu = DeleteMenu.Field()
