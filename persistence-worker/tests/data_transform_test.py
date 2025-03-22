import pytest

from persistence_worker.utils.data_transform import prepare_data_to_save, transform_iot_data


def test_transform_iot_data():
    iot_data = {
        "support": ["TEMP", "GPS"],
        "mac": "00:00:00:00:00:00",
        "imei": "000000000000000",
        "sha256": "123123123123123",
        "data": [
            {"temp": "25", "timestamp": "2021-01-01T00:00:00", "lat": "0", "long": "0"},
            {"temp": "26", "timestamp": "2021-01-01T00:01:00", "lat": "0", "long": "0"},
        ],
    }

    device_id = "abc123"

    result = transform_iot_data(device_id, iot_data)

    assert len(result) == 2

    for i, entry in enumerate(result):
        assert entry["device_id"] == device_id
        assert entry["support"] == iot_data["support"]
        assert entry["mac"] == iot_data["mac"]
        assert entry["imei"] == iot_data["imei"]
        assert entry["sha256_orig"] == iot_data["sha256"]
        assert entry["timestamp"] == iot_data["data"][i]["timestamp"]
        assert entry["data"] == iot_data["data"][i]


def test_transform_iot_data_empty_data():
    iot_data = {
        "support": ["TEMP", "GPS"],
        "mac": "00:00:00:00:00:00",
        "imei": "000000000000000",
        "sha256": "123123123123123",
        "data": [],
    }

    device_id = "abc123"

    result = transform_iot_data(device_id, iot_data)

    assert result == []


def test_prepare_data_to_save_empty_data():
    iot_data = {
        "support": ["TEMP"],
        "mac": "00:00:00:00:00:00",
        "imei": "000000000000000",
        "sha256": "abc123",
        "data": [],
    }

    device_id = "test-device"
    with pytest.raises(ValueError, match="Empty data array"):
        prepare_data_to_save(device_id, iot_data)


def test_prepare_data_to_save_missing_required_key():
    incomplete_iot_data = {
        "support": ["TEMP"],
        "mac": "00:00:00:00:00:00",
        "imei": "000000000000000",
        # "sha256" is missing
        "data": [{"temp": "25", "timestamp": "2021-01-01T00:00:00"}],
    }

    device_id = "test-device"
    with pytest.raises(ValueError, match="Missing required key: sha256"):
        prepare_data_to_save(device_id, incomplete_iot_data)


def test_prepare_data_to_save_missing_timestamp_in_data():
    iot_data = {
        "support": ["TEMP"],
        "mac": "00:00:00:00:00:00",
        "imei": "000000000000000",
        "sha256": "abc123",
        "data": [
            {
                "temp": "25"
                # missing "timestamp"
            }
        ],
    }

    device_id = "test-device"
    with pytest.raises(ValueError, match="Missing required key: timestamp in data element"):
        prepare_data_to_save(device_id, iot_data)
