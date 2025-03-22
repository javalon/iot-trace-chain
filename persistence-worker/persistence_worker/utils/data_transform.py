from persistence_worker.utils.merkle_tree import generate_merkle_proof, generate_merkle_root
from persistence_worker.utils.time_profiling import measure_time


@measure_time
def transform_iot_data(device_id, iot_data):
    required_keys = ["support", "mac", "imei", "sha256", "data"]
    for key in required_keys:
        if key not in iot_data:
            raise ValueError(f"Missing required key: {key}")

    transformed_data = []
    for data in iot_data["data"]:
        if "timestamp" not in data:
            raise ValueError("Missing required key: timestamp in data element")
        transformed_data.append(
            {
                "device_id": device_id,
                "support": iot_data["support"],
                "mac": iot_data["mac"],
                "imei": iot_data["imei"],
                "sha256_orig": iot_data["sha256"],
                "timestamp": data["timestamp"],
                "data": {**data},
            }
        )

    return transformed_data


@measure_time
def prepare_data_to_save(device_id, iot_data):
    transformed_data = transform_iot_data(device_id, iot_data)
    merkle_root = generate_merkle_root(transformed_data)
    for i, data in enumerate(transformed_data):
        proof = generate_merkle_proof(transformed_data, i)
        data["merkle_proof"] = proof
    return merkle_root, transformed_data
