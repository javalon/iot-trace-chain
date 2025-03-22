import hashlib
import json


def get_device_id(mac, imei):
    return hashlib.sha256((str(mac) + str(imei)).encode("utf-8")).hexdigest()


def generate_hash(data):
    filtered = {k: v for k, v in data.items() if k != "hash"}  # Remove hash key
    data_string = json.dumps(filtered, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data_string.encode("utf-8")).hexdigest()
