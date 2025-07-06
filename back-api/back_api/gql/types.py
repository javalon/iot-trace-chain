from graphene import ObjectType, String, Int, Field, List, DateTime
from graphene.types.generic import GenericScalar
    
class DeviceObject(ObjectType):
    id = Int()
    name = String()
    description = String()
    mac = String()
    imei = String()
    device_id = String()
    user_id = Int()
    user = Field(lambda: UserObject)

    @staticmethod
    def resolve_user(root, info):
        return root.user if root.user else None
    
class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    role = String()

    @staticmethod
    def resolve_role(root, info):
        return root.role if root.role else "user"  # Default role if not set
    
class MerkleProofEntry(ObjectType):
    hash = String()
    position = String()
    level = Int()

class DeviceDataObject(ObjectType):
    device_id = String(name="deviceId")
    support = List(String)
    mac = String()
    imei = String()
    sha256_orig = String(name="sha256Orig")
    timestamp = DateTime()
    data = GenericScalar()
    hash = String()
    merkle_proof = String(name="merkleProof")
    tx_hash = String(name="txHash")
    record_id = String(name="recordId")
    ts_cast = DateTime(name="tsCast")
    date = DateTime()

class DeviceTimesObject(ObjectType):
    max_date = Int(name="maxDate")
    min_date = Int(name="minDate")
