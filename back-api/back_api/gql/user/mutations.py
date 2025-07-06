from graphene import Mutation, String, Field
from graphql import GraphQLError
from back_api.db.database import Session
from back_api.db.models import User
from back_api.gql.types import UserObject
from back_api.utils.auth import generate_token, get_authentication_user, hash_password, verify_password
from back_api.utils.decorators import admin_user

class LoginUser(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    def mutate(root, info, email, password):
        session = Session()
        user = session.query(User).filter(User.email == email).first()
        session.close()

        if not user:
            raise GraphQLError("A user with this email does not exist.")
        
        verify_password(password, user.password_hash)

        token = generate_token(email, user.username, user.role)
        return LoginUser(token=token)
    
class AddUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(lambda: UserObject)

    @staticmethod
    @admin_user
    def mutate(root, info, username, email, password, role):
        if role == "admin":
            current_user = get_authentication_user(info.context)
            if current_user.role != "admin":
                raise GraphQLError("Only admins can create other admin users.")

        session = Session()
        existing_user = session.query(User).filter(User.email == email).first()

        if existing_user:
            session.close()
            raise GraphQLError("A user with this email already exists.")

        user = User(username=username, email=email, password_hash=hash_password(password), role=role)
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()

        return AddUser(user=user)