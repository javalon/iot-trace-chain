schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "sha256": {"type": "string"},
        "mac": {"type": "string"},
        "imei": {"type": "string"},
        "support": {"type": "array", "items": {"type": "string"}},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "timestamp": {"type": "string"},
                    "lat": {"type": "string"},
                    "long": {"type": "string"},
                    "temp": {"type": "string"},
                },
                "required": ["timestamp"],
            },
        },
    },
    "required": ["sha256", "mac", "imei", "support", "data"],
}
