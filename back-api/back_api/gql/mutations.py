from graphene import ObjectType
from back_api.gql.device.mutations import AddDevice, UpdateDevice, DeleteDevice
from back_api.gql.user.mutations import AddUser, LoginUser

class Mutation(ObjectType):
    add_device = AddDevice.Field()
    update_device = UpdateDevice.Field()
    delete_device = DeleteDevice.Field()

    login_user = LoginUser.Field()
    add_user = AddUser.Field()