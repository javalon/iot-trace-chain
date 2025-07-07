import hashlib
from graphene import Mutation, String, Int, Field
from back_api.gql.types import DeviceObject
from back_api.db.database import Session
from back_api.db.models import Device
from back_api.utils.decorators import admin_user

class AddDevice(Mutation):
    class Arguments:
        name = String(required=True)
        description = String(required=True)
        user_id = Int(required=True)
        mac = String(required=False)
        imei = String(required=False)

    device = Field(lambda: DeviceObject)

    @staticmethod
    @admin_user
    def mutate(root, info, name, description, mac, imei, user_id):
        device_id = None
        if mac or imei:
            device_id = hashlib.sha256((str(mac) + str(imei)).encode("utf-8")).hexdigest()
        device = Device(
            name=name, 
            description=description,
            mac=mac,
            imei=imei,
            device_id=device_id,
            user_id=user_id
            )
        session = Session()
        session.add(device)
        session.commit()
        session.refresh(device)
        session.close()
        return AddDevice(device=device)        
    
class UpdateDevice(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        description = String()
        mac = String()
        imei = String()
        user_id = Int()

    device = Field(lambda: DeviceObject)

    @staticmethod
    @admin_user
    def mutate(root, info, id, name=None, description=None, mac=None, imei=None, user_id=None):
        session = Session()
        device = session.query(Device)\
            .filter(Device.id == id)\
            .first()
        if not device:
            session.close()
            raise Exception("Device not found")
        
        if name:
            device.name = name
        if description:
            device.description = description
        if user_id:
            device.user_id = user_id
        if mac:
            device.mac = mac
        if imei:
            device.imei = imei
        if mac or imei:
            device.device_id = hashlib.sha256((str(mac) + str(imei)).encode("utf-8")).hexdigest()
        
        session.commit()
        session.refresh(device)
        session.close()
        return UpdateDevice(device=device)
        
class DeleteDevice(Mutation):
    class Arguments:
        id = Int(required=True)

    success = String()

    @staticmethod
    @admin_user
    def mutate(root, info, id):
        session = Session()
        device = session.query(Device).filter(Device.id == id).first()
        if not device:
            session.close()
            raise Exception("Device not found")
        
        session.delete(device)
        session.commit()
        session.close()
        return DeleteDevice(success="Device deleted successfully")
