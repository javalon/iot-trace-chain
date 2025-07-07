from graphene import Field, Int, ObjectType, List, String
from back_api.gql.types import DeviceObject, DeviceTimesObject, UserObject, DeviceDataObject
from back_api.db.database import Session
from back_api.db.models import Device, User
from back_api.utils.decorators import admin_user, authenticated_user_same_as_or_admin
from back_api.utils.auth import get_authentication_user
from back_api.gql.device.service import DeviceService

class Query(ObjectType):
    devices = List(DeviceObject)
    device = Field(DeviceObject, id=Int(required=True))
    device_data = List(DeviceDataObject, id=Int(required=True), data_from=Int(required=False), data_to=Int(required=False))
    device_times = Field(DeviceTimesObject, id=Int(required=True))
    users = List(UserObject)
    user = Field(UserObject, id=Int(required=True))

    @staticmethod
    @authenticated_user_same_as_or_admin
    def resolve_devices(root, info):
        # If user is admin retur all devices, otherwise return devices of the authenticated user
        session = Session()
        user = get_authentication_user(info.context)
        if user and user.role == 'admin':
            devices = session.query(Device).all()
        else:
            devices = session.query(Device).filter(Device.user_id == user.id).all()
        session.close()
        return devices
    
    @staticmethod
    @authenticated_user_same_as_or_admin
    def resolve_device_data(root, info, id, data_from=None, data_to=None):
        session = Session()
        user = get_authentication_user(info.context)
        device = session.query(Device).filter(Device.id == id).first()
        if not device:
            session.close()
            raise Exception("Device not found")
        if user.role != 'admin' and device.user_id != user.id:
            session.close()
            raise Exception("You do not have permission to access this device")
        session.close()

        # Return the device data
        device_data = DeviceService.get_device_data(device.device_id, data_from, data_to)
        return [DeviceDataObject(**item) for item in device_data]
    
    @staticmethod
    @authenticated_user_same_as_or_admin
    def resolve_device_times(root, info, id):
        session = Session()
        user = get_authentication_user(info.context)
        device = session.query(Device).filter(Device.id == id).first()
        if not device:
            session.close()
            raise Exception("Device not found")
        if user.role != 'admin' and device.user_id != user.id:
            session.close()
            raise Exception("You do not have permission to access this device")
        session.close()

        # Return the device times
        device_times = DeviceService.get_device_times(device.device_id)
        print(device_times)
        return DeviceTimesObject(
            max_date=device_times.get('max_date'),
            min_date=device_times.get('min_date')
        )
    
    @staticmethod
    @authenticated_user_same_as_or_admin
    def resolve_device(root, info, id):
        session = Session()
        device = session.query(device).filter(device.id == id).first()
        session.close()
        if not device:
            raise Exception("Device not found")
        return device
    
    @staticmethod
    @admin_user
    def resolve_users(root, info):
        return Session().query(User).all()
    
    @staticmethod
    @admin_user
    def resolve_user(root, info, id):
        session = Session()
        user = session.query(User).filter(User.id == id).first()
        session.close()
        if not user:
            raise Exception("User not found")
        return user
    