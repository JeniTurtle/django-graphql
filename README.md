# django_graphql

------


django + graphql实现前后端分离。支持jwt登录效验，以及resolver权限绑定。

### 一、安装依赖

> pip install -r requirements.txt

------

### 二、配置数据库链接

> 打开core/setting.py，找到databases选项并修改

```python
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jouryu_django',
        'USER': 'root',
        'PASSWORD': '!',
        'HOST': '127.0.0.1',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB;'
        }
    }
}
```

------

### 三、创建数据库

> 例：CREATE DATABASE jouryu_django DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

------

### 四、执行makemigrations命令

> python manage.py makemigrations

------

### 五、执行migrate命令

> python manage.py migrate

------

### 六、创建超级管理员

> python manage.py createsuperuser

------

### 六、进入xadmin后台

> http://127.0.0.1:8000/xadmin

------

### 七、进入graphql调试界面

> 无需效验登录：http://127.0.0.1:8000/unauthorized_graphiql
> 需要效验登录：http://127.0.0.1:8000/graphiql

------
