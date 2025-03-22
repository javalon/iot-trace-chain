from jsonschema import validate

from persistence_worker.utils.hashing import generate_hash
from persistence_worker.utils.schema import schema


def validate_json(data):
    validate(instance=data, schema=schema)


def check_data_integrity(data):
    from copy import deepcopy

    data_sha256 = data["sha256"]
    data_copy = deepcopy(data)
    data_copy.pop("sha256")
    return generate_hash(data_copy) == data_sha256
