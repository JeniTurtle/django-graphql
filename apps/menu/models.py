from datetime import datetime
from django.db import models
from django.contrib.auth.models import Group


class Menus(models.Model):
    """
    导航菜单
    """
    MENU_TYPE_CHOICES = ((0, '根菜单'), (1, '一级菜单'), (2, '二级菜单'), (3, '三级菜单'))
    
    menu_name = models.CharField(
        default='',
        max_length=32,
        verbose_name='菜单名称',
        help_text='菜单名称',
    )

    menu_type = models.IntegerField(
        default=0,
        choices=MENU_TYPE_CHOICES,
        verbose_name='菜单级别',
        help_text='菜单级别，0:根菜单，1:一级菜单，2:二级菜单，3:三级菜单',
    )

    menu_url = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='菜单地址',
        help_text='菜单url地址',
    )

    menu_icon = models.ImageField(
        upload_to='menu/images/',
        null=True,
        blank=True,
        verbose_name='菜单icon地址',
        help_text='菜单icon图片地址',
    )
    
    menu_order = models.IntegerField(
        default=0,
        verbose_name='导航序号',
        help_text='导航排序序号，顺序排序',
    )

    menu_parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        verbose_name='父导航',
        help_text='父导航',
        related_name='sub_menu',
        on_delete=models.CASCADE,
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

    class Meta:
        verbose_name = '导航菜单'
        verbose_name_plural = '导航菜单列表'

    def __str__(self):
        return self.menu_name
    
Group.add_to_class('menus', models.ManyToManyField(
    Menus,
    verbose_name='导航菜单',
    blank=True,
))
