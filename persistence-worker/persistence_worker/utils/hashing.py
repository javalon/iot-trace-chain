import hashlib
import json


def get_device_id(mac, imei):
    return hashlib.sha256((str(mac) + str(imei)).encode("utf-8")).hexdigest()

def generate_hash(data):
    data_string = get_data_string(data)
    return hashlib.sha256(data_string.encode("utf-8")).hexdigest()

def get_data_string(data):
    filtered = {k: v for k, v in data.items() if k != "hash"}  # Remove hash key
    return json.dumps(filtered, sort_keys=True, separators=(",", ":"))
