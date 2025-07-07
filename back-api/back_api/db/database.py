from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from back_api.db.models import Base, Device, User
from back_api.settings.config import DB_URL
from back_api.db.data import devices_data, users_data

engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)

def prepare_database():
    from back_api.utils.auth import hash_password
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    for device in devices_data:
        session.add(Device(**device))

    for user in users_data:
        user['password_hash'] = hash_password(user['password'])
        del user['password']
        session.add(User(**user))

    session.commit()
    session.close()