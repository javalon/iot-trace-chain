from datetime import  datetime, timedelta, timezone
from back_api.settings.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRATION_TIME_MINUTES
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError
from back_api.db.models import User
from back_api.db.database import Session
from jwt.exceptions import InvalidSignatureError

ph = PasswordHasher()

def generate_token(email, name, role):
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": email,
        "exp": expiration_time,
        "iat": datetime.now(timezone.utc),
        "name": name,
        "role": role
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def hash_password(password):
    return ph.hash(password)

def verify_password(plain_password, hashed_password):
    try:
        ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        raise GraphQLError("Invalid password.")
    
def get_authentication_user(context):
    request_object = context.get("request")
    auth_header = request_object.headers.get("Authorization")

    if auth_header:
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc):
                raise GraphQLError("Token has expired.")
            
            session = Session()
            user = session.query(User).filter(User.email == payload.get("sub")).first()

            if not user:
                raise GraphQLError("Could not authenticatre user.")
            return user
        except InvalidSignatureError:
            raise GraphQLError("Invalid authentication token.")
    else:
        raise GraphQLError("Authentication token is missing.")