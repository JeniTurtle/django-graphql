import graphene

from user import schemas as user_schema
from menu import schemas as menu_schema


# 不验证登录
class Querys(
    graphene.ObjectType,
    user_schema.Query
):
    pass


# 不验证登录
class Mutations(
    graphene.ObjectType,
    user_schema.Mutation
):
    pass


# 验证登录
class AuthedQuerys(
    graphene.ObjectType,
    user_schema.AuthedQuery,
    menu_schema.AuthedQuery
):
    pass


# 验证登录
class AuthedMutations(
    graphene.ObjectType,
    user_schema.AuthedMutation,
    menu_schema.AuthedMutation
):
    pass

schema = graphene.Schema(query=Querys, mutation=Mutations)
authed_schema = graphene.Schema(query=AuthedQuerys, mutation=AuthedMutations)
