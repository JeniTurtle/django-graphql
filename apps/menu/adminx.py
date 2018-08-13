import xadmin

from .models import Menus


class MenusAdmin(object):
    model_icon = 'fa fa-cog'
    list_display = ['menu_name', 'menu_type', 'menu_url', 'menu_parent', 'menu_order', 'create_time']
    search_fields = ['menu_name', 'menu_url']
    list_editable = ['menu_order', 'menu_name', 'menu_url', 'menu_parent', 'menu_type']
    list_filter = ['menu_type', 'menu_parent']

xadmin.site.register(Menus, MenusAdmin)
