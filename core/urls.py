from django.conf.urls import url
from django.views.static import serve
from graphene_django.views import GraphQLView

import xadmin
from .schema import schema, authed_schema
from .settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^unauthorized_graphiql/', GraphQLView.as_view(graphiql=True, schema=schema)),
    url(r'^graphiql/', GraphQLView.as_view(graphiql=True, schema=authed_schema)),  # 登陆后才有权限访问
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]
