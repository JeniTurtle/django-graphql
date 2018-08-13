from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

from menu.models import Menus as MenuModel


class Users(AbstractUser):
    """
    用户
    """
    real_name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name='真实姓名',
        help_text='用户真实姓名',  # 作为graphql api文档中的说明
    )
    
    mobile = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        verbose_name='用户手机号码',
        help_text='用户手机号码',
    )
    
    gender = models.IntegerField(
        default=0,
        choices=((0, '未知'), (1, '男'), (2, '女')),
        verbose_name='性别，0:未知，1:男，2:女',
        help_text='性别，0:未知，1:男，2:女',
    )
    
    email = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='用户邮箱',
        help_text='用户邮箱',
    )
    
    create_time = models.DateTimeField(
        default=datetime.now,
        verbose_name='创建时间',
        help_text='创建时间',
    )
    
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='修改时间',
        help_text='修改时间',
    )

    first_name = None
    
    last_name = None
    
    class Meta:
        verbose_name = '用户'
        
        verbose_name_plural = '用户列表'
        
        permissions = (
            ('graphql_reset_password', '重置用户密码'),
        )
    
    def get_group_menus(self, **kwargs):
        order_by = kwargs.pop('order_by')
        menu_type = kwargs.get('menu_type', None)
        user_groups_field = self.__class__._meta.get_field('groups')
        user_groups_query = 'group__%s' % user_groups_field.related_query_name()
        opts = {
            user_groups_query: self,
        }
        if menu_type is not None:
            opts['menu_type'] = menu_type
        
        return MenuModel.objects.filter(**opts).order_by(order_by)
    
    def __str__(self):
        return self.username
