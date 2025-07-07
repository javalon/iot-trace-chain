from functools import wraps
from graphql import GraphQLError
from back_api.utils.auth import get_authentication_user

def admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authentication_user(info.context)

        if user.role != "admin":
            raise GraphQLError("Only admins can perform this action.")
        
        return func(*args, **kwargs)
    
    return wrapper

def authenticated_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authentication_user(info.context)
        if not user:
            raise GraphQLError("Authentication required.")
        
        return func(*args, **kwargs)
    return wrapper

def authenticated_user_same_as(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authentication_user(info.context)
        user_id = kwargs.get('user_id')

        if not user or user.id != user_id :
            raise GraphQLError("Authentication required or user does not match.")
        
        return func(*args, **kwargs)
    return wrapper

def authenticated_user_same_as_or_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authentication_user(info.context)
        user_id = kwargs.get('user_id')

        if not user or (user.id != user_id and user.role != "admin"):
            raise GraphQLError("Authentication required or user does not match.")
        
        return func(*args, **kwargs)
    return wrapper